import os
import zipfile
from django.conf import settings
from .models import RemoteApp, RemoteAppFileConfigType, RemoteAppTask, RemoteAppTaskFileConfig

class RemoteAppBase:
    """Базовый класс для обертки над функциональностью программы
    """

    def __init__(self):
        self.__config = {}

    def run(self):
        """Основной метод запуcка программы на выполнение
        """
        pass

    def dispose(self):
        """Очистить ресурсы
        """
        pass

    def set_config(self, config: dict):
        self.__config = config


class RemoteAppTaskStarter:
    """Запуск задач ПО
    """
    ROOT_APP_TASKS_PATH = os.path.join(settings.MEDIA_ROOT, 'tasks')

    def __init__(self, remote_app_guid: str):
        self.__app_guid = remote_app_guid
        self.__task_guid = self.__create_app_task(remote_app_guid)
        self.__create_app_subfolder()

    
    @classmethod
    def __get_app_task_folder(cls, app_guid: str) -> str:
        if app_guid is None:
            raise Exception("Не передан GUID приложения!")
        remote_app_task = RemoteAppTask.objects.filter(guid=app_guid)
        if len(remote_app_task) == 0:
            raise Exception("Задач выполнения программного обеспечения не создана!")
        return os.path.join(cls.ROOT_APP_TASKS_PATH, app_guid)


    def __create_app_task(self, remote_app_guid: str) -> str:
        remote_app = RemoteApp.objects.get(guid=remote_app_guid)
        remote_app_task = RemoteAppTask(remote_app=remote_app, status=RemoteAppTask.TaskStatus.NOT_STARTED)
        remote_app_task.save()
        return str(remote_app_task.guid)


    def __create_app_subfolder(self):
        if self.__task_guid:
            remote_app = RemoteApp.objects.get(guid=self.__app_guid)
            folder_app_run = self.__get_app_task_folder(self.__app_guid)
            with zipfile.ZipFile(remote_app.app_zip.path, 'r') as zip_ref:
                zip_ref.extractall(folder_app_run)


    def run(self):
        pass


    def __run_app(self):
        pass
        
