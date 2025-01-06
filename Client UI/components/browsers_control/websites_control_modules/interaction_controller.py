import logging
import threading
from importlib import import_module
from PyQt5 import QtCore
from selenium.common import TimeoutException

from .. import webdriver
from ... import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.interaction_controller')


class WebsiteController:
    excluded_urls = []

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

        site_interaction_module = import_module(
            f'.browsers_control.websites_control_modules.{self.common_auth_data["bkmkr_name"]}',
            package='components')
        self.SiteInteractionClass = getattr(site_interaction_module, 'SiteInteraction')

        self.bookmaker = self.common_auth_data['bkmkr_name']
        self.preloaded = False
        self.close_request = False
        self.prepared_for_bet = False
        self.last_test_completed = False
        self.stop_betting = False

        self.event_data = {}
        self.bet_params = {}

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""
        driver_dict = webdriver.Driver(settings.BOOKMAKERS.get(self.bookmaker)).get_driver()
        self.driver = driver_dict['driver']
        if not self.driver:
            self.__send_diag_message(f"Сайт {self.bookmaker} {driver_dict['status']}",
                                     exception=driver_dict['ex'],
                                     status='error')
            return

        self.site_interaction_instance = self.SiteInteractionClass(self.driver, self.diag_signal, self.common_auth_data)
        try:
            self.preloaded = self.site_interaction_instance.preload()
            self.__send_diag_message(f'Сайт {self.bookmaker} загружен, авторизация пройдена успешно')
        except BaseException as ex:
            self.__send_diag_message(f'Ошибка авторизации {self.bookmaker}', exception=ex)
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
        self.__send_diag_message(f"Запущен процесс размещения ставки {self.bookmaker}")
        try:
            print(self.event_data)
            url = self.event_data["url"]
            try:
                self.driver.get(url=url)
            except TimeoutException:
                self.__send_diag_message(f'Превышение времени ожидания открытия страницы события {self.bookmaker}. Попытка продолжить')
            except BaseException as ex:
                self.__send_diag_message(f'Не удалось открыть url {self.bookmaker}: {url}', exception=ex)
                self.thread_pause_event.clear()
                return

            self.prepared_for_bet = self.site_interaction_instance.prepare_for_bet(self.event_data, self.bet_params)

            if self.prepared_for_bet:
                self.__send_diag_message(f"Получена готовность {self.bookmaker} к ставке")
                # ожидание готовности обоих букмекеров
                self.thread_bet_event.wait()

                if self.close_request:
                    self.__quit()
                    return
                elif self.stop_betting:
                    self.__send_diag_message(
                        f"Процесс размещения ставки {self.bookmaker} прерван. Нет готовности второго букмекера")
                    self.thread_pause_event.clear()
                    return
                self.__send_diag_message(f"Получена готовность обоих букмекеров к ставке. Запущены последние короткие тесты {self.bookmaker}")

                self.last_test_completed = self.site_interaction_instance.last_test(self.bet_params)
                if self.last_test_completed:
                    # ожидание результатов последней короткой проверки
                    self.thread_last_test_event.wait()
                    if self.close_request:
                        self.__quit()
                        return
                    elif self.stop_betting:
                        self.__send_diag_message(
                            f"Процесс размещения ставки {self.bookmaker} прерван. Нет общей готовности обоих букмекеров после проведения последней короткой проверки")
                        self.thread_pause_event.clear()
                        return

                    bet_placed = self.site_interaction_instance.bet(self.bet_params)
                    if bet_placed:
                        self.__send_diag_message(f"Ставка {self.bookmaker} размещена успешно")
                        WebsiteController.excluded_urls.append(url)
                    else:
                        self.__send_diag_message(f"Ставка {self.bookmaker} не размещена, либо результат неизвестен")
                else:
                    self.__send_diag_message(
                        f"Процесс размещения ставки {self.bookmaker} окончен неудачно. Не пройдены последние короткие проверки")
                    self.thread_pause_event.clear()
                    return
            else:
                self.__send_diag_message(f"Процесс размещения ставки {self.bookmaker} окончен неудачно. Нет готовности к размещению ставки")
                self.thread_pause_event.clear()
                return

        except BaseException as ex:
            self.__send_diag_message(f"Процесс размещения ставки {self.bookmaker} окончен неудачно",
                                     exception=ex)
            self.thread_pause_event.clear()
            return
        self.__send_diag_message(f"Процесс размещения ставки {self.bookmaker} завершен")
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
            self.__send_diag_message(f'Сайт {self.bookmaker} закрыт')
        except BaseException:
            pass
