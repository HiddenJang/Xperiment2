import logging

import asyncio
import aiohttp
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import webdriver
from .. import settings

logger = logging.getLogger('Client_UI.components.browsers_control.result_parsers_sync')


class SeleniumParser:
    """Получение результатов путем открытия страниц событий модулем Selenium"""
    page_load_timeout = 5

    def __init__(self, active_bets_data: dict, diag_signal: QtCore.pyqtSignal) -> None:
        self.active_bets_data = active_bets_data
        self.diag_signal = diag_signal

    def start(self) -> dict | None:
        """Открытие страниц с результатом и получение результатов событий"""
        results = {}
        driver = webdriver.Driver.get_driver(page_load_timout=SeleniumParser.page_load_timeout)
        if not driver['driver']:
            logger.error(driver['status'])
            self.diag_signal.emit(driver['status'])
            return {}
        else:
            self.driver = driver['driver']

        for event_key, event_data in self.active_bets_data.items():
            for bkmkr_data in event_data:
                bookmaker = bkmkr_data['bookmaker']

                if QThread.currentThread().isInterruptionRequested():
                    self.driver.close()
                    self.driver.quit()
                    return {}
                try:
                    func = getattr(self, bookmaker)
                except AttributeError as ex:
                    logger.info(ex)
                    continue
                result = func(bkmkr_data)
                if result:
                    results[event_key] = {'result': result, 'event_data': event_data}

        self.driver.close()
        self.driver.quit()

        if not results:
            message = 'Не удалось получить результаты событий по ранее сделанным ставкам (SELENIUM)'
        elif len(results) != len(self.active_bets_data):
            message = 'Результаты событий получены не по всем ранее сделанным ставкам (SELENIUM)'
        else:
            message = 'Результаты событий получены по всем ранее сделанным ставкам (SELENIUM)'

        logger.info(message)
        self.diag_signal.emit(message)
        return results

    def leon(self, event_data: dict) -> str | None:
        """Получение результата события (в формате '2:3')"""
        try:
            self.driver.get(event_data['url'])
        except TimeoutException:
            logger.info(
                f'Превышение времени ожидания открытия страницы {event_data["bookmaker"]} для получения результата. Попытка продолжить')
            return
        except WebDriverException as ex:
            logger.info(f'Ошибка открытия страницы {event_data["bookmaker"]}: {ex}')
            return
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'post-match-statistic-incident__score')]")))
            event_result = element.text
            return event_result
        except BaseException as ex:
            logger.info(ex)

    def olimp(self, event_data: dict) -> str | None:
        """Получение результата события (в формате '2:3')"""
        try:
            bookmaker = event_data['bookmaker']
            date = event_data['date']
            sport_type_num = event_data.get('sport_type_num')
            if not sport_type_num:
                sport_type_num = 1
            teams = event_data['teams']
            url = settings.RESULTS_URL[bookmaker] % (sport_type_num, date, date)
            try:
                self.driver.get(url)
            except TimeoutException:
                logger.info(
                    f'Превышение времени ожидания открытия страницы {bookmaker} для получения результата. Попытка продолжить')
                return
            for _ in range(20):
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            page_data = self.driver.find_element(By.ID, 'content').text.split('\n')
            if teams not in page_data:
                logger.info(f'События {teams} нет в списке завершенных событий {bookmaker}')
                return
            event_result = page_data[page_data.index(teams) + 1].split(' ')[0]
            return event_result
        except BaseException as ex:
            logger.info(ex)


