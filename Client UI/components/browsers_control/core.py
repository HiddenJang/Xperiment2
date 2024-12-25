import logging
import threading
from PyQt5 import QtCore
from PyQt5.QtCore import QObject

from .. import settings
from importlib import import_module


logger = logging.getLogger('Client UI.components.browsers_control.core')


class BrowserControl(QObject):
    diag_signal = QtCore.pyqtSignal(str)
    finish_signal = QtCore.pyqtSignal()
    bet_params = {}

    def __init__(self, control_settings: dict):
        super(BrowserControl, self).__init__()
        self.control_settings = control_settings
        self.started_threads = {}
        self.timer = QtCore.QTimer()

    def preload_sites_and_authorize(self):
        """Запуск потоков загрузки браузеров и авторизации на сайтах БК"""

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
                thread_pause_event = threading.Event()
                control = control_module.Control({'bkmkr_name': bkmkr_name, 'auth_data': auth_data[bkmkr_name]},
                                                 thread_pause_event,
                                                 self.diag_signal)
                control_thread = threading.Thread(target=control.preload, daemon=True)
                control_thread.start()
                self.started_threads[bkmkr_name] = {'control_module_class': control_module.Control,
                                                    'control_instance': control,
                                                    'control_thread': control_thread,
                                                    'thread_pause_event': thread_pause_event}
        if not self.started_threads:
            self.diag_signal.emit("Процесс автоматического управления не запущен. "
                                  "Отсутвуют требуемые модули управления или данные авторизации для доступных модулей")
            logger.info("Процесс автоматического управления не запущен. "
                                  "Отсутвуют требуемые модули управления или данные авторизации для доступных модулей")
            self.finish_signal.emit()
            return
        self.diag_signal.emit("Процесс автоматического управления запущен")

    def start_betting(self, events_data: list) -> None:
        """Разместить ставки на одно из найденных событий"""
        for event_data in events_data:
            first_bkmkr_name = event_data[0]['bookmaker']
            second_bkmkr_name = event_data[1]['bookmaker']
            if not self.started_threads.get(first_bkmkr_name) or not self.started_threads.get(second_bkmkr_name):
                continue

            if BrowserControl.bet_params and \
                    self.started_threads[first_bkmkr_name]['control_instance'].preloaded and \
                    self.started_threads[second_bkmkr_name]['control_instance'].preloaded:
                first_thread_pause_event = self.started_threads[first_bkmkr_name]['thread_pause_event']
                second_thread_pause_event = self.started_threads[second_bkmkr_name]['thread_pause_event']
                first_thread_pause_event.set()
                second_thread_pause_event.set()

            return

    def close_browsers(self) -> None:
        """Закрытие браузеров"""
        if self.__survey_threads_status():
            for bkmkr_name in self.started_threads.keys():
                control_instance = self.started_threads[bkmkr_name]['control_instance']
                control_instance.close_request = True
                thread_pause_event = self.started_threads[bkmkr_name]['thread_pause_event']
                thread_pause_event.set()
            if not self.timer.isActive():
                self.timer.setInterval(500)
                self.timer.timeout.connect(self.__survey_threads_status)
                self.timer.start()
        # else:
        #     self.finish_signal.emit()

    def __survey_threads_status(self) -> bool:
        """Опрос сотояний потоков управления сайтами букмекеров, True - в работе, False - завершены/не запущены"""
        threads_in_work = False
        for bkmkr_name in self.started_threads.keys():
            control_thread = self.started_threads[bkmkr_name]['control_thread']
            threads_in_work = threads_in_work or control_thread.is_alive()

        if not threads_in_work:
            self.finish_signal.emit()
        return threads_in_work

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

