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
    
    def __init__(self, remote_app_guid):
        self.__app_guid = remote_app_guid
        self.__task_guid = self.__create_app_task(remote_app_guid)

    def __create_app_task(self, remote_app_guid):
        remote_app = RemoteApp.objects.get(guid=remote_app_guid)
        remote_app_task = RemoteAppTask(remote_app=remote_app, status=RemoteAppTask.TaskStatus.NOT_STARTED)
        remote_app_task.save()
        return remote_app_task.guid

    def __create_app_subfoldler(self):
        pass

    