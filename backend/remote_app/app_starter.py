from .models import 

class RemoteAppBase:
    """Базовый класс для обертки над функциональностью программы
    """

    def __init__(self):
        self.__config = {}

    def run(self):
        """Основной метод запсука программы на выполнение
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
        self.__remote_app_guid = remote_app_guid
        self.__create_app_task()

    def __create_app_task(self, remote_app_guid):
        pass

    def __create_app_subfoldler(self):
        pass