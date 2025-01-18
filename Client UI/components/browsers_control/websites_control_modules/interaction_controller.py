import logging
import threading
from importlib import import_module

from PyQt5 import QtCore
from selenium.common import TimeoutException

from .. import webdriver
from ... import settings
from ...telegram import TelegramService

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.interaction_controller')


class WebsiteController:
    excluded_urls = []
    page_load_timeout = 5

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
        self.placed_bet_data = {}

        self.event_data = {}
        self.bet_params = {}

    def preload_and_authorize(self):
        """Открытие страницы БК и авторизация пользователя"""
        driver_dict = webdriver.Driver.get_driver(settings.BOOKMAKERS.get(self.bookmaker),
                                                  page_load_timout=self.page_load_timeout)
        self.driver = driver_dict['driver']
        if not self.driver:
            self.__send_diag_message(f"Сайт {self.bookmaker} {driver_dict['status']}",
                                     ex=driver_dict['ex'],
                                     status='error',
                                     send_telegram=False)
            return

        self.site_interaction_instance = self.SiteInteractionClass(self.driver, self.diag_signal, self.bookmaker)
        try:
            self.preloaded = self.site_interaction_instance.preload(self.common_auth_data)
            self.__send_diag_message(f'Сайт {self.bookmaker} загружен, авторизация пройдена успешно')
        except BaseException as ex:
            self.__send_diag_message(f'Ошибка авторизации {self.bookmaker}', ex=ex, send_telegram=False)
            self.__quit()
            return

        while True:
            self.thread_pause_event.wait()
            self.thread_bet_event.clear()
            self.thread_last_test_event.clear()
            self.prepared_for_bet = False
            self.stop_betting = False
            self.placed_bet_data = {}

            if self.close_request:
                self.__quit()
                return

            self.__prepare_website()

    def __prepare_website(self) -> None:
        """Запуск подготовки сайта букмекера к размещению ставки"""
        self.__send_diag_message(f"Запущен процесс размещения ставки {self.bookmaker}")

        try:
            self.driver.get(url=self.event_data.get("url"))
        except TimeoutException:
            self.__send_diag_message(f'Превышение времени ожидания открытия страницы события {self.bookmaker}. Попытка продолжить', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось открыть url {self.bookmaker}:{self.event_data.get("url")}', ex=ex)
            self.thread_pause_event.clear()
            return

        self.prepared_for_bet = self.site_interaction_instance.prepare_for_bet(self.event_data, self.bet_params)

        if self.prepared_for_bet:
            self.__send_diag_message(f"Получена готовность {self.bookmaker} к ставке", send_telegram=False)
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
            self.__run_last_tests()
        else:
            self.__send_diag_message(f"Процесс размещения ставки {self.bookmaker} окончен неудачно. Нет готовности к размещению ставки")
            self.thread_pause_event.clear()
            return

    def __run_last_tests(self) -> None:
        """Запуск последних коротких проверок перед совершением ставки"""
        self.__send_diag_message(f"Получена готовность обоих букмекеров к ставке. Запущены последние короткие тесты {self.bookmaker}", send_telegram=False)
        self.last_test_completed = self.site_interaction_instance.last_test(self.bet_params)

        if self.last_test_completed:
            self.__send_diag_message(f"Последние короткие тесты {self.bookmaker} проведены успешно", send_telegram=False)
            # ожидание результатов последней короткой проверки второго букмекера
            self.thread_last_test_event.wait()

            if self.close_request:
                self.__quit()
                return
            elif self.stop_betting:
                self.__send_diag_message(f"Процесс размещения ставки {self.bookmaker} прерван. Нет общей готовности обоих букмекеров после проведения последней короткой проверки")
                self.thread_pause_event.clear()
                return
            self.__place_bet()
        else:
            self.__send_diag_message(f"Процесс размещения ставки прерван. Нет готовности {self.bookmaker} к размещению ставки после проведения последней короткой проверки")
            self.thread_pause_event.clear()
            return

    def __place_bet(self) -> None:
        """Размещение ставки"""
        self.__send_diag_message(f"Последние короткие тесты обоих букмекеров проведены успешно", send_telegram=False)
        bet_placed = self.site_interaction_instance.bet(self.bet_params)

        if bet_placed['result']:
            self.__send_diag_message(f"Процесс размещения завершен. Ставка {self.bookmaker} размещена успешно за {bet_placed['bet_data_for_stats']['betting_time']}")
        else:
            self.__send_diag_message(f"Процесс размещения завершен. Ставка {self.bookmaker} не размещена, либо результат неизвестен")

        self.placed_bet_data = bet_placed['bet_data_for_stats']
        WebsiteController.excluded_urls.append(self.event_data.get("url"))
        self.thread_pause_event.clear()

    def __send_diag_message(self,
                            diag_mess: str,
                            ex: BaseException = '',
                            status: str = 'info',
                            send_telegram: bool = True) -> None:
        """Отправка диагностических сообщений в логгер и приложение"""
        log_info = f'{diag_mess} {str(ex)}'
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
        if send_telegram:
            TelegramService.send_text(diag_mess)

    def __quit(self) -> None:
        """Завершение работы"""
        self.thread_pause_event.clear()
        try:
            self.driver.close()
            self.driver.quit()
            self.__send_diag_message(f'Сайт {self.bookmaker} закрыт')
        except BaseException:
            pass


class ResultExtractor:

    def __init__(self, event_data: list, diag_signal: QtCore.pyqtSignal):
        self.event_data = event_data
        self.diag_signal = diag_signal

    def extract_data(self) -> dict | None:
        for bkmkr_data in self.event_data:
            bookmaker = bkmkr_data["bookmaker"]
            site_interaction_module = import_module(
                f'.browsers_control.websites_control_modules.{bookmaker}',
                package='components')
            SiteInteractionClass = getattr(site_interaction_module, 'SiteInteraction')

            driver_dict = webdriver.Driver.get_driver(settings.BOOKMAKERS.get(bookmaker))
            driver = driver_dict['driver']
            if not driver:
                self.__send_diag_message(f"Сайт {bookmaker} {driver_dict['status']}",
                                         ex=driver_dict['ex'],
                                         status='error')
                continue
            site_interaction_instance = SiteInteractionClass(driver, self.diag_signal, bookmaker)
            event_result = site_interaction_instance.extract_event_result(bkmkr_data)
            driver.close()
            driver.quit()
            if event_result and event_result.get('result'):
                return event_result

    def __send_diag_message(self,
                            diag_mess: str,
                            ex: BaseException = '',
                            status: str = 'info',
                            send_telegram: bool = True) -> None:
        """Отправка диагностических сообщений в логгер и приложение"""
        log_info = f'{diag_mess} {str(ex)}'
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
        if send_telegram:
            TelegramService.send_text(diag_mess)