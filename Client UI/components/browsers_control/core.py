import logging
import threading
from PyQt5 import QtCore

from .. import settings
from importlib import import_module


logger = logging.getLogger('Client UI.components.browsers_control.core')


class BrowserControl:
    diag_signal = QtCore.pyqtSignal(str)
    bet_params = dict

    def __init__(self, control_settings: dict):
        self.control_settings = control_settings

    def start(self):
        """Запуск потоков загрузки браузеров и авторизации на сайтах БК"""
        started_threads = {}
        control_modules = self.__get_control_modules()
        auth_data = self.control_settings["auth_data"]

        for bkmkr_name in auth_data.keys():
            if not (auth_data[bkmkr_name]['login'] and auth_data[bkmkr_name]['password']):
                try:
                    del control_modules[bkmkr_name]
                except BaseException:
                    continue

        for bkmkr_name in control_modules.keys():
            if auth_data.get(bkmkr_name):
                control_module = control_modules[bkmkr_name]
                thread_event = threading.Event()
                control = control_module.Control({'bkmkr_name': bkmkr_name, 'auth_data': auth_data[bkmkr_name]},
                                                 thread_event)
                control_thread = threading.Thread(target=control.preload, daemon=True)
                control_thread.start()
                started_threads[bkmkr_name] = {'control_thread': control_thread, 'thread_event': thread_event}

    def bet(self) -> None:
        """Разместить ставки на найденное событие"""



    @staticmethod
    def __get_control_modules() -> dict:
        """Получение перечня доступных модулей управления вебстраницами букмекеров"""
        modules_dict = {}
        for bkmkr_name in settings.BOOKMAKERS.keys():
            try:
                module = import_module(f'.browsers_control.websites_control_modules.{bkmkr_name}', package='components')
            except BaseException as ex:
                logger.error(ex)
                continue
            modules_dict[bkmkr_name] = module
        return modules_dict


if __name__ == '__main__':
    pass
