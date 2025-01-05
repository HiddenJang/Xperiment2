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


def close_coupon(driver: selenium.webdriver, diag_signal: QtCore.pyqtSignal, bookmaker: str) -> None:
    """Закрытие купона ставки"""
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


def preload(driver: selenium.webdriver, login: str, password: str) -> None:
    """Авторизация пользователя"""
    # нажатие кнопки ВОЙТИ
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/login']"))).click()
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
                    total_koeff: str) -> bool | None:
    """Подготовка к размещению ставки"""

    if total_koeff_type == 'under':
        total = f'Меньше ({total_nominal})'
    else:
        total = f'Больше ({total_nominal})'

    # закрытие купона тотала, если он остался от предыдущей ставки
    close_coupon(driver, diag_signal, bookmaker)
    # проверка достаточности баланса
    try:
        driver.implicitly_wait(10)
        element = driver.find_element(By.XPATH, '//div[contains(@class, "balance__text")]')
        balance = element.text.split(',')[0]
        driver.implicitly_wait(0)
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

    # попытка закрыть всплывающее окно уведомления
    try:
        driver.find_element(By.XPATH, "//svg[@role='presentation']").click()
        logger.info(f'Всплывающее окно уведомления закрыто')
    except BaseException as ex:
        logger.info(f'Всплывающее окно уведомления не найдено, {ex}')

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
        driver.find_element(By.XPATH, "//svg[@role='presentation']").click()
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
        logger.info(f'Кнопка {total} букмекара {bookmaker} найдена и нажата успешно')
    except BaseException as ex:
        message = f'Попытка нажать на кнопку {total} (открыть купон тотала) букмекера {bookmaker} неудачна'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')
        diag_signal.emit(message)

        # попытка закрыть всплывающее окно уведомления
        driver.find_element(By.XPATH, "//svg[@role='presentation']").click()
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
        diag_signal.emit(message)
        logger.info(message)
    except BaseException as ex:
        message = f'Не удалось ввести значение ставки на событие {bookmaker} {url}.Ставка не будет сделана'
        TelegramService.send_text(message)
        diag_signal.emit(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon(driver, diag_signal, bookmaker)
        return

    # получение текущего коэффициента ставки на нужный тотал и сравнение с установленным
    try:
        control_koeff = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "slip-list-item__current-odd")]')))
        control_koeff = float(control_koeff.text)
        if control_koeff < float(total_koeff):
            message = f'Ставка на событие {bookmaker} не сделана, текущий коэффициент ставки меньше установленного ({control_koeff}<{total_koeff})'
            TelegramService.send_text(message)
            diag_signal.emit(message)
            logger.info(message)

            get_screenshot(driver, bookmaker)
            close_coupon(driver, diag_signal, bookmaker)
            return
        message = f'Текущий коэффициент ставки {bookmaker} выше или равен установленному ({control_koeff}>={total_koeff})'
        TelegramService.send_text(message)
        diag_signal.emit(message)
        logger.info(message)
    except BaseException as ex:
        message = f'Не удалось получить текущий коэффициент ставки {bookmaker}. Ставка не будет сделана'
        TelegramService.send_text(message)
        diag_signal.emit(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon(driver, diag_signal, bookmaker)
        return

    return True


def last_test(driver: selenium.webdriver,
              diag_signal: QtCore.pyqtSignal,
              bookmaker: str,
              total_koeff: str) -> bool | None:
    """Проведение последних коротких проверок перед совершением ставки"""
    # повторная проверка коэффициента на нужный тотал и сравнение с установленным
    try:
        control_koeff = driver.find_element(By.XPATH, '//span[contains(@class, "slip-list-item__current-odd")]')
        control_koeff = float(control_koeff.text)
        if control_koeff < float(total_koeff):
            message = f'Не пройдена последняя контрольная проверка {bookmaker}. Коэффициент в купоне меньше установленного ({control_koeff}<{total_koeff}). Ставка не будет сделана'
            TelegramService.send_text(message)
            diag_signal.emit(message)
            logger.info(message)

            get_screenshot(driver, bookmaker)
            close_coupon(driver, diag_signal, bookmaker)
            return
        message = f'Коэффициент в купоне {bookmaker} перед ставкой выше или равен установленному ({control_koeff}>={total_koeff})'
        TelegramService.send_text(message)
        diag_signal.emit(message)
        logger.info(message)
    except BaseException as ex:
        message = f'Не пройдена последняя контрольная проверка {bookmaker}. Не удалось получить коэффициент в купоне. Ставка не будет сделана'
        TelegramService.send_text(message)
        diag_signal.emit(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon(driver, diag_signal, bookmaker)
        return
    #  проверка доступности размещения ставки по информации в купоне
    try:
        element = driver.find_element(By.XPATH, "//div[contains(@class, 'slip-list-item__blocked-message')]")
        bet_availability = element.text
        if 'Недоступно для ставок' in bet_availability:
            message = f'Не пройдена последняя контрольная проверка {bookmaker}. Совершение ставки недоступно по информации в купоне. Ставка не будет сделана'
            TelegramService.send_text(message)
            diag_signal.emit(message)
            logger.info(message)

            get_screenshot(driver, bookmaker)
            close_coupon(driver, diag_signal, bookmaker)
            return
    except BaseException as ex:
        message = f'Не пройдена последняя контрольная проверка. Совершение ставки букмекера {bookmaker} недоступно по информации в купоне. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')
        diag_signal.emit(message)
        return
    message = f'Последняя контрольная проверка пройдена. Букмекер {bookmaker} готов к ставке'
    TelegramService.send_text(message)
    logger.info(message)
    diag_signal.emit(message)
    return True


def bet(driver: selenium.webdriver,
        diag_signal: QtCore.pyqtSignal,
        bookmaker: str,
        imitation: bool) -> bool | None:
    """Размещение ставки"""
    # нажатие кнопки "Заключить пари"
    try:
        if not imitation:
            driver.find_element(By.XPATH, "//button[@data-test-el='bet-slip-button_summary']").click()
            message = f'Кнопка ЗАКЛЮЧИТЬ ПАРИ {bookmaker} успешно нажата'
        else:
            message = f'Кнопка ЗАКЛЮЧИТЬ ПАРИ {bookmaker} успешно нажата (в режиме имитации)'
        TelegramService.send_text(message)
        logger.info(message)

        return True
    except BaseException as ex:
        message = f'Не удалось нажать кнопку ЗАКЛЮЧИТЬ ПАРИ {bookmaker}. Ставка не будет сделана'
        TelegramService.send_text(message)
        logger.info(f'{message}: {ex}')

        get_screenshot(driver, bookmaker)
        close_coupon(driver, diag_signal, bookmaker)

    # проверка изменения баланса после ставки
    # try:
    #     element_ = driver.find_element(By.XPATH, '//div[@class ="balance__text"]')
    #     balance_afterbet = element_.text
    #     balance_afterbet = balance_afterbet.split(' ')[0]
    #     if float(balance_afterbet) < float(balance):
    #         logger.info(f'Есть изменение баланса LEON после ставки: {url}')
    #         TelegramBot.sendText(f'Есть изменение баланса LEON после ставки.')
    #         if book_number == 'first':
    #             Preload.betDone_first = True
    #         else:
    #             Preload.betDone_second = True
    #         break