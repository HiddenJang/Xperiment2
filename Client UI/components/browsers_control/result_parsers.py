import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import webdriver
from .. import settings

logger = logging.getLogger('Client UI.components.browsers_control.websites_control_modules.interaction_controller')


class ResultParser(QObject):
    diag_signal = QtCore.pyqtSignal(str)
    finish_signal = QtCore.pyqtSignal()

    def __init__(self, active_bets_urls: list):
        super(ResultParser, self).__init__()
        self.active_bets_urls = active_bets_urls
        self.driver = webdriver.Driver.get_driver

    def check_starter(self) -> None:
        url = 'https://leon.ru/bets/soccer/turkey/super-lig/1970324845368614-torku-konyaspor-fenerbah-e'
        self.leon(url)

    def leon(self, event_url: str) -> dict | None:
        if self.driver:
            driver = self.driver(event_url, headless=True)['driver']
        else:
            self.diag_signal.emit(self.driver(event_url)['status'])
            return
        try:
            element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'post-match-statistic-incident__score')]")))
            result = element.text
            print(result)
        except BaseException as ex:
            logger.info(ex)
        driver.close()
        driver.quit()
