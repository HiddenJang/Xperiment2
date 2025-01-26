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
from ...telegram import TelegramService

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.olimp')


class SiteInteraction:
    """Класс управления сайтом букмекера"""

    def __init__(self,
                 driver: selenium.webdriver,
                 diag_signal: QtCore.pyqtSignal,
                 bookmaker: str):
        self.driver = driver
        self.diag_signal = diag_signal

        self.bookmaker = bookmaker
        self.start_balance = '0'
        self.bet_data_for_stats = {}

    def __get_screenshot(self) -> str | None:
        """Скриншот и отправка скриншота в telegram"""
        screenshot_name = settings.SCREENSHOTS_DIR / f"{self.bookmaker}-{str(datetime.now()).replace(':', '-')}.png"
        try:
            self.driver.get_screenshot_as_file(screenshot_name)
            TelegramService.send_photo(screenshot_name)
            return str(screenshot_name)
        except BaseException as ex:
            self.__send_diag_message(f"Не удалось сделать скриншот {self.bookmaker}", ex,  send_telegram=False)

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
            self.driver.find_element(By.XPATH, '//button[contains(@class, "clear")]').click()
            self.driver.implicitly_wait(0)
            self.__send_diag_message(f'Купон {self.bookmaker} от ставки закрыт', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(
                f'Не удалось закрытие купона {self.bookmaker} (возможно купоны отсутствуют или были закрыты ранее)', ex, send_telegram=False)

    def __quit(self, message: str, ex: BaseException = '') -> None:
        """Прекращение процесса размещения ставки"""
        self.__get_screenshot()
        self.__send_diag_message(message, ex)
        self.__close_coupon()

    def preload(self, common_auth_data) -> bool | Exception:
        """Авторизация пользователя"""
        login = common_auth_data['auth_data']['login']
        password = common_auth_data['auth_data']['password']
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
        """Подготовка к размещению ставки"""
        self.start_time = datetime.timestamp(datetime.now())

        bookmaker = event_data["bookmaker"]
        bet_size = bet_params[bookmaker]['bet_size']
        min_koeff = bet_params[bookmaker]['min_koeff']
        total_nominal = list(event_data['runners'].keys())[0]
        total_koeff_type = list(event_data['runners'][total_nominal].keys())[0]

        self.bet_data_for_stats['game_type'] = event_data["game_type"]
        self.bet_data_for_stats['game_type_num'] = event_data["game_type_num"]
        self.bet_data_for_stats['bookmaker'] = bookmaker
        self.bet_data_for_stats['teams'] = event_data["teams"]
        self.bet_data_for_stats['url'] = event_data["url"]
        self.bet_data_for_stats['total_nominal'] = total_nominal
        self.bet_data_for_stats['bet_size'] = bet_size
        self.bet_data_for_stats['total_koeff_type'] = total_koeff_type
        self.bet_data_for_stats['date'] = event_data["date"]

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
                self.__send_diag_message(f'Баланс {self.bookmaker} получен и больше размера ставки', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}. Ставка не будет сделана', ex)
            self.__get_screenshot()
            return

        # переключение на вкладку ТОТАЛЫ
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Тоталы']"))).click()
            self.__send_diag_message(f'Вкладка "Тоталы" букмекера {self.bookmaker} нажата', send_telegram=False)
        except BaseException as ex:
            self.__send_diag_message(f'Попытка открыть вкладку "Тоталы" букмекера {self.bookmaker} неудачна', ex)
            self.__get_screenshot()
            return

        # нажатие кнопки с нужным номиналом тотала (открытие купона тотала)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                            f"//div[text()='Тотал']/ancestor::div[contains(@class, 'accordionHead')]/following-sibling::div[contains(@class, 'accordionContent')]/div/div[contains(@class, 'outcomes')]/descendant::span[contains(text(),'{total}')]"))).click()
            self.__send_diag_message(f'Кнопка {total} букмекара {self.bookmaker} найдена и нажата успешно', send_telegram=False)
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
            self.__send_diag_message(f'Значение ставки на событие {self.bookmaker} введено успешно', send_telegram=False)
        except BaseException as ex:
            self.__quit(f'Не удалось ввести значение ставки на событие {self.bookmaker}.Ставка не будет сделана', ex)
            return

        # получение текущего коэффициента ставки на нужный тотал и сравнение с установленным
        try:
            for _ in range(10):
                control_koeff = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(@data-qa, "betCardCoeff")]')))
                logger.info(f'iter = {_}')
                if control_koeff.text:
                    break
            control_koeff = float(control_koeff.text)
            if control_koeff < float(min_koeff):
                self.__send_diag_message(
                    f'Ставка на событие {self.bookmaker} не сделана, текущий коэффициент ставки меньше установленного ({control_koeff}<{min_koeff})')
                self.__get_screenshot()
                self.__close_coupon()
                return
            self.__send_diag_message(
                f'Текущий коэффициент ставки {self.bookmaker} выше или равен установленному ({control_koeff}>={min_koeff})', send_telegram=False)
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
            control_koeff = self.driver.find_element(By.XPATH, '//span[contains(@data-qa, "betCardCoeff")]')
            control_koeff = float(control_koeff.text)
            self.driver.implicitly_wait(0)
            if control_koeff < float(min_koeff):
                self.__quit(
                    f'Коэффициент в купоне {self.bookmaker} меньше установленного ({control_koeff}<{min_koeff}). Ставка не будет сделана')
                return
            self.__send_diag_message(
                f'Коэффициент в купоне {self.bookmaker} перед ставкой выше или равен установленному ({control_koeff}>={min_koeff})', send_telegram=False)
            self.bet_data_for_stats["total_koeff"] = control_koeff
        except BaseException as ex:
            self.__quit(f'Не удалось получить коэффициент в купоне {self.bookmaker}. Ставка не будет сделана', ex)
            return

        #  проверка доступности размещения ставки по информации в купоне
        try:
            element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'warningMessage')]")
            bet_availability = element.text
            if 'Исход недоступен' in bet_availability:
                self.__quit(f'Совершение ставки недоступно по информации в купоне {self.bookmaker}. Ставка не будет сделана')
                return
            self.__send_diag_message(f'Купон {self.bookmaker} доступен для ставки (надпись <Исход недоступен> отсутсвует в купоне)', send_telegram=False)
        except NoSuchElementException as ex:
            self.__send_diag_message(
                f'Купон {self.bookmaker} доступен для ставки (надпись <Исход недоступен> отсутсвует в купоне)', ex, send_telegram=False)
        except BaseException as ex:
            self.__quit(
                f'Невозможно подтвердить доступность ставки по информации в купоне {self.bookmaker}. Ставка не будет сделана', ex)
            return

        # проверка наличия кнопки "Сделать ставку"
        try:
            element = self.driver.find_element(By.XPATH,
                                               "//div[contains(@class, 'makeBetButton')]/div[contains(@class, 'buttons')]/button[@type='submit']")
            button_name = element.text
            if 'сделать ставку' not in button_name.lower():
                self.__quit(
                    f'Кнопка <Сделать ставку> {self.bookmaker} недоступна. Ставка не будет сделана')
                return
            self.__send_diag_message(f'Кнопка <Сделать ставку> {self.bookmaker} найдена', send_telegram=False)
        except BaseException as ex:
            self.__quit(
                f'Кнопка <Сделать ставку> {self.bookmaker} не найдена. Ставка не будет сделана',
                ex)
            return

        self.__send_diag_message(f'Букмекер {self.bookmaker} готов к ставке', send_telegram=False)

        return True

    def bet(self, bet_params: dict) -> dict:
        """Размещение ставки"""
        imitation = bet_params['bet_imitation']
        result = False
        self.bet_data_for_stats['start_balance'] = self.start_balance
        self.bet_data_for_stats['bet_imitation'] = imitation
        # нажатие кнопки "Сделать ставку"
        try:
            if not imitation:
                self.driver.find_element(By.XPATH, "//div[contains(@class, 'makeBetButton')]/div[contains(@class, 'buttons')]/button[@type='submit']").click()
                self.__send_diag_message(f'Кнопка <Сделать ставку> {self.bookmaker} успешно нажата')
            else:
                self.__send_diag_message(f'Кнопка <Сделать ставку> {self.bookmaker} успешно нажата (в режиме имитации)')
        except BaseException as ex:
            self.__quit(f'Не удалось нажать кнопку <Сделать ставку> {self.bookmaker}. Ставка не будет сделана', ex)

        self.betting_time = datetime.timestamp(datetime.now()) - self.start_time
        self.bet_data_for_stats['betting_time'] = self.betting_time
        self.bet_data_for_stats['screenshot_name'] = self.__get_screenshot()
        # проверка изменения баланса после ставки
        try:
            for i in range(30):
                element = self.driver.find_element(By.XPATH, "//span[contains(@title, 'Пополнить баланс')]")
                balance = element.text
                if (float(balance) < float(self.start_balance)) or imitation:
                    self.__send_diag_message(f'Есть изменение баланса {self.bookmaker}')
                    result = True
                    self.bet_data_for_stats['balance_after_bet'] = balance
                    break
                else:
                    self.__send_diag_message(f'Нет изменения баланса {self.bookmaker}')
                sleep(1)
        except BaseException as ex:
            self.__send_diag_message(f'Не удалось получить баланс {self.bookmaker}', ex)

        self.__get_screenshot()
        return {'result': result, 'bet_data_for_stats': self.bet_data_for_stats}

    def extract_event_result(self, event_data: dict) -> dict:
        """Получение результата события"""
        sleep(10)
        return {'bookmaker': 'leon', 'teams': 'ЦСКА - Спартак', 'result': {'home': '2', 'away': '0'}}