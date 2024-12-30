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
        bookmaker: str,
        url: str,
        bet_size: str,
        total_nominal: str,
        total_koeff_type: str,
        total_koeff: str) -> None:
    """Размещение ставки"""
    # закрытие купона тотала, если он остался от предыдущей ставки
    try:
        element = driver.find_element(By.XPATH, '//button[@class="bet-slip-event-card__remove"]')
        element.click()
        logger.info(f'Купон {bookmaker} от предыдущей ставки закрыт после загрузки страницы найденного события')
    except BaseException as ex:
        logger.info(
            f'Не удалось закрытие купона LEON сразу после загрузки страницы (возможно он ранее был закрыт), {ex}')
    # проверка достаточности баланса
    try:
        elementW = WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.XPATH, '//div[@class="balance__text"]')))
        elementW.text
        balance = balance.split('.')[0]
        if float(balance) < float(bet_size):
            TelegramBot.sendText('Ставка на событие LEON не будет сделана, баланс меньше размера ставки.')
            logger.info(f'Ставка на событие LEON {url} не будет сделана, баланс меньше размера ставки.')
            self.event_thread.clear()
            return
    except Exception as ex:
        TelegramBot.sendText('Не удалось получить баланс LEON. Ставка не будет сделана.')
        logger.info(f'Не удалось получить баланс LEON. Ставка не будет сделана. {ex}')

        # удалить после отработки
        shotname_after = Preload.path + f"screenshots\\LEONafter-{str(datetime.now()).replace(':', '-')}.png"
        driver.get_screenshot_as_file(shotname_after)  # скриншот
        TelegramBot.sendPhoto(shotname_after)  # отправляет скриншот

        self.event_thread.clear()
        return



