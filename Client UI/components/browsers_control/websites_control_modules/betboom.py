import logging
import time
import selenium
from PyQt5 import QtCore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.betboom')


def preload(driver: selenium.webdriver, login: str, password: str) -> None:
    """Авторизация пользователя"""
    driver.switch_to.default_content()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f'//button[contains(text(), "Вход")]'))).click()
    element4 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='tel']")))
    element5 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
    element4.click()
    element4.send_keys(login)
    element5.send_keys(password)
    element6 = driver.find_element(By.XPATH, "//button[@type='submit']")  # [contains(text(), 'Войти']
    element6.click()


def prepare_for_bet(driver: selenium.webdriver,
                  iag_signal: QtCore.pyqtSignal,
                  bookmaker: str,
                  url: str,
                  bet_size: str,
                  total_nominal: str,
                  total_koeff_type: str,
                  total_koeff: str) -> None:
    """Размещение ставки"""
    time.sleep(10)
    return True
