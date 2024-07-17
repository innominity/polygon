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

    def __init__(self, remote_app_guid):
        self.__app_guid = remote_app_guid
        self.__task_guid = self.__create_app_task(remote_app_guid)
        self.__create_app_subfoldler()


    def __create_app_task(self, remote_app_guid):
        remote_app = RemoteApp.objects.get(guid=remote_app_guid)
        remote_app_task = RemoteAppTask(remote_app=remote_app, status=RemoteAppTask.TaskStatus.NOT_STARTED)
        remote_app_task.save()
        return remote_app_task.guid


    def __create_app_subfoldler(self):
        if self.__task_guid:
            remote_app = RemoteApp.objects.get(guid=self.__app_guid)
            folder_app_run = os.path.join(self.ROOT_APP_TASKS_PATH, self.__task_guid)
            with zipfile.ZipFile(remote_app.app_zip.path, 'r') as zip_ref:
                zip_ref.extractall(folder_app_run)
            
    def __run_app(self):
        pass
