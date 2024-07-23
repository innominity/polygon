import os
import importlib.util
import sys
import shutil
import zipfile
from django.conf import settings
from .models import (
    RemoteApp,
    RemoteAppFileConfigType,
    RemoteAppTask,
    RemoteAppTaskFileConfig,
)


class RemoteAppSoftwareBase:
    """Базовый класс для обертки над функциональностью программы"""

    def __init__(self, app_dir_path):
        self.app_dir_path = app_dir_path
        self.config = {}

    @property
    def app_dir_path(self):
        return self.__app_dir_path

    @app_dir_path.setter
    def app_dir_path(self, app_dir_path):
        self.__app_dir_path = app_dir_path

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config: dict):
        self.__config = config

    def run(self):
        """Основной метод запуcка программы на выполнение"""
        pass

    def dispose(self):
        """Очистить ресурсы"""
        pass


class RemoteAppSoftwareTask:
    """Запуск задач ПО"""

    ROOT_APP_TASKS_PATH = os.path.join(settings.MEDIA_ROOT, "tasks")
    MODULE_NAME = "remote_software_app"

    def __init__(
        self,
        remote_app_guid: str = None,
        remote_app_task_guid: str = None,
        guid_config_files: list[str] = None,
    ):
        """Инициализация задачи выполнения

        Args:
            remote_app_guid (str): GUID задачи из базы данных модель RemoteApp. Defaults to None.
            remote_app_task_guid (str): GUID задачи выполнения ПО из базы данных модель RemoteAppTask. Defaults to None.
            guid_config_files (list[str], optional): Список GUID файлов конфигурации из бд модель RemoteAppTaskFileConfig. Defaults to None.
        """
        if remote_app_guid is None and remote_app_task_guid is None:
            raise Exception(
                "Должен быть передан либо GUID приложения либо GUID задачи выполнения приложения"
            )

        self.__remote_app_guid = remote_app_guid
        self.__task_guid = (
            self.__create_app_task(remote_app_guid)
            if remote_app_task_guid is None
            else remote_app_task_guid
        )
        if remote_app_task_guid is None:
            self.__create_app_subfolder()

            if guid_config_files is not None:
                self.__attach_config_files(guid_config_files)
        else:
            remote_app_task = RemoteAppTask.objects.filter(guid=remote_app_task_guid)
            if len(remote_app_task) == 0:
                raise Exception("Задач выполнения программного обеспечения не найдена!")

    @classmethod
    def __get_app_task_folder(cls, app_task_guid: str) -> str:
        """Метод получения пути до директории выполнения ПО

        Args:
            app_task_guid (str): GUID задачи из базы данных модель RemoteAppTask

        Returns:
            str: путь расположения ПО и файлов конфигурации
        """
        if app_task_guid is None:
            raise Exception("Не передан GUID приложения!")
        remote_app_task = RemoteAppTask.objects.filter(guid=app_task_guid)
        if len(remote_app_task) == 0:
            raise Exception("Задач выполнения программного обеспечения не найдена!")
        return os.path.join(cls.ROOT_APP_TASKS_PATH, app_task_guid)

    def __create_app_task(self, remote_app_guid: str) -> str:
        """Создание задачи запуска ПО

        Args:
            remote_app_guid (str): GUID задачи из базы данных модель RemoteApp

        Returns:
            str: GUID задачи выполнения ПО (модель RemoteAppTask)
        """
        remote_app = RemoteApp.objects.get(guid=remote_app_guid)
        remote_app_task = RemoteAppTask(
            remote_app=remote_app, status=RemoteAppTask.TaskStatus.NOT_STARTED
        )
        remote_app_task.save()
        return str(remote_app_task.guid)

    def __attach_config_files(self, guid_config_files: list[str] = None) -> None:
        """Метод закрепления файлов конфигурации за экземпляром выполнения ПО

        Args:
            guid_config_files (list[str], optional): Список GUID файлов конфигурации из бд модель RemoteAppTaskFileConfig. Defaults to None.
        """
        app_task = RemoteAppTask.objects.get(self.__task_guid)
        app_task_dir = self.__get_app_task_folder(self.__task_guid)

        for guid_config_file in guid_config_files:

            config_file = RemoteAppTaskFileConfig.objects.get(guid=guid_config_file)
            config_file_path = config_file.config_file.path
            config_filename = config_file.config_filename
            if config_filename == "":
                raise Exception("Ошибка чтения имения файла конфигурации!")
            # Закрепляем конфиг файл за задачей
            config_file.remote_app_task = app_task
            config_file.save()
            # копируем файл конфигурации в папку приложения
            app_config_file_path = os.path.join(app_task_dir, config_filename)
            shutil.copyfile(config_file_path, app_config_file_path)

    def __create_app_subfolder(self) -> None:
        """Создания директории для выполнения ПО"""
        if self.__task_guid:
            remote_app = RemoteApp.objects.get(guid=self.__remote_app_guid)
            folder_app_run = self.__get_app_task_folder(self.__task_guid)
            with zipfile.ZipFile(remote_app.app_zip.path, "r") as zip_ref:
                zip_ref.extractall(folder_app_run)

    def run(self, config_params: dict = None) -> dict:
        """Метод запуска задачи выполнения ПО с переданными параметрами

        Args:
            config_params (dict, optional): _description_. Defaults to None.

        Returns:
            dict: Результат выполнения задачи
        """
        app_dir = self.__get_app_task_folder(self._task_guid)
        app_module_path = os.path.join(app_dir, "app.py")
        module_name = "remote_software_app"

        spec = importlib.util.spec_from_file_location(module_name, app_module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        remote_software = module.RemoteAppSoftware(app_dir)
        if config_params is not None:
            remote_software.config = config_params

        return remote_software.run()
