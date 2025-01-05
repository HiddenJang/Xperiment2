import logging
import time
import selenium
from PyQt5 import QtCore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.olimp')


def preload(driver: selenium.webdriver, login: str, password: str):
    """Авторизация пользователя"""
    # нажатие кнопки ВХОД
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'signIn')]"))).click()
    # ввод ЛОГИНА
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel']")))
    element.click()
    element.send_keys(login)
    # ввод ПАРОЛЯ
    element = driver.find_element(By.XPATH, "//input[@type='password']")
    element.click()
    element.send_keys(password)
    # нажатие кнопки ВОЙТИ после ввода логина и пароля
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # проверка завершения авторизации
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'balanceButton')]")))


def prepare_for_bet(driver: selenium.webdriver,
        diag_signal: QtCore.pyqtSignal,
        bookmaker: str,
        url: str,
        bet_size: str,
        total_nominal: str,
        total_koeff_type: str,
        total_koeff: str) -> str | None:
    """Размещение ставки"""
    time.sleep(5)
    balance = '100'
    return balance


def last_test(driver: selenium.webdriver,
              diag_signal: QtCore.pyqtSignal,
              bookmaker: str,
              total_koeff: str) -> bool | None:
    """Проведение последних коротких проверок перед совершением ставки"""
    time.sleep(1)
    return True

def bet(driver: selenium.webdriver,
        diag_signal: QtCore.pyqtSignal,
        bookmaker: str,
        start_balance: str,
        imitation: bool) -> bool | None:
    """Размещение ставки"""
    return True
