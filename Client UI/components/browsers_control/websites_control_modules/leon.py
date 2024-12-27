import logging
import time
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.leon')


def preload(driver: selenium.webdriver, login: str, password: str) -> None:
    """Авторизация пользователя"""
    # нажатие кнопки ВОЙТИ
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/login']"))).click()
    # нажатие вкладки EMAIL
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'E-mail')]"))).click()
    # очитска полей ЛОШИН и ПАРОЛЬ и ввод данных авторизации
    element1 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='login']")))
    element2 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    element1.clear()
    element2.clear()
    element1.send_keys(login)
    element2.send_keys(password)
    # нажатие кнопки ВОЙТИ в окне авторизации
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'login__button')]"))).click()


def bet(driver: selenium.webdriver,
        url: str,
        bet_size: str,
        total_nominal: str,
        total_koeff_type: str,
        total_koeff: str) -> None:
    """Размещение ставки"""
    time.sleep(10)



