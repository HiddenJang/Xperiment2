from datetime import datetime
import logging
from time import sleep
import selenium
from PyQt5 import QtCore
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ... import settings
from ...telegram_message_service import TelegramService

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.olimp')


class SiteInteraction:
    """Класс управления сайтом букмекера"""

    def __init__(self,
                 driver: selenium.webdriver,
                 diag_signal: QtCore.pyqtSignal,
                 common_auth_data: dict):
        self.driver = driver
        self.common_auth_data = common_auth_data
        self.diag_signal = diag_signal

        self.bookmaker = self.common_auth_data['bkmkr_name']
        self.start_balance = '0'

    def __get_screenshot(self) -> None:
        """Скриншот и отправка скриншота в telegram"""
        screenshot_name = settings.SCREENSHOTS_DIR / f"{self.bookmaker}-{str(datetime.now()).replace(':', '-')}.png"
        self.driver.get_screenshot_as_file(screenshot_name)
        TelegramService.send_photo(screenshot_name)

    def __send_diag_message(self, message: str, ex: BaseException = '') -> None:
        """Отправка диагностики"""
        logger.info(f'{message} {str(ex)}')
        TelegramService.send_text(message)
        self.diag_signal.emit(message)

    def __close_coupon(self) -> None:
        """Закрытие купона ставки"""
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(By.XPATH, '//button[text()="Очистить"]').click()
            self.driver.find_element(By.XPATH, '//button[text()="Удалить"]').click()
            self.driver.implicitly_wait(0)
            self.__send_diag_message(f'Купон {self.bookmaker} от ставки закрыт')
        except BaseException as ex:
            self.__send_diag_message(
                f'Не удалось закрытие купона {self.bookmaker} (возможно купоны отсутствуют или были закрыты ранее)', ex)

    def preload(self) -> bool | Exception:
        """Авторизация пользователя"""
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']
        # нажатие кнопки ВХОД
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'signIn')]"))).click()
        # ввод ЛОГИНА
        element = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel']")))
        element.click()
        element.send_keys(login)
        # ввод ПАРОЛЯ
        element = self.driver.find_element(By.XPATH, "//input[@type='password']")
        element.click()
        element.send_keys(password)
        # нажатие кнопки ВОЙТИ после ввода логина и пароля
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # проверка завершения авторизации
        balance = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(@title, 'Пополнить баланс')]")))
        balance = balance.text
        if not float(balance) >= 0:
            raise Exception
        else:
            return True

    def prepare_for_bet(self, event_data: dict, bet_params: dict) -> bool | None:
        """Размещение ставки"""
        sleep(5)
        self.start_balance = '100'
        return True

    def last_test(self, bet_params: dict) -> bool | None:
        """Проведение последних коротких проверок перед совершением ставки"""
        sleep(1)
        return True

    def bet(self, bet_params: dict) -> bool | None:
        """Размещение ставки"""
        return True
