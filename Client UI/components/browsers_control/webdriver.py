import logging
import os.path
import sys

from selenium.common import TimeoutException, WebDriverException

#from .. import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger('Client UI.components.browsers_control.webdriver')


class settings:
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    WEBDRIVER_DIR = {'linux': BASE_DIR / "components/browsers_control/chromedriver/chromedriver",
                     'win32': BASE_DIR / "components\\browsers_control\\chromedriver\\chromedriver.exe"}

class Driver:
    """Класс вебдрайвера для управления браузером"""

    @staticmethod
    def get_driver(url: str = '', page_load_timout: int = 5, headless: bool = None) -> dict:
        """Создание объекта вебдрайвера"""
        webdriver_file_path = settings.WEBDRIVER_DIR.get(sys.platform)
        if not os.path.exists(webdriver_file_path):
            logger.error(f'Webdriver отсутствует в директории {webdriver_file_path}. '
                               f'Необходимо скачать webdriver Chrome')
            return {'driver': None,
                    'status': f'Webdriver отсутствует в директории {webdriver_file_path}. '
                               f'Необходимо скачать webdriver Chrome',
                    'ex': ''}

        s = Service(executable_path=webdriver_file_path)
        opts = Options()
        if headless:
            opts.add_argument('--headless') # запуск браузера в фоне
        opts.add_argument("start-maximized")  # открыть в весь экран
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])  # устанавливаем опции для эмуляции управления прользователем (чтобы сайт не догадался)
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_experimental_option('detach', True)
        try:
            driver = webdriver.Chrome(options=opts, service=s)
            driver.set_page_load_timeout(page_load_timout)
            if not url:
                return {'driver': driver, 'status': 'Webdriver успешно подключен', 'ex': ''}
            try:
                driver.get(url=url)
            except TimeoutException:
                logger.info(f'Превышение времени ожидания открытия стартовой страницы {url}. Попытка продолжить')
            return {'driver': driver, 'status': 'Webdriver успешно подключен', 'ex': ''}
        except BaseException as ex:
            try:
                driver.quit()
                driver.close()
            except BaseException:
                pass
            logger.error(ex)
            return {'driver': None, 'status': f'Ошибка в работе webdriver', 'ex': ex}


if __name__ == '__main__':
    driver = Driver('https://leon.ru/').get_driver()
