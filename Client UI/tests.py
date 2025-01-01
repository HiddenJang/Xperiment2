import os
from time import sleep
from datetime import datetime
import logging
from logging import handlers
from pathlib import Path

import selenium
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

def init_logger(name):
    """Инициализация логгера"""
    LOGLEVEL = logging.INFO
    FORMAT = "%(asctime)s -- %(name)s -- %(lineno)s -- %(levelname)s -- %(message)s"
    LOGS_PATH = BASE_DIR / "logs"
    FILENAME = LOGS_PATH / "gui_logs.log"

    logger = logging.getLogger(name)
    logger.setLevel(LOGLEVEL)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(LOGLEVEL)

    fh = handlers.RotatingFileHandler(
        filename=FILENAME,
        encoding="UTF-8",
        maxBytes=300000,
        backupCount=5,
    )
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(LOGLEVEL)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')


init_logger('test')
logger = logging.getLogger('test.leon')


def start():
    driver_dict = Driver('https://leon.ru/').get_driver()
    driver = driver_dict['driver']

    url = 'https://leon.ru/bets/soccer/russia/russia-cup/1970324845269340-akron-togliatti-fc-spartak-moscow'
    bookmaker = 'leon'
    bet_size = '20'
    total_nominal = '2.5'
    total_koeff_type = 'Больше'
    total_koeff = '1.6'


    preload(driver, login, password)
    bet(driver, bookmaker, url, bet_size, total_nominal, total_koeff_type, total_koeff)

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
    sleep(3)

def bet(driver: selenium.webdriver,
        bookmaker: str,
        url: str,
        bet_size: str,
        total_nominal: str,
        total_koeff_type: str,
        total_koeff: str) -> None:
    """Размещение ставки"""

    def close_coupon(webdriver: selenium.webdriver) -> None:
        """Закрытие купона ставки"""

        try:
            WebDriverWait(webdriver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Очистить"]'))).click()
            WebDriverWait(webdriver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Удалить"]'))).click()
            message = f'Купон {bookmaker} от ставки закрыт'
            logger.info(f'{message}')
        except BaseException as ex:
            message = f'Не удалось закрытие купона {bookmaker} (возможно купоны отсутствуют или были закрыты ранее)'
            logger.info(f'{message} {ex}')

    driver.get(url=url)
    # закрытие купона тотала, если он остался от предыдущей ставки
    close_coupon(driver)
    # проверка достаточности баланса
    try:
        driver.implicitly_wait(10)
        element = driver.find_element(By.XPATH, '//div[contains(@class, "balance__text")]')
        balance = element.text.split(',')[0]
        if float(balance) < float(bet_size):
            message = f'Ставка на событие {bookmaker} {url} не будет сделана, баланс меньше размера ставки'
            logger.info(message)
            return
    except BaseException as ex:
        message = f'Не удалось получить баланс {bookmaker}. Ставка не будет сделана'
        logger.info(f'{message}: {ex}')
        return

    # попытка нажать вкладку ТОТАЛЫ
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Тоталы']"))).click()
    except BaseException as ex:
        message = f'Попытка открыть вкладку "Тоталы" букмекера {bookmaker} неудачна'
        logger.info(f'{message}: {ex}')

        # попытка закрыть всплывающее окно уведомления
        driver.implicitly_wait(0)
        driver.find_element(By.XPATH, "//button[text()='Позже']").click()
        driver.find_element(By.XPATH, "//button[text()='Тоталы']").click()
    except:
        message = f'Попытка закрыть всплывающее окно {bookmaker} для открытия вкладки Тоталы неудачна. Ставка не будет сделана'
        logger.info(message)
        return

    # попытка нажать на кнопку с нужным тоталом (открыть купон тотала)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total_nominal}')]"))).click()
        logger.info('Тотал успешно найден, кнопка нажата')
    except BaseException as ex:
        message = f'Попытка нажать на кнопку с нужным тоталом (открыть купон тотала) букмекера {bookmaker} неудачна'
        logger.info(f'{message}: {ex}')

        # попытка закрыть всплывающее окно уведомления
        driver.find_element(By.XPATH, "//button[contains(text(),'Позже')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total_nominal}')]"))).click()
    except:
        message = f'Попытка закрыть всплывающее окно {bookmaker} для открытия купона Тотала неудачна. Ставка не будет сделана'
        logger.info(message)
        return

    # беттинг
    # if Preload.betting_on:  # если автоматический беттинг разрешен пробуем поставить
    # ввод значения ставки
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@class,"stake-input__value")]')))
        element.click()
        element.send_keys(Keys.CONTROL+'A')
        element.send_keys(Keys.DELETE)
        element.send_keys(bet_size)
        if int(element.get_attribute('value')) != int(bet_size):
            raise Exception
        message = f'Значение ставки на событие {bookmaker} введено успешно'
        logger.info(message)
    except BaseException as ex:
        message = f'Не удалось ввести значение ставки на событие {bookmaker} {url}.Ставка не будет сделана'
        logger.info(f'{message}: {ex}')
        close_coupon(driver)
    sleep(10)
    driver.close()
    driver.quit()

class Driver:
    """Класс вебдрайвера для управления браузером"""

    def __init__(self, base_url):
        self.base_url = base_url

    def get_driver(self) -> dict:
        """Создание объекта вебдрайвера"""
        webdriver_file_path = BASE_DIR / "components/browsers_control/chromedriver-linux64/chromedriver"
        if not os.path.exists(webdriver_file_path):
            logger.error(f'Webdriver отсутствует в директории {webdriver_file_path}. '
                               f'Необходимо скачать webdriver Chrome')
            return {'driver': None,
                    'status': f'Webdriver отсутствует в директории {webdriver_file_path}. '
                               f'Необходимо скачать webdriver Chrome',
                    'ex': ''}
        s = Service(executable_path=str(webdriver_file_path))
        opts = Options()
        # opts.add_argument('--headless') # запуск браузера в фоне
        opts.add_argument("start-maximized")  # открыть в весь экран
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])  # устанавливаем опции для эмуляции управления прользователем (чтобы сайт не догадался)
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_experimental_option('detach', True)
        try:
            driver = webdriver.Chrome(options=opts, service=s)
            driver.get(url=self.base_url)
            return {'driver': driver, 'status': 'Webdriver успешно подключен', 'ex': ''}
        except BaseException as ex:
            logger.error(ex)
            return {'driver': None, 'status': f'Ошибка в работе webdriver', 'ex': ex}


if __name__ == '__main__':
    start()
