import logging
import threading
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .. import webdriver
from ... import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.betboom')


class Control:
    preloaded = False

    def __init__(self, common_auth_data: dict, thread_event: threading.Event):
        self.common_auth_data = common_auth_data
        self.thread_event = thread_event

    def preload(self):
        """Открытие страницы БК и авторизация пользователя"""

        driver = webdriver.Driver(settings.BOOKMAKERS.get(self.common_auth_data['bkmkr_name'])).get_driver()
        driver = driver['driver']
        login = self.common_auth_data['auth_data']['login']
        password = self.common_auth_data['auth_data']['password']

        for n in range(5):
            try:
                driver.switch_to.default_content()
                element3 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, f'//button[contains(text(), "Вход")]')))
                element3.click()
                sleep(2)
                break
            except BaseException as ex:
                if n == 4:
                    logger.error(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    driver.close()
                    driver.quit()
                    return
                sleep(3)
                continue
        for n in range(5):
            try:
                element4 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel']")))
                element5 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
                element4.clear()
                sleep(0.5)
                element4.send_keys(login)
                sleep(0.5)
                element5.send_keys(password)
                sleep(0.5)
                element6 = driver.find_element(By.XPATH, "//button[@type='submit']")  # [contains(text(), 'Войти']
                element6.click()
                sleep(2)
                break
            except Exception as ex:
                if n == 4:
                    logger.error(f'Ошибка авторизации {self.common_auth_data["bkmkr_name"]}, {ex}')
                    driver.close()
                    driver.quit()
                    return
                else:
                    try:
                        element4 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='tel']")))
                        element5 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
                        element4.clear()
                        sleep(0.5)
                        element5.clear()
                        sleep(0.5)
                    except:
                        continue
                    sleep(1)

        Control.preloaded = True
        self.thread_event.wait()
