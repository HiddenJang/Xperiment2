import logging
import threading
from importlib import import_module
from PyQt5 import QtCore
from selenium.common import TimeoutException

from .. import webdriver
from ... import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.interaction_controller')


class WebsiteController:

    def __init__(self, common_auth_data: dict,
                 thread_pause_event: threading.Event,
                 thread_last_test_event: threading.Event,
                 thread_bet_event: threading.Event,
                 diag_signal: QtCore.pyqtSignal):
        self.common_auth_data = common_auth_data
        self.thread_pause_event = thread_pause_event
        self.thread_last_test_event = thread_last_test_event
        self.thread_bet_event = thread_bet_event
        self.diag_signal = diag_signal

        self.preloaded = False
        self.close_request = False
        self.event_data = {}
        self.bet_params = {}
        self.site_interaction_module = import_module(f'.browsers_control.websites_control_modules.{self.common_auth_data["bkmkr_name"]}',
                                    package='components')
        self.prepared_for_bet = False
        self.last_test_completed = False
        self.stop_betting = False

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""
        driver_dict = webdriver.Driver(settings.BOOKMAKERS.get(self.common_auth_data['bkmkr_name'])).get_driver()
        self.driver = driver_dict['driver']
        if not self.driver:
            self.__send_diag_message(f"Сайт {self.common_auth_data['bkmkr_name']} {driver_dict['status']}",
                                     exception=driver_dict['ex'],
                                     status='error')
            return
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']

        try:
            self.site_interaction_module.preload(self.driver, login, password)
            self.__send_diag_message(
                f'Сайт {self.common_auth_data["bkmkr_name"]} загружен, авторизация пройдена успешно')
            self.preloaded = True
        except BaseException as ex:
            self.__send_diag_message(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}', exception=ex)
            self.__quit()
            return

        while True:
            self.thread_bet_event.clear()
            self.thread_last_test_event.clear()
            self.prepared_for_bet = False
            self.stop_betting = False

            self.thread_pause_event.wait()
            if self.close_request:
                self.__quit()
                return
            self.bet()

    def bet(self) -> None:
        """Размещение ставки"""
        self.__send_diag_message(f"Запущен процесс размещения ставки {self.common_auth_data['bkmkr_name']}")
        try:
            print(self.event_data)
            bookmaker = self.event_data["bookmaker"]
            url = self.event_data["url"]
            bet_size = self.bet_params[self.common_auth_data['bkmkr_name']]
            total_nominal = list(self.event_data['runners'].keys())[0]
            total_koeff_type = list(self.event_data['runners'][total_nominal].keys())[0]
            total_koeff = self.event_data['runners'][total_nominal][total_koeff_type]
            imitation = self.bet_params['bet_imitation']

            try:
                self.driver.get(url=url)
            except TimeoutException:
                self.__send_diag_message(f'Превышение времени ожидания открытия страницы события {bookmaker}. Попытка продолжить')
            except BaseException as ex:
                self.__send_diag_message(f'Не удалось открыть url {bookmaker}: {url}', exception=ex)
                self.thread_pause_event.clear()
                return

            self.prepared_for_bet = self.site_interaction_module.prepare_for_bet(self.driver,
                                                                                 self.diag_signal,
                                                                                 bookmaker,
                                                                                 url,
                                                                                 bet_size,
                                                                                 total_nominal,
                                                                                 total_koeff_type,
                                                                                 total_koeff)
            if self.prepared_for_bet:
                self.__send_diag_message(f"Получена готовность {self.common_auth_data['bkmkr_name']} к ставке")
                # ожидание готовности обоих букмекеров
                self.thread_bet_event.wait()

                if self.close_request:
                    self.__quit()
                    return
                elif self.stop_betting:
                    self.__send_diag_message(
                        f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} прерван. Нет готовности второго букмекера")
                    self.thread_pause_event.clear()
                    return
                self.__send_diag_message(f"Получена готовность обоих букмекеров к ставке. Запущены последние короткие тесты {self.common_auth_data['bkmkr_name']}")

                self.last_test_completed = self.site_interaction_module.last_test(self.driver,
                                                                                  self.diag_signal,
                                                                                  bookmaker,
                                                                                  total_koeff)
                if self.last_test_completed:
                    # ожидание результатов последней короткой проверки
                    self.thread_last_test_event.wait()
                    if self.close_request:
                        self.__quit()
                        return
                    elif self.stop_betting:
                        self.__send_diag_message(
                            f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} прерван. Нет готовности одного из букмекеров после проведения последней короткой проверки")
                        self.thread_pause_event.clear()
                        return

                    bet_placed = self.site_interaction_module.bet(self.driver,
                                                                  self.diag_signal,
                                                                  bookmaker,
                                                                  self.prepared_for_bet,
                                                                  imitation)

                    if bet_placed:
                        self.__send_diag_message(f"Ставка {self.common_auth_data['bkmkr_name']} размещена успешно")
                    else:
                        self.__send_diag_message(f"Ставка {self.common_auth_data['bkmkr_name']} не размещена, либо результат неизвестен")
                else:
                    self.__send_diag_message(
                        f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} окончен неудачно. Не пройдены последние короткие проверки")
                    self.thread_pause_event.clear()
                    return
            else:
                self.__send_diag_message(f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} окончен неудачно. Нет готовности к размещению ставки")
                self.thread_pause_event.clear()
                return

        except BaseException as ex:
            self.__send_diag_message(f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} окончен неудачно",
                                     exception=ex)
            self.thread_pause_event.clear()
            return
        self.__send_diag_message(f"Процесс размещения ставки {self.common_auth_data['bkmkr_name']} завершен")
        self.thread_pause_event.clear()

    def __send_diag_message(self, diag_mess: str, exception: BaseException = '', status: str = 'info') -> None:
        """Отправка диагностических сообщений в логгер и приложение"""
        log_info = diag_mess + ' ' + str(exception)
        match status:
            case 'debug':
                logger.debug(log_info)
            case 'info':
                logger.info(log_info)
            case "warning":
                logger.warning(log_info)
            case "error":
                logger.error(log_info)
            case "critical":
                logger.critical(log_info)
        self.diag_signal.emit(diag_mess)

    def __quit(self) -> None:
        """Завершение работы"""
        self.thread_pause_event.clear()
        try:
            self.driver.close()
            self.driver.quit()
            self.__send_diag_message(f'Сайт {self.common_auth_data["bkmkr_name"]} закрыт')
        except BaseException:
            pass
