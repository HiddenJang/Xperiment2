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

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.leon')


class Control:
    preloaded = False
    close_request = False

    def __init__(self, common_auth_data: dict,
                 thread_event: threading.Event,
                 diag_signal: QtCore.pyqtSignal,
                 status_signal: QtCore.pyqtSignal):
        self.common_auth_data = common_auth_data
        self.thread_event = thread_event
        self.diag_signal = diag_signal
        self.status_signal = status_signal

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""

        driver = webdriver.Driver(settings.BOOKMAKERS.get(self.common_auth_data['bkmkr_name'])).get_driver()
        driver = driver['driver']
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']

        for n in range(5):
            try:
                element3 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='/login']")))
                element3.click()
                element4 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'E-mail')]")))
                element4.click()
                element5 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='login']")))
                element6 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
                element5.clear()
                element6.clear()
                element5.send_keys(login)
                element6.send_keys(password)
                element7 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'login__button')]")))
                element7.click()
                break
            except BaseException as ex:
                if n == 4:
                    logger.error(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    self.diag_signal.emit(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    driver.close()
                    driver.quit()
                    return
                continue

        Control.preloaded = True
        self.diag_signal.emit(f'Сайт {self.common_auth_data["bkmkr_name"]} загружен, авторизация пройдена успешно')
        self.thread_event.wait()
        if Control.close_request:
            driver.close()
            driver.quit()
            self.diag_signal.emit(f'Сайт {self.common_auth_data["bkmkr_name"]} закрыт')
            return