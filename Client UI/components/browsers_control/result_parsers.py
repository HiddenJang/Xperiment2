import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import webdriver

logger = logging.getLogger('Client UI.components.browsers_control.result_parsers')


class ResultParser(QObject):
    finish_signal = QtCore.pyqtSignal(dict)
    page_load_timeout = 5

    def __init__(self, active_bets_urls: list):
        super(ResultParser, self).__init__()
        self.active_bets_urls = active_bets_urls

    def start(self) -> str | None:
        """Открытие страниц с результатом и получение результатов событий"""
        results = {}
        driver = webdriver.Driver.get_driver(page_load_timout=ResultParser.page_load_timeout)
        if not driver['driver']:
            self.finish_signal.emit({'status': driver['status'], 'results': {}})
            return
        else:
            self.driver = driver['driver']

        for event_url in self.active_bets_urls:
            bookmaker = event_url.split('$$')[0]
            url = event_url.split('$$')[1]

            if QThread.currentThread().isInterruptionRequested():
                self.driver.close()
                self.driver.quit()
                self.finish_signal.emit({'status': 'Поиск ранее сделанных ставок пропущен пользователем', 'results': {}})
                return
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
                results[event_url] = {'result': result}

        self.driver.close()
        self.driver.quit()
        if not results:
            self.finish_signal.emit({'status': 'Не удалось получить результаты событий по ранее сделанным ставкам',
                                     'results': {}})
        elif len(results) != len(self.active_bets_urls):
            self.finish_signal.emit({'status': 'Результаты событий получены не по всем ранее сделанным ставкам',
                                     'results': results})
        else:
            self.finish_signal.emit({'status': 'Результаты событий получены по всем ранее сделанным ставкам',
                                     'results': results})

    def leon(self) -> str | None:
        """Получение результата события (в формате '2:3')"""

        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'post-match-statistic-incident__score')]")))
            result = element.text
            return result
        except BaseException as ex:
            logger.info(ex)

    def olimp(self) -> str | None:
        """Получение результата события (в формате '2:3')"""
        pass