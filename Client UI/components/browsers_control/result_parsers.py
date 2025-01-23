import logging

import asyncio
import aiohttp
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import webdriver
from .. import settings

logger = logging.getLogger('Client UI.components.browsers_control.result_parsers')


class SeleniumParser(QObject):
    """Получение результатов путем открытия страниц событий модулем Selenium"""
    finish_signal = QtCore.pyqtSignal(dict)
    page_load_timeout = 5

    def __init__(self, active_bets_urls: list):
        super(SeleniumParser, self).__init__()
        self.active_bets_urls = active_bets_urls

    def start(self) -> str | None:
        """Открытие страниц с результатом и получение результатов событий"""
        results = {}
        driver = webdriver.Driver.get_driver(page_load_timout=SeleniumParser.page_load_timeout)
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


class ApiResponseParser(QObject):
    """Получение результатов путем запроса к API сайта букмекера"""
    finish_signal = QtCore.pyqtSignal(dict)

    def __init__(self, active_bets_data: list):
        super(ApiResponseParser, self).__init__()
        self.active_bets_data = active_bets_data

    def start(self) -> None:
        """Запуск"""
        asyncio.run(self.start_async_func())

    async def start_async_func(self) -> list:
        results = {}
        tasks = []
        async with aiohttp.ClientSession() as session:
            for event_data in self.active_bets_data:
                bookmaker = event_data["bookmaker"]
                date = event_data["date"]
                api_url = settings.RESULT_API_URL.get(bookmaker)

                try:
                    func = getattr(self, bookmaker)
                except AttributeError as ex:
                    logger.info(ex)
                    continue

                task = asyncio.create_task(func(session, api_url, date))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        return results

    async def olimp(self,
                    session: aiohttp.ClientSession,
                    api_url: str,
                    date: str,
                    sport_type: int = 1) -> str | None:
        """Получение результата события (в формате '2:3')"""
        json_data = {
            'time_shift': -240,
            'id': sport_type,
            'date': date,
            'date_end': date,
            'lang_id': '0',
            'platforma': 'SITE_CUPIS',
        }
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'baggage': 'sentry-environment=production,sentry-release=1737355356409,sentry-public_key=103e26ab0315f2335e929876414ae8d8,sentry-trace_id=aeefcf790469441094f20c20a93d4f03,sentry-sample_rate=1,sentry-sampled=true',
            'content-type': 'application/json',
            # 'cookie': 'Path=/; _sa=SA1.cfc06580-dedd-4a85-a2b1-a3b9d7b87369.1719406286; visitor_id=82cc43ab0d3e1fcb24fff0ef8242dd70; visitor_id_version=2; _ga=GA1.2.1887908695.1719406287; __exponea_etc__=aae1d5de-c0c2-4a9b-aa42-a1823a04f11f; user_ukey=b2e7f9c5-2823-40b9-90da-83bfca6c4898; __exponea_time2__=-0.05280804634094238',
            'origin': 'https://www.olimp.bet',
            'priority': 'u=1, i',
            'referer': f'https://www.olimp.bet/results?sportId={sport_type}&startDate={date}&endDate={date}&shouldSearchByChamps=false',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': 'aeefcf790469441094f20c20a93d4f03-a9d9158df858286b-1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-cupis': '1',
            'x-guid': '82cc43ab0d3e1fcb24fff0ef8242dd70',
            'x-token': '02ced4de2fab79eb6a2d08c040664335',
        }
        async with session.post(url=api_url, json=json_data, headers=headers) as response:
            result = await response.text()
        print(result)
        return result


## Out example
## {'leon$$https://leon.ru/bets/soccer/europe/uefa-europa-league/1970324845367328-besiktas-jk-athletic-bilbao': {'result': '4:1', 'event_data': {'balance_after_bet': '103', 'bet_imitation': True, 'bet_size': 22, 'betting_time': 16.43402099609375, 'bookmaker': 'leon', 'date': '2025-01-22', 'screenshot_name': '/usr/pythonProjects/Xperiment2/Client UI/screenshots/leon-2025-01-22 20-02-15.844436.png', 'start_balance': '103', 'teams': 'Бешикташ - Атлетик Бильбао', 'total_koeff': 1.7, 'total_koeff_type': 'under', 'total_nominal': '3', 'url': 'https://leon.ru/bets/soccer/europe/uefa-europa-league/1970324845367328-besiktas-jk-athletic-bilbao'}}, 'leon$$https://leon.ru/bets/soccer/qatar/stars-league/1970324845592137-al-gharafa-sc-al-ahli': {'result': '2:0', 'event_data': {'balance_after_bet': '103', 'bet_imitation': True, 'bet_size': 22, 'betting_time': 12.209675073623657, 'bookmaker': 'leon', 'date': '2025-01-22', 'screenshot_name': '/usr/pythonProjects/Xperiment2/Client UI/screenshots/leon-2025-01-22 20-25-38.747639.png', 'start_balance': '103', 'teams': 'Аль-Гарафа - Аль-Ахли', 'total_koeff': 1.75, 'total_koeff_type': 'under', 'total_nominal': '3', 'url': 'https://leon.ru/bets/soccer/qatar/stars-league/1970324845592137-al-gharafa-sc-al-ahli'}}}
