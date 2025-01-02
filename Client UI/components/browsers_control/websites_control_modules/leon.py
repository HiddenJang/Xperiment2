from datetime import datetime
import logging
import selenium
from PyQt5 import QtCore
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ... import settings
from ...telegram_message_service import TelegramService

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.leon')


def get_screenshot(driver: selenium.webdriver, bookmaker: str) -> None:
    """Скриншот и отправка скриншота в telegram"""
    screenshot_name = settings.SCREENSHOTS_DIR / f"{bookmaker}-{str(datetime.now()).replace(':', '-')}.png"
    driver.get_screenshot_as_file(screenshot_name)
    TelegramService.send_photo(screenshot_name)


def preload(driver: selenium.webdriver, login: str, password: str) -> None:
    """Авторизация пользователя"""
    # нажатие кнопки ВОЙТИ
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/login']"))).click()
    # нажатие вкладки EMAIL
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'E-mail')]"))).click()
    # очитска полей ЛОГИН и ПАРОЛЬ и ввод данных авторизации
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


def prepare_for_bet(driver: selenium.webdriver,
        diag_signal: QtCore.pyqtSignal,
        bookmaker: str,
        url: str,
        bet_size: str,
        total_nominal: str,
        total_koeff_type: str,
        total_koeff: str) -> None:
    """Размещение ставки"""

    if total_koeff_type == 'under':
        total = f'Меньше ({total_nominal})'
    else:
        total = f'Больше ({total_nominal})'

    def close_coupon() -> None:
        """Закрытие купона ставки"""
        nonlocal diag_signal, driver
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Очистить"]'))).click()
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Удалить"]'))).click()
            message = f'Купон {bookmaker} от ставки закрыт'
            logger.info(f'{message}')
        except BaseException as ex:
            message = f'Не удалось закрытие купона {bookmaker} (возможно купоны отсутствуют или были закрыты ранее)'
            logger.info(f'{message} {ex}')
        diag_signal.emit(message)

    # закрытие купона тотала, если он остался от предыдущей ставки
    close_coupon()
    # проверка достаточности баланса
    try:
        driver.implicitly_wait(10)
        element = driver.find_element(By.XPATH, '//div[contains(@class, "balance__text")]')
        balance = element.text.split(',')[0]
        if float(balance) < float(bet_size):
            message = f'Ставка на событие {bookmaker} {url} не будет сделана, баланс меньше размера ставки'
            TelegramService.send_text(message)
            logger.info(message)
            diag_signal.emit(message)
            return
    except BaseException as ex:
        message = f'Не удалось получить баланс {bookmaker}. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')
        diag_signal.emit(message)
        get_screenshot(driver, bookmaker)
        return

    # переключение на вкладку ТОТАЛЫ
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Тоталы']"))).click()
    except BaseException as ex:
        message = f'Попытка открыть вкладку "Тоталы" букмекера {bookmaker} неудачна'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')
        diag_signal.emit(message)

        # попытка закрыть всплывающее окно уведомления
        driver.implicitly_wait(0)
        driver.find_element(By.XPATH, "//button[text()='Позже']").click()
        driver.find_element(By.XPATH, "//button[text()='Тоталы']").click()
    except:
        message = f'Попытка закрыть всплывающее окно {bookmaker} для открытия вкладки Тоталы неудачна. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(message)
        diag_signal.emit(message)

        get_screenshot(driver, bookmaker)
        return

    # нажатие кнопки с нужным номиналом тотала (открытие купона тотала)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total}')]"))).click()
        logger.info(f'Кнопка с {total} букмекара {bookmaker} найдена и нажата успешно')
    except BaseException as ex:
        message = f'Попытка нажать на кнопку {total} (открыть купон тотала) букмекера {bookmaker} неудачна'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')
        diag_signal.emit(message)

        # попытка закрыть всплывающее окно уведомления
        driver.find_element(By.XPATH, "//button[contains(text(),'Позже')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
            f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total}')]"))).click()
    except:
        message = f'Попытка закрыть всплывающее окно {bookmaker} для открытия купона тотала неудачна. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(message)
        diag_signal.emit(message)

        get_screenshot(driver, bookmaker)
        return

    # беттинг
    #if Preload.betting_on:  # если автоматический беттинг разрешен пробуем поставить
    # ввод значения ставки
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@class,"stake-input__value")]')))
        element.click()
        element.send_keys(Keys.CONTROL + 'A')
        element.send_keys(Keys.DELETE)
        element.send_keys(bet_size)
        if int(element.get_attribute('value')) != int(bet_size):
            raise Exception
        message = f'Значение ставки на событие {bookmaker} введено успешно'
        logger.info(message)
    except BaseException as ex:
        message = f'Не удалось ввести значение ставки на событие {bookmaker} {url}.Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon()
        return

    # получение актуального коэффициента на нужный тотал и сравнение с установленным
    try:
        control_koeff = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "slip-list-item__current-odd")]')))
        control_koeff = float(control_koeff.text)
        if control_koeff < float(total_koeff):
            message = f'Ставка на событие {bookmaker} не сделана, контрольный коэффициент перед ставкой меньше установленного ({control_koeff}<{total_koeff})'
            TelegramService.send_text(message)
            logger.info(message)

            get_screenshot(driver, bookmaker)
            close_coupon()
            return
        message = f'Контрольный коэффициент {bookmaker} перед ставкой выше установленного ({control_koeff}>{total_koeff})'
        logger.info(message)
    except BaseException as ex:
        message = f'Не удалось получить контрольный коэффициент {bookmaker}. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon()
        return

    return True
