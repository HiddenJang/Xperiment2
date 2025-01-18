import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import webdriver
from .. import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.interaction_controller')


class ResultParser(QObject):
    diag_signal = QtCore.pyqtSignal(str)
    finish_signal = QtCore.pyqtSignal()
    page_load_timeout = 5

    def __init__(self, active_bets_urls: list):
        super(ResultParser, self).__init__()
        self.active_bets_urls = active_bets_urls

    def check_starter(self) -> str | None:
        driver = webdriver.Driver.get_driver(page_load_timout=self.page_load_timeout, headless=True)
        if not driver['driver']:
            self.diag_signal.emit(driver['status'])
            return
        else:
            self.driver = driver['driver']

        for event_url in self.active_bets_urls:
            bookmaker = event_url.split('$$')[0]
            url = event_url.split('$$')[1]
            try:
                func = getattr(self, bookmaker)
            except AttributeError as ex:
                logger.info(ex)
                continue
            try:
                self.driver.get(url)
            except TimeoutException:
                logger.info(f'Превышение времени ожидания открытия страницы {bookmaker} для получения результата. Попытка продолжить')
            result = func()
            if result:
                return result

        self.driver.close()
        self.driver.quit()

    def leon(self) -> str | None:
        """Получение результата события (в формате '2:3')"""

        try:
            element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'post-match-statistic-incident__score')]")))
            result = element.text
            return result
        except BaseException as ex:
            logger.info(ex)

    def olimp(self) -> str | None:
        """Получение результата события (в формате '2:3')"""
        pass