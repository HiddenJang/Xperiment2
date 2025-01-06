import logging
import threading
from importlib import import_module
from PyQt5 import QtCore
from PyQt5.QtCore import QObject

from .. import settings
from .websites_control_modules.interaction_controller import WebsiteController


logger = logging.getLogger('Client UI.components.browsers_control.core')


class BrowserControl(QObject):
    diag_signal = QtCore.pyqtSignal(str)
    finish_signal = QtCore.pyqtSignal()
    close_all_signal = QtCore.pyqtSignal()
    bet_params = {}

    def __init__(self, control_settings: dict):
        super(BrowserControl, self).__init__()
        self.control_settings = control_settings
        self.started_threads = {}
        self.bet_in_progress = False
        self.threads_status_timer = QtCore.QTimer()
        self.betting_status_timer = QtCore.QTimer()
        self.bet_prohibitions_timer = QtCore.QTimer()
        self.bet_preparing_interval_timer = QtCore.QTimer()
        self.last_test_timer = QtCore.QTimer()

    def preload_sites_and_authorize(self):
        """Запуск потоков загрузки браузеров и авторизации на сайтах БК"""
        interaction_modules = self.__get_site_interaction_modules()
        auth_data = self.control_settings["auth_data"]

        for bkmkr_name in auth_data.keys():
            if not (auth_data[bkmkr_name]['login'] and auth_data[bkmkr_name]['password']):
                try:
                    del interaction_modules[bkmkr_name]
                except BaseException:
                    continue

        for bkmkr_name in interaction_modules.keys():
            if auth_data.get(bkmkr_name):
                interaction_module = interaction_modules[bkmkr_name]
                thread_pause_event = threading.Event()
                thread_last_test_event = threading.Event()
                thread_bet_event = threading.Event()
                website_controller = WebsiteController({'bkmkr_name': bkmkr_name, 'auth_data': auth_data[bkmkr_name]},
                                                       thread_pause_event,
                                                       thread_last_test_event,
                                                       thread_bet_event,
                                                       self.diag_signal)
                control_thread = threading.Thread(target=website_controller.preload, daemon=True)
                control_thread.start()
                self.started_threads[bkmkr_name] = {'interaction_module': interaction_module,
                                                    'controller_instance': website_controller,
                                                    'control_thread': control_thread,
                                                    'thread_pause_event': thread_pause_event,
                                                    'thread_last_test_event': thread_last_test_event,
                                                    'thread_bet_event': thread_bet_event}
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
            first_bkmkr_url = event_data[0]['url']
            second_bkmkr_name = event_data[1]['bookmaker']
            second_bkmkr_url = event_data[1]['url']

            if first_bkmkr_url in WebsiteController.excluded_urls or second_bkmkr_url in WebsiteController.excluded_urls:
                continue

            if self.started_threads.get(first_bkmkr_name) and \
                    self.started_threads.get(second_bkmkr_name) and \
                    BrowserControl.bet_params and \
                    self.started_threads[first_bkmkr_name]['controller_instance'].preloaded and \
                    self.started_threads[second_bkmkr_name]['controller_instance'].preloaded:
                self.started_threads[first_bkmkr_name]['controller_instance'].bet_params = BrowserControl.bet_params
                self.started_threads[first_bkmkr_name]['controller_instance'].event_data = event_data[0]

                self.started_threads[second_bkmkr_name]['controller_instance'].bet_params = BrowserControl.bet_params
                self.started_threads[second_bkmkr_name]['controller_instance'].event_data = event_data[1]

                first_thread_pause_event = self.started_threads[first_bkmkr_name]['thread_pause_event']
                second_thread_pause_event = self.started_threads[second_bkmkr_name]['thread_pause_event']

                first_thread_pause_event.set()
                second_thread_pause_event.set()
                self.bet_in_progress = True

                if not self.betting_status_timer.isActive():
                    self.betting_status_timer.setInterval(1000)
                    self.betting_status_timer.timeout.connect(lambda: self.__survey_betting_status(first_bkmkr_name, second_bkmkr_name))
                    self.betting_status_timer.start()

                if not self.bet_prohibitions_timer.isActive():
                    self.bet_prohibitions_timer.setInterval(500)
                    self.bet_prohibitions_timer.timeout.connect(lambda: self.__survey_bet_prohibitions_status(first_bkmkr_name, second_bkmkr_name))
                    self.bet_prohibitions_timer.start()
                return

    def __survey_betting_status(self, first_bkmkr_name: str, second_bkmkr_name: str) -> None:
        """Опрос состояний потоков размещения ставок,
                True - в работе, False - завершены/не запущены"""
        first_bkmkr_thread = self.started_threads[first_bkmkr_name]['control_thread']
        second_bkmkr_thread = self.started_threads[second_bkmkr_name]['control_thread']
        if not first_bkmkr_thread.is_alive() or not second_bkmkr_thread.is_alive():
            self.close_all_signal.emit()
            return

        first_bkmkr_thread_pause_event = self.started_threads[first_bkmkr_name]['thread_pause_event']
        second_bkmkr_thread_pause_event = self.started_threads[second_bkmkr_name]['thread_pause_event']
        if not first_bkmkr_thread_pause_event.is_set() and not second_bkmkr_thread_pause_event.is_set():
            self.bet_in_progress = False
            if self.bet_prohibitions_timer.isActive():
                self.bet_prohibitions_timer.stop()

    def __survey_bet_prohibitions_status(self, first_bkmkr_name: str, second_bkmkr_name: str) -> None:
        """Опрос готовностей к размещению ставок"""
        first_prepared_for_bet = self.started_threads[first_bkmkr_name]['controller_instance'].prepared_for_bet
        second_prepared_for_bet = self.started_threads[second_bkmkr_name]['controller_instance'].prepared_for_bet

        first_last_test_completed = self.started_threads[first_bkmkr_name]['controller_instance'].last_test_completed
        second_last_test_completed = self.started_threads[second_bkmkr_name]['controller_instance'].last_test_completed

        if first_prepared_for_bet and second_prepared_for_bet:
            first_thread_bet_event = self.started_threads[first_bkmkr_name]['thread_bet_event']
            second_thread_bet_event = self.started_threads[second_bkmkr_name]['thread_bet_event']
            first_thread_bet_event.set()
            second_thread_bet_event.set()

            if not self.last_test_timer.isActive():
                self.last_test_timer.setInterval(3000)
                self.last_test_timer.timeout.connect(lambda: self.__stop_betting(first_bkmkr_name, second_bkmkr_name))
                self.last_test_timer.start()

            if first_last_test_completed and second_last_test_completed:
                first_thread_last_test_event = self.started_threads[first_bkmkr_name]['thread_last_test_event']
                second_thread_last_test_event = self.started_threads[second_bkmkr_name]['thread_last_test_event']
                first_thread_last_test_event.set()
                second_thread_last_test_event.set()

        elif first_prepared_for_bet or second_prepared_for_bet:
            if not self.bet_preparing_interval_timer.isActive():
                self.bet_preparing_interval_timer.setInterval(10000)
                self.bet_preparing_interval_timer.timeout.connect(lambda: self.__stop_betting(first_bkmkr_name, second_bkmkr_name))
                self.bet_preparing_interval_timer.start()

        elif self.bet_preparing_interval_timer.isActive():
            self.bet_preparing_interval_timer.stop()
            if self.last_test_timer.isActive():
                self.last_test_timer.stop()

    def __stop_betting(self, first_bkmkr_name: str, second_bkmkr_name: str):
        """Прерывание процесса размещения ставки при отсутствии готовности одного из букмекеров"""
        self.started_threads[first_bkmkr_name]['controller_instance'].stop_betting = True
        self.started_threads[second_bkmkr_name]['controller_instance'].stop_betting = True

        first_thread_bet_event = self.started_threads[first_bkmkr_name]['thread_bet_event']
        second_thread_bet_event = self.started_threads[second_bkmkr_name]['thread_bet_event']
        first_thread_bet_event.set()
        second_thread_bet_event.set()

        first_thread_last_test_event = self.started_threads[first_bkmkr_name]['thread_last_test_event']
        second_thread_last_test_event = self.started_threads[second_bkmkr_name]['thread_last_test_event']
        first_thread_last_test_event.set()
        second_thread_last_test_event.set()

    def close_browsers(self) -> None:
        """Закрытие браузеров"""
        if self.__survey_threads_status():
            for bkmkr_name in self.started_threads.keys():
                controller_instance = self.started_threads[bkmkr_name]['controller_instance']
                controller_instance.close_request = True
                thread_pause_event = self.started_threads[bkmkr_name]['thread_pause_event']
                thread_pause_event.set()
                thread_bet_event = self.started_threads[bkmkr_name]['thread_bet_event']
                thread_bet_event.set()

            if self.bet_preparing_interval_timer.isActive():
                self.bet_preparing_interval_timer.stop()
            if self.bet_prohibitions_timer.isActive():
                self.bet_prohibitions_timer.stop()
            if self.betting_status_timer.isActive():
                self.betting_status_timer.stop()

            if not self.threads_status_timer.isActive():
                self.threads_status_timer.setInterval(500)
                self.threads_status_timer.timeout.connect(self.__survey_threads_status)
                self.threads_status_timer.start()

    def __survey_threads_status(self) -> bool:
        """Опрос сотояний потоков управления сайтами букмекеров,
        True - в работе, False - завершены/не запущены"""
        threads_in_work = False
        for bkmkr_name in self.started_threads.keys():
            control_thread = self.started_threads[bkmkr_name]['control_thread']
            threads_in_work = threads_in_work or control_thread.is_alive()

        if not threads_in_work:
            self.finish_signal.emit()
        return threads_in_work

    @staticmethod
    def __get_site_interaction_modules() -> dict:
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

