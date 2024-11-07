import logging
import sys

from .. import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger('Client UI.components.browsers_control.core')


class Driver:
    """Класс вебдрайвера для управления браузером"""

    def __init__(self, base_url):
        self.base_url = base_url

    def get_driver(self) -> webdriver:
        """Создание объекта вебдрайвера"""
        webdriver_file_path = settings.WEBDRIVER_DIR.get(sys.platform)
        s = Service(executable_path=webdriver_file_path)
        opts = Options()
        # opts.add_argument('--headless') # запуск браузера в фоне
        opts.add_argument("start-maximized")  # открыть в весь экран
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])  # устанавливаем опции для эмуляции управления прользователем (чтобы сайт не догадался)
        opts.add_experimental_option('useAutomationExtension', False)
        try:
            driver = webdriver.Chrome(options=opts, service=s)
            driver.get(url=self.base_url)
            return driver
        except BaseException as ex:
            logger.error(ex)


if __name__ == '__main__':
    driver = Driver('https://leon.ru/').get_driver()
