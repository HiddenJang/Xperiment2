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

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.leon')


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
        try:
            self.driver.get_screenshot_as_file(screenshot_name)
            TelegramService.send_photo(screenshot_name)
        except BaseException as ex:
            self.__send_diag_message(f"Не удалось сделать скриншот {self.bookmaker}", ex, send_telegram=False)

    def __send_diag_message(self, message: str, ex: BaseException = '', send_telegram: bool = True) -> None:
        """Отправка диагностики"""
        logger.info(f'{message} {str(ex)}')
        self.diag_signal.emit(message)
        if send_telegram:
            TelegramService.send_text(message)

    def __close_coupon(self) -> None:
        """Закрытие купона ставки"""
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(By.XPATH, '//button[text()="Очистить"]').click()
            self.driver.find_element(By.XPATH, '//button[text()="Удалить"]').click()
            self.driver.implicitly_wait(0)
            self.__send_diag_message(f'Купон {self.bookmaker} от ставки закрыт', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось закрытие купона {self.bookmaker} (возможно купоны отсутствуют или были закрыты ранее)', ex, send_telegram=False)

    def __quit(self, message: str, ex: BaseException = '') -> None:
        """Прекращение процесса размещения ставки"""
        self.__get_screenshot()
        self.__send_diag_message(message, ex)
        self.__close_coupon()

    def preload(self) -> bool | Exception:
        """Авторизация пользователя"""
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']
        # нажатие кнопки ВОЙТИ
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/login']"))).click()
        # нажатие вкладки EMAIL
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'E-mail')]"))).click()
        # очитска полей ЛОГИН и ПАРОЛЬ и ввод данных авторизации
        element1 = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='login']")))
        element2 = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        element1.clear()
        element2.clear()
        element1.send_keys(login)
        element2.send_keys(password)
        # нажатие кнопки ВОЙТИ в окне авторизации
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'login__button')]"))).click()
        # проверка отображения баланса
        self.driver.implicitly_wait(20)
        element = self.driver.find_element(By.XPATH, '//div[contains(@class, "balance__text")]')
        balance = element.text.split(',')[0]
        self.driver.implicitly_wait(0)
        if not float(balance) >= 0:
            raise Exception
        else:
            return True

    def prepare_for_bet(self, event_data: dict, bet_params: dict) -> bool | None:
        """Подготовка к размещению ставки"""
        self.start_time = datetime.timestamp(datetime.now())

        bookmaker = event_data["bookmaker"]
        bet_size = bet_params[bookmaker]['bet_size']
        min_koeff = bet_params[bookmaker]['min_koeff']
        total_nominal = list(event_data['runners'].keys())[0]
        total_koeff_type = list(event_data['runners'][total_nominal].keys())[0]

        if total_koeff_type == 'under':
            total = f'Меньше ({total_nominal})'
        else:
            total = f'Больше ({total_nominal})'

        # закрытие купона тотала, если он остался от предыдущей ставки
        self.__close_coupon()
        # проверка достаточности баланса
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "balance__text")]')))
            self.start_balance = element.text.split(',')[0]
            if float(self.start_balance) < float(bet_size):
                self.__send_diag_message(f'Ставка на событие {self.bookmaker} не будет сделана, баланс меньше размера ставки')
                return
            else:
                self.__send_diag_message(f'Баланс {self.bookmaker} получен и больше размера ставки', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}. Ставка не будет сделана', ex)
            self.__get_screenshot()
            return

        # попытка закрыть всплывающее окно уведомления
        try:
            WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//svg[@role='presentation']"))).click()
            logger.info(f'Всплывающее окно уведомления {self.bookmaker} закрыто')
        except BaseException as ex:
            logger.info(f'Всплывающее окно уведомления {self.bookmaker} не найдено, {ex}')

        # переключение на вкладку ТОТАЛЫ
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Тоталы']"))).click()
            self.__send_diag_message(f'Вкладка "Тоталы" букмекера {self.bookmaker} нажата', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Попытка открыть вкладку "Тоталы" букмекера {self.bookmaker} неудачна', ex)
            ## попытка закрыть всплывающее окно уведомления
            WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//svg[@role='presentation']"))).click()
            self.driver.find_element(By.XPATH, "//button[text()='Тоталы']").click()
        except:
            self.__send_diag_message(f'Попытка закрыть всплывающее окно {self.bookmaker} для открытия вкладки Тоталы неудачна. Ставка не будет сделана')
            self.__get_screenshot()
            return

        # нажатие кнопки с нужным номиналом тотала (открытие купона тотала)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total}')]"))).click()
            self.__send_diag_message(f'Кнопка {total} букмекара {self.bookmaker} найдена и нажата успешно', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Попытка нажать на кнопку {total} (открыть купон тотала) букмекера {self.bookmaker} неудачна', ex)
            ## попытка закрыть всплывающее окно уведомления
            WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//svg[@role='presentation']"))).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                f"//span[text()='Тотал']/ancestor::div[contains(@class, 'sport-event-details-market-group__header')]/following-sibling::div[contains(@class, 'sport-event-details-market-group__content')]/descendant::span[contains(text(),'{total}')]"))).click()
            self.__send_diag_message(f'Кнопка {total} букмекара {self.bookmaker} найдена и нажата после закрытия всплывающего окно уведомления', send_telegram=False)
        except:
            self.__send_diag_message(f'Попытка закрыть всплывающее окно {self.bookmaker} для открытия купона тотала неудачна. Ставка не будет сделана')
            self.__get_screenshot()
            return

        # ввод значения ставки
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[contains(@class,"stake-input__value")]')))
            element.click()
            element.send_keys(Keys.CONTROL + 'A')
            element.send_keys(Keys.DELETE)
            element.send_keys(bet_size)
            if int(element.get_attribute('value')) != int(bet_size):
                raise Exception
            self.__send_diag_message(f'Значение ставки на событие {self.bookmaker} введено успешно', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Не удалось ввести значение ставки на событие {self.bookmaker}.Ставка не будет сделана', ex)
            return

        # получение текущего коэффициента ставки на нужный тотал и сравнение с установленным
        try:
            control_koeff = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "slip-list-item__current-odd")]')))
            control_koeff = float(control_koeff.text)
            if control_koeff < float(min_koeff):
                self.__send_diag_message(f'Ставка на событие {self.bookmaker} не сделана, текущий коэффициент ставки меньше установленного ({control_koeff}<{min_koeff})')
                self.__get_screenshot()
                self.__close_coupon()
                return
            self.__send_diag_message(f'Текущий коэффициент ставки {self.bookmaker} выше или равен установленному ({control_koeff}>={min_koeff})', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Не удалось получить текущий коэффициент ставки {self.bookmaker}. Ставка не будет сделана', ex)
            return

        return True

    def last_test(self, bet_params: dict) -> bool | None:
        """Проведение последних коротких проверок перед совершением ставки"""
        min_koeff = bet_params[self.bookmaker]['min_koeff']
        # повторная проверка коэффициента на нужный тотал и сравнение с установленным
        try:
            self.driver.implicitly_wait(1)
            control_koeff = self.driver.find_element(By.XPATH, '//span[contains(@class, "slip-list-item__current-odd")]')
            control_koeff = float(control_koeff.text)
            self.driver.implicitly_wait(0)
            if control_koeff < float(min_koeff):
                self.__quit(f'Коэффициент в купоне {self.bookmaker} меньше установленного ({control_koeff}<{min_koeff}). Ставка не будет сделана')
                return
            self.__send_diag_message(f'Коэффициент в купоне {self.bookmaker} перед ставкой выше или равен установленному ({control_koeff}>={min_koeff})', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Не удалось получить коэффициент в купоне {self.bookmaker}. Ставка не будет сделана', ex)
            return

        #  проверка доступности размещения ставки по информации в купоне
        try:
            element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'slip-list-item__blocked-message')]")
            bet_availability = element.text
            if 'Недоступно для ставок' in bet_availability:
                self.__quit(f'Совершение ставки {self.bookmaker} недоступно по информации в купоне. Ставка не будет сделана')
                return
            self.__send_diag_message(f'Купон {self.bookmaker} доступен для ставки (надпись <Недоступно для ставок> отсутсвует в купоне)', send_telegram=False)
        except NoSuchElementException:
            self.__send_diag_message(f'Купон {self.bookmaker} доступен для ставки (надпись <Недоступно для ставок> отсутсвует в купоне)', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Невозможно подтвердить доступность ставки по информации в купоне {self.bookmaker}. Ставка не будет сделана', ex)
            return

        # проверка наличия кнопки "Заключить пари"
        try:
            element = self.driver.find_element(By.XPATH, "//button[contains(@data-test-attr-mode, 'ready_to_place_bet')]")
            button_name = element.text
            if 'заключить пари' not in button_name.lower():
                self.__quit(f'Кнопка <Заключить пари> {self.bookmaker} недоступна. Ставка не будет сделана')
                return
            self.__send_diag_message(f'Кнопка <Заключить пари> {self.bookmaker} найдена', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Кнопка <Заключить пари> {self.bookmaker} не найдена. Ставка не будет сделана', ex)
            return

        self.__send_diag_message(f'Букмекер {self.bookmaker} готов к ставке', send_telegram=False)
        return True

    def bet(self, bet_params: dict) -> dict:
        """Размещение ставки"""
        imitation = bet_params['bet_imitation']
        result = False
        # нажатие кнопки "Заключить пари"
        try:
            if not imitation:
                self.driver.find_element(By.XPATH, "//button[@data-test-el='bet-slip-button_summary']").click()
                self.__send_diag_message(f'Кнопка <Заключить пари> {self.bookmaker} успешно нажата')
            else:
                self.__send_diag_message(f'Кнопка <Заключить пари> {self.bookmaker} успешно нажата (в режиме имитации)')
        except BaseException as ex:
            self.__quit(f'Не удалось нажать кнопку <Заключить пари> {self.bookmaker}. Ставка не будет сделана', ex)

        self.betting_time = datetime.timestamp(datetime.now()) - self.start_time

        # проверка изменения баланса после ставки
        try:
            for i in range(30):
                element = self.driver.find_element(By.XPATH, '//div[contains(@class, "balance__text")]')
                balance = element.text.split(',')[0]
                if (float(balance) < float(self.start_balance)) or imitation:
                    self.__send_diag_message(f'Есть изменение баланса {self.bookmaker}')
                    result = True
                    break
                else:
                    self.__send_diag_message(f'Нет изменения баланса {self.bookmaker}')
                sleep(1)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}', ex)

        self.__get_screenshot()
        return {'result': result, 'betting_time': self.betting_time}
