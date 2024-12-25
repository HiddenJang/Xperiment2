import logging
import threading
from time import sleep

from PyQt5 import QtCore
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .. import webdriver
from ... import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.betboom')


class Control:

    def __init__(self, common_auth_data: dict,
                 thread_pause_event: threading.Event,
                 diag_signal: QtCore.pyqtSignal):
        self.common_auth_data = common_auth_data
        self.thread_pause_event = thread_pause_event
        self.diag_signal = diag_signal

        self.preloaded = False
        self.close_request = False

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""
        driver_dict = webdriver.Driver(settings.BOOKMAKERS.get(self.common_auth_data['bkmkr_name'])).get_driver()
        self.driver = driver_dict['driver']
        if not self.driver:
            logger.error(f"Сайт {self.common_auth_data['bkmkr_name']} {driver_dict['status']}")
            self.diag_signal.emit(f"Сайт {self.common_auth_data['bkmkr_name']} {driver_dict['status']}")
            return
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']

        for n in range(5):
            try:
                self.driver.switch_to.default_content()
                element3 = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, f'//button[contains(text(), "Вход")]')))
                element3.click()
                break
            except BaseException as ex:
                if n == 4:
                    self.__quit(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    return

        for n in range(5):
            try:
                element4 = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel']")))
                element5 = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
                element4.click()
                element4.send_keys(login)
                element5.send_keys(password)
                element6 = self.driver.find_element(By.XPATH, "//button[@type='submit']")  # [contains(text(), 'Войти']
                element6.click()
                break
            except Exception as ex:
                if n == 4:
                    self.__quit(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    return

        self.preloaded = True
        self.diag_signal.emit(f'Сайт {self.common_auth_data["bkmkr_name"]} загружен, авторизация пройдена успешно')
        logger.info(f'Сайт {self.common_auth_data["bkmkr_name"]} загружен, авторизация пройдена успешно')

        self.thread_pause_event.wait()
        if self.close_request:
            self.__quit(f'Сайт {self.common_auth_data["bkmkr_name"]} закрыт')
            return

    def __quit(self, diag_mess: str) -> None:
        """Завершение работы"""
        self.driver.close()
        self.driver.quit()
        logger.error(diag_mess)
        self.diag_signal.emit(diag_mess)