class ApiResponseParser:
    """Получение результатов путем запроса к API сайта букмекера"""

    def __init__(self, active_bets_data: dict, diag_signal: QtCore.pyqtSignal) -> None:
        self.active_bets_data = active_bets_data
        self.diag_signal = diag_signal

    def start(self) -> None:
        """Запуск"""
        asyncio.run(self.start_async())

    async def start_async(self) -> dict:
        """out -> dict(event_key: result, ...)"""
        results = {}
        tasks = []
        async with aiohttp.ClientSession() as session:
            for event_key, event_data in self.active_bets_data.items():
                for bkmkr_data in event_data:
                    try:
                        func = getattr(self, bkmkr_data["bookmaker"])
                    except AttributeError as ex:
                        logger.info(ex)
                        continue

                    task = asyncio.create_task(func(session, event_key, bkmkr_data, event_data))
                    tasks.append(task)
            if tasks:
                all_results = await asyncio.gather(*tasks)
                results = {key: value for event_dict in all_results if event_dict for (key, value) in event_dict.items()}

        if not results:
            message = 'Не удалось получить результаты событий по ранее сделанным ставкам (API)'
        elif len(results) != len(self.active_bets_data):
            message = 'Результаты событий получены не по всем ранее сделанным ставкам (API)'
        else:
            message = 'Результаты событий получены по всем ранее сделанным ставкам (API)'

        logger.info(message)
        self.diag_signal.emit(message)
        return results

    # async def olimp(self,
    #                 session: aiohttp.ClientSession,
    #                 event_key: str,
    #                 bkmkr_data: str,
    #                 event_data: dict) -> dict | None:
    #     """Получение результата события (в формате '2:3')"""
    #     print(event_data)
    #     date = bkmkr_data["date"]
    #     #sport_type = int(bkmkr_data["sport_type_num"])
    #     sport_type = 1
    #     api_url = settings.RESULT_API_URL.get(bkmkr_data["bookmaker"])
    #     json_data = {
    #         'time_shift': -240,
    #         'id': sport_type,
    #         'date': date,
    #         'date_end': date,
    #         'lang_id': '0',
    #         'platforma': 'SITE_CUPIS',
    #     }
    #     headers = {
    #         'accept': 'application/json, text/plain, */*',
    #         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    #         'baggage': 'sentry-environment=production,sentry-release=1737355356409,sentry-public_key=103e26ab0315f2335e929876414ae8d8,sentry-trace_id=aeefcf790469441094f20c20a93d4f03,sentry-sample_rate=1,sentry-sampled=true',
    #         'content-type': 'application/json',
    #         # 'cookie': 'Path=/; _sa=SA1.cfc06580-dedd-4a85-a2b1-a3b9d7b87369.1719406286; visitor_id=82cc43ab0d3e1fcb24fff0ef8242dd70; visitor_id_version=2; _ga=GA1.2.1887908695.1719406287; __exponea_etc__=aae1d5de-c0c2-4a9b-aa42-a1823a04f11f; user_ukey=b2e7f9c5-2823-40b9-90da-83bfca6c4898; __exponea_time2__=-0.05280804634094238',
    #         'origin': 'https://www.olimp.bet',
    #         'priority': 'u=1, i',
    #         'referer': f'https://www.olimp.bet/results?sportId={sport_type}&startDate={date}&endDate={date}&shouldSearchByChamps=false',
    #         'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"Linux"',
    #         'sec-fetch-dest': 'empty',
    #         'sec-fetch-mode': 'cors',
    #         'sec-fetch-site': 'same-origin',
    #         'sentry-trace': 'aeefcf790469441094f20c20a93d4f03-a9d9158df858286b-1',
    #         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    #         'x-cupis': '1',
    #         'x-guid': '82cc43ab0d3e1fcb24fff0ef8242dd70',
    #         'x-token': '02ced4de2fab79eb6a2d08c040664335',
    #     }
    #     async with session.post(url=api_url, json=json_data, headers=headers) as response:
    #         result = await response.text()
    #     if result:
    #         return {event_key: {'result': result, 'event_data': event_data}}


## Input example
# {'balance_after_bet': '198',
#  'bet_imitation': True,
#  'bet_size': 22,
#  'betting_time': 8.484900951385498,
#  'bookmaker': 'olimp',
#  'date': '2025-01-22',
#  'screenshot_name': '/usr/pythonProjects/Xperiment2/Client_UI/screenshots/olimp-2025-01-22 20-25-38.731788.png',
#  'start_balance': '198',
#  'teams': 'Аль-Гарафа - Аль-Ахли Доха',
#  'total_koeff': 1.95,
#  'total_koeff_type': 'over',
#  'total_nominal': '3',
#  'url': 'https://www.olimp.bet/line/1/675327/81514787'}

## Out example
# {'leon$$https://leon.ru/bets/soccer/europe/uefa-europa-league/1970324845367328-besiktas-jk-athletic-bilbao':
#      {'result': '4:1',
#       'event_data':
#           {'balance_after_bet': '103',
#            'bet_imitation': True,
#            'bet_size': 22,
#            'betting_time': 16.43402099609375,
#            'bookmaker': 'leon',
#            'date': '2025-01-22',
#            'screenshot_name': '/usr/pythonProjects/Xperiment2/Client_UI/screenshots/leon-2025-01-22 20-02-15.844436.png',
#            'start_balance': '103',
#            'teams': 'Бешикташ - Атлетик Бильбао',
#            'total_koeff': 1.7,
#            'total_koeff_type': 'under',
#            'total_nominal': '3',
#            'url': 'https://leon.ru/bets/soccer/europe/uefa-europa-league/1970324845367328-besiktas-jk-athletic-bilbao'}},
#      'leon$$https://leon.ru/bets/soccer/qatar/stars-league/1970324845592137-al-gharafa-sc-al-ahli':
#          {'result': '2:0', 'event_data':
#              {'balance_after_bet': '103',
#               'bet_imitation': True,
#               'bet_size': 22,
#               'betting_time': 12.209675073623657,
#               'bookmaker': 'leon',
#               'date': '2025-01-22',
#               'screenshot_name': '/usr/pythonProjects/Xperiment2/Client_UI/screenshots/leon-2025-01-22 20-25-38.747639.png',
#               'start_balance': '103',
#               'teams': 'Аль-Гарафа - Аль-Ахли',
#               'total_koeff': 1.75,
#               'total_koeff_type': 'under',
#               'total_nominal': '3',
#               'url': 'https://leon.ru/bets/soccer/qatar/stars-league/1970324845592137-al-gharafa-sc-al-ahli'}}
#  }
