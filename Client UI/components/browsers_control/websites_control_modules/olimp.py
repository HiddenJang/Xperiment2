import logging
import threading
import time
from PyQt5 import QtCore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .. import webdriver
from ... import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.olimp')


class Control:

    def __init__(self, common_auth_data: dict,
                 thread_pause_event: threading.Event,
                 diag_signal: QtCore.pyqtSignal):
        self.common_auth_data = common_auth_data
        self.thread_pause_event = thread_pause_event
        self.diag_signal = diag_signal

        self.preloaded = False
        self.close_request = False
        self.event_data = {}
        self.bet_params = {}

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""
        driver_dict = webdriver.Driver(settings.BOOKMAKERS.get(self.common_auth_data['bkmkr_name'])).get_driver()
        self.driver = driver_dict['driver']
        if not self.driver:
            self.__send_diag_message(f"Сайт {self.common_auth_data['bkmkr_name']} {driver_dict['status']}", 'error')
            return
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']

        try:
            # нажатие кнопки ВХОД
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'signIn')]"))).click()
            # ввод ЛОГИНА
            element = self.driver.find_element(By.XPATH, "//input[@type='tel']")
            element.click()
            element.send_keys(login)
            # ввод ПАРОЛЯ
            element = self.driver.find_element(By.XPATH, "//input[@type='password']")
            element.click()
            element.send_keys(password)
            # нажатие кнопки ВОЙТИ после ввода логина и пароля
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        except BaseException as ex:
            self.__quit(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
            return

        self.preloaded = True
        self.__send_diag_message(f'Сайт {self.common_auth_data["bkmkr_name"]} загружен, авторизация пройдена успешно')

        while True:
            self.thread_pause_event.wait()
            if self.close_request:
                self.__quit(f'Сайт {self.common_auth_data["bkmkr_name"]} закрыт')
                return
            self.bet()

    def bet(self) -> None:
        """Размещение ставки"""
        self.__send_diag_message(f"Запущен процесс размещения ставки {self.common_auth_data['bkmkr_name']}")
        time.sleep(10)
        self.__send_diag_message(f"Закончен процесс размещения ставки {self.common_auth_data['bkmkr_name']}")


    def __send_diag_message(self, diag_mess: str, status: str='info') -> None:
        """Отправка диагностических сообщений в логгер и приложение"""
        match status:
            case 'debug':
                logger.debug(diag_mess)
            case 'info':
                logger.info(diag_mess)
            case "warning":
                logger.warning(diag_mess)
            case "error":
                logger.error(diag_mess)
            case "critical":
                logger.critical(diag_mess)
        self.diag_signal.emit(diag_mess)

    def __quit(self, diag_mess: str) -> None:
        """Завершение работы"""
        try:
            self.driver.close()
            self.driver.quit()
        except BaseException:
            pass
        logger.error(diag_mess)
        self.diag_signal.emit(diag_mess)
