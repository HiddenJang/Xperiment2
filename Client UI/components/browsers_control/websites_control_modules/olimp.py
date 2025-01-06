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
            self.driver.find_element(By.XPATH, '//button[contains(@class, "clear")]').click()
            self.driver.implicitly_wait(0)
            self.__send_diag_message(f'Купон {self.bookmaker} от ставки закрыт')
        except BaseException as ex:
            self.__send_diag_message(
                f'Не удалось закрытие купона {self.bookmaker} (возможно купоны отсутствуют или были закрыты ранее)', ex)

    def __quit(self, message: str, ex: BaseException = '') -> None:
        """Прекращение процесса размещения ставки"""
        self.__send_diag_message(message, ex)
        self.__get_screenshot()
        self.__close_coupon()

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
        """Подготовка к размещению ставки"""
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
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@title, 'Пополнить баланс')]")))
            self.start_balance = element.text
            if float(self.start_balance) < float(bet_size):
                self.__send_diag_message(
                    f'Ставка на событие {self.bookmaker} не будет сделана, баланс меньше размера ставки')
                return
            else:
                self.__send_diag_message(f'Баланс {self.bookmaker} получен и больше размера ставки')
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}. Ставка не будет сделана', ex)
            self.__get_screenshot()
            return

        # переключение на вкладку ТОТАЛЫ
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Тоталы']"))).click()
        except BaseException as ex:
            self.__send_diag_message(f'Попытка открыть вкладку "Тоталы" букмекера {self.bookmaker} неудачна', ex)
            self.__get_screenshot()
            return

        # нажатие кнопки с нужным номиналом тотала (открытие купона тотала)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                            f"//div[text()='Тотал']/ancestor::div[contains(@class, 'accordionHead')]/following-sibling::div[contains(@class, 'accordionContent')]/div/div[contains(@class, 'outcomes')]/descendant::span[contains(text(),'{total}')]"))).click()
            logger.info(f'Кнопка {total} букмекара {self.bookmaker} найдена и нажата успешно')
        except BaseException as ex:
            self.__send_diag_message(
                f'Попытка нажать на кнопку {total} (открыть купон тотала) букмекера {self.bookmaker} неудачна', ex)
            self.__get_screenshot()
            return

        # ввод значения ставки
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder,"Сумма")]')))
            element.click()
            element.send_keys(Keys.CONTROL + 'A')
            element.send_keys(Keys.DELETE)
            element.send_keys(bet_size)
            if int(element.get_attribute('value')) != int(bet_size):
                raise Exception
            self.__send_diag_message(f'Значение ставки на событие {self.bookmaker} введено успешно')
        except BaseException as ex:
            self.__quit(f'Не удалось ввести значение ставки на событие {self.bookmaker}.Ставка не будет сделана', ex)
            return

        # получение текущего коэффициента ставки на нужный тотал и сравнение с установленным
        try:
            control_koeff = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@data-qa, "betCardCoeff")]')))
            control_koeff = float(control_koeff.text)
            if control_koeff < float(min_koeff):
                self.__send_diag_message(
                    f'Ставка на событие {self.bookmaker} не сделана, текущий коэффициент ставки меньше установленного ({control_koeff}<{min_koeff})')
                self.__get_screenshot()
                self.__close_coupon()
                return
            self.__send_diag_message(
                f'Текущий коэффициент ставки {self.bookmaker} выше или равен установленному ({control_koeff}>={min_koeff})')
        except BaseException as ex:
            self.__quit(f'Не удалось получить текущий коэффициент ставки {self.bookmaker}. Ставка не будет сделана', ex)
            return

        return True

    def last_test(self, bet_params: dict) -> bool | None:
        """Проведение последних коротких проверок перед совершением ставки"""
        min_koeff = bet_params[self.bookmaker]['min_koeff']
        # повторная проверка коэффициента на нужный тотал и сравнение с установленным
        try:
            self.driver.implicitly_wait(5)
            control_koeff = self.driver.find_element(By.XPATH, '//span[contains(@data-qa, "betCardCoeff")]')
            control_koeff = float(control_koeff.text)
            self.driver.implicitly_wait(0)
            if control_koeff < float(min_koeff):
                self.__quit(
                    f'Не пройдена последняя контрольная проверка {self.bookmaker}. Коэффициент в купоне меньше установленного ({control_koeff}<{min_koeff}). Ставка не будет сделана')
                return
            self.__send_diag_message(
                f'Коэффициент в купоне {self.bookmaker} перед ставкой выше или равен установленному ({control_koeff}>={min_koeff})')
        except BaseException as ex:
            self.__quit(
                f'Не пройдена последняя контрольная проверка {self.bookmaker}. Не удалось получить коэффициент в купоне. Ставка не будет сделана',
                ex)
            return

        #  проверка доступности размещения ставки по информации в купоне
        try:
            element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'warningMessage')]")
            bet_availability = element.text
            if 'Исход недоступен' in bet_availability:
                self.__quit(
                    f'Не пройдена последняя контрольная проверка {self.bookmaker}. Совершение ставки недоступно по информации в купоне. Ставка не будет сделана')
                return
        except NoSuchElementException as ex:
            self.__send_diag_message(
                f'Купон {self.bookmaker} доступен для ставки (надпись <Исход недоступен> отсутсвует в купоне)', ex)
        except BaseException as ex:
            self.__quit(
                f'Не пройдена последняя контрольная проверка {self.bookmaker}. Невозможно подтвердить доступность ставки по информации в купоне. Ставка не будет сделана',
                ex)
            return

        # проверка наличия кнопки "Сделать ставку"
        try:
            element = self.driver.find_element(By.XPATH,
                                               "//div[contains(@class, 'makeBetButton')]/div[contains(@class, 'buttons')]/button[@type='submit']")
            button_name = element.text
            if 'сделать ставку' not in button_name.lower():
                self.__quit(
                    f'Не пройдена последняя контрольная проверка {self.bookmaker}. Кнопка <Сделать ставку> недоступна. Ставка не будет сделана')
                return
            self.__send_diag_message(f'Кнопка <Сделать ставку> найдена')
        except BaseException as ex:
            self.__quit(
                f'Не пройдена последняя контрольная проверка {self.bookmaker}. Кнопка <Сделать ставку> не найдена. Ставка не будет сделана',
                ex)
            return

        self.__send_diag_message(f'Последняя контрольная проверка пройдена. Букмекер {self.bookmaker} готов к ставке')

        return True

    def bet(self, bet_params: dict) -> bool | None:
        """Размещение ставки"""
        imitation = bet_params['bet_imitation']

        # нажатие кнопки "Сделать ставку"
        try:
            if not imitation:
                self.driver.find_element(By.XPATH, "//div[contains(@class, 'makeBetButton')]/div[contains(@class, 'buttons')]/button[@type='submit']").click()
                self.__send_diag_message(f'Кнопка <Сделать ставку> {self.bookmaker} успешно нажата')
            else:
                self.__quit(f'Кнопка <Сделать ставку> {self.bookmaker} успешно нажата (в режиме имитации)')
        except BaseException as ex:
            self.__quit(f'Не удалось нажать кнопку <Сделать ставку> {self.bookmaker}. Ставка не будет сделана', ex)

        # проверка изменения баланса после ставки
        try:
            for i in range(30):
                element = self.driver.find_element(By.XPATH, "//span[contains(@title, 'Пополнить баланс')]")
                balance = element.text
                if (float(balance) < float(self.start_balance)) or imitation:
                    self.__send_diag_message(f'Есть изменение баланса {self.bookmaker}')
                    result = True
                    break
                else:
                    self.__send_diag_message(f'Нет изменения баланса {self.bookmaker}')
                    result = None
                sleep(1)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}', ex)
            result = None

        self.__get_screenshot()
        return result
