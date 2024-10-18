import asyncio
import aiohttp
from datetime import datetime

from apps.scanner.services.parsers import parse_settings
from celery.utils.log import get_task_logger

logger = get_task_logger('Xperiment2.apps.scanner.services.parsers.xstavka.xstavka_parser')

CONNECTION_ATTEMPTS = 20
CONNECTION_TIMEOUT = aiohttp.ClientTimeout(
    total=None,
    sock_connect=parse_settings.CONNECTION_TIMEOUT["sock_connect"],
    sock_read=parse_settings.CONNECTION_TIMEOUT["sock_read"]
)

########### HEADERS ##############
HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'SESSION=821a8470d610a923ddb2653722683447; visit=1-ac83e58d370d2de08a8adfca09b5cc33; fast_coupon=true; v3fr=1; lng=ru; flaglng=ru; typeBetNames=short; auid=vCodv2Y6W3War4fesfnLAg==; tzo=4; completed_user_settings=true; right_side=right; pushfree_status=canceled; ggru=125; _glhf=1715263551; coefview=0',
    'If-Modified-Since': 'Thu, 09 May 2024 09:11:33 GMT',
    'Referer': 'https://1xstavka.ru/line/football',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

#### GET URL's ####
LEAGUES_LIST_URL = 'https://1xstavka.ru/LineFeed/GetSportsShortZip?sports=%d&tf=2200000&tz=4&antisports=188&country=1&partner=51&virtualSports=true&gr=44'
EVENTS_LIST_URL = 'https://1xstavka.ru/LineFeed/Get1x2_VZip?sports=1&champs=%d&count=50&tf=2200000&tz=4&antisports=188&mode=4&country=1&partner=51&getEmpty=true&gr=44'
EVENT_URL = 'https://1xstavka.ru/LineFeed/GetGameZip?id=%d&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&country=1&fcountry=1&marketType=1&gr=44&isNewBuilder=true'

class XstavkaParser:
    """
        Класс получения данных букмекера Betboom
        Свойства:
        1. game_type (тип игры): Soccer (1), Basketball (3), IceHockey (2), etc...
        2. betline (стадия игры): inplay, prematch
        3. market (тип ставки): Исход (Победитель), Тотал, Фора
        4. region (страна): country_name(lang=ru, exp: 'Россия') или all
        5. league (региональная лига): league_name(lang=ru, exp: 'NHL. Плей-офф') или all
    """

    def __init__(
            self,
            game_type: int | str,
            betline: str ='prematch',
            market: str ='Исход',
            region: str ='all',
            league: str ='all'
    ):
        match game_type:
            case int():
                self.__game_type = game_type
            case "Soccer":
                self.__game_type = 1
            case "Basketball":
                self.__game_type = 3
            case "IceHockey":
                self.__game_type = 2
        self.__market = market
        self.__betline = betline
        self.__region = region
        self.__league = league

    async def start_parse(self):
        """Запуск асинхронного парсинга, обработки результатов и получения списка данных по каждому событию (матчу)"""

        if self.__betline == 'inplay':
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=CONNECTION_TIMEOUT) as session:
                all_events_data = await asyncio.create_task(self.__get_live_events_data(session))

        elif self.__betline == 'prematch':
            async with aiohttp.ClientSession(timeout=CONNECTION_TIMEOUT) as session:
                leagues_data_list = await self.get_all_leagues_data(session)

                tasks = []
                for league_data in leagues_data_list:
                    task = asyncio.create_task(self.__get_events_id(session, league_data.get("LI")))
                    tasks.append(task)
                events_id = await asyncio.gather(*tasks)
                events_id = [x for y in events_id for x in y]

                tasks = []
                for event_id in events_id:
                    task = asyncio.create_task(self.__get_event_data(session, event_id))
                    tasks.append(task)
                all_events_data = await asyncio.gather(*tasks)

        else:
            return []

        return self.__process_parse_data(all_events_data)

    async def get_all_leagues_data(self, session: aiohttp.ClientSession) -> list:
        """Получение списка id национальных лиг каждого региона (имя региона и id для дальнейшего
        GET-запроса событий каждой лиги) """

        try:
            async with session.get(url=LEAGUES_LIST_URL % self.__game_type, headers=HEADERS) as r:
                sports_data = await r.json()
            for sport_data in sports_data["Value"]:
                if sport_data["I"] == self.__game_type and sport_data.get("L"):
                    leagues_data_list = sport_data["L"]

                    if self.__league != 'all':
                        for league_data in leagues_data_list:
                            if league_data.get("L") == self.__league:
                                return [league_data]

                    return leagues_data_list

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return []

    async def __get_events_id(self, session: aiohttp.ClientSession, league_id: int) -> list:
        """Получение id событий каждого чемпионата для дальнейшего GET-запроса данных по каждому событию"""

        try:
            async with session.get(url=EVENTS_LIST_URL % league_id, headers=HEADERS) as r:
                league_events_list = await r.json()

            events_id = []
            if league_events_list.get("Value"):
                for event_data in league_events_list["Value"]:
                    events_id.append(event_data.get("CI"))

            return events_id

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return []

    async def __get_event_data(self, session: aiohttp.ClientSession, event_id: int) -> dict:
        """Получение данных prematch события по id"""

        try:
            async with session.get(url=EVENT_URL % event_id, headers=HEADERS) as r:
                common_event_data = await r.json()
            return common_event_data.get("Value")

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return {}

    # async def __get_live_events_data(self, session: aiohttp.ClientSession) -> list:
    #     """Получение данных всех LIVE-событий"""
    #
    #     try:
    #         async with session.get(url=LIVE_EVENTS_URL % self.__game_type, headers=HEADERS) as r:
    #             countries_data = await r.text()
    #
    #         events_data = []
    #         for country_data in json.loads(countries_data).get('CNT'):
    #             if country_data.get('N') == self.__region or self.__region == 'all':
    #                 for champs_data in country_data.get("CL"):
    #                     if champs_data.get('N') == self.__league or self.__league == 'all':
    #                         for event_data in champs_data.get("E"):
    #                             events_data.append(event_data)
    #         return events_data
    #
    #     except Exception:
    #         logger.info(f'Критическая ошибка соединения')
    #         return []

    def __process_parse_data(self, all_events_data: list) -> list:
        """Обработка данных парсинга и фомирование выходных данных в требуемом формате"""

        output_data = []
        for event_data in all_events_data:
            if not event_data:
                continue
            processed_event_data = self.__get_markets(event_data)
            if not processed_event_data['runners']:
                continue

            ## Формирование url для selenium ##
            sport_type = event_data['SE'].lower()
            id = event_data['CI']
            teams = f"{event_data['O1E'].lower().replace(' ', '-')}-{event_data['O2E'].lower().replace(' ', '-')}"
            league_url = f"{event_data['LI']}-{event_data['LE'].lower().replace(' ', '-')}"
            event_url = f'https://1xstavka.ru/line/{sport_type}/{league_url}/{str(id)}-{teams}'
            ###################################

            processed_event_data['url'] = event_url
            output_data.append(processed_event_data)
        return output_data

    def __get_markets(self, event_data: dict) -> dict:
        """Получение требуемых данных событий"""

        runners_table = {
            'bookmaker': 'xstavka',
            'region': 'closed',
            'league': 'closed',
            'teams': 'closed',
            'market': 'closed',
            'runners': {},
            'date': datetime.fromtimestamp(event_data['S']).strftime('%Y-%m-%d'),
        }

        if self.__market == 'Победитель':
            return self.__get_markets_winner(event_data, runners_table)
        elif self.__market == 'Тотал':
            return self.__get_markets_total(event_data, runners_table)
        elif self.__market == 'Фора':
            return self.__get_markets_handicap(event_data, runners_table)
        else:
            return {}

    def __get_markets_winner(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Исход' (1Х2)"""

        if 'GE' in event_data:
            for market in event_data['GE']:
                runners_table['region'] = event_data.get('CN')
                runners_table['league'] = event_data.get('L')
                runners_table['teams'] = f"{event_data['O1E']} - {event_data['O2E']}"
                runners_table['market'] = "Исход"
                runners_table['runners'] = {'home': 0, 'draw': 0, 'away': 0}
                for runner in market.get('E'):
                    if runner[0].get("T") == 1 and "B" not in runner[0]:
                        runners_table['runners']['home'] = runner.get('C')
                    if runner[0].get("T") == 2 and "B" not in runner[0]:
                        runners_table['runners']['draw'] = runner.get('C')
                    if runner[0].get("T") == 3 and "B" not in runner[0]:
                        runners_table['runners']['away'] = runner.get('C')
        return runners_table

    def __get_markets_total(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Тотал' """

        if 'GE' in event_data:
            for market in event_data['GE']:
                runners_table['region'] = event_data.get('CN')
                runners_table['league'] = event_data.get('L')
                runners_table['teams'] = f"{event_data['O1E']} - {event_data['O2E']}"
                runners_table['market'] = "Тотал"
                for runner in market.get('E'):
                    for item in runner:
                        if item.get('T') == 9 and "B" not in item:
                            handicap = item.get('P')
                            if not runners_table['runners'].get(handicap):
                                runners_table['runners'][handicap] = {'under': 'closed', 'over': item.get('C')}
                            else:
                                runners_table['runners'][handicap]['over'] = item.get('C')
                        elif item.get('T') == 10 and "B" not in item:
                            handicap = item.get('P')
                            if not runners_table['runners'].get(handicap):
                                runners_table['runners'][handicap] = {'under': item.get('C'), 'over': 'closed'}
                            else:
                                runners_table['runners'][handicap]['under'] = item.get('C')

        return runners_table

    def __get_markets_handicap(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Фора' """

        if 'GE' in event_data:
            for market in event_data['GE']:
                runners_table['region'] = event_data.get('CN')
                runners_table['league'] = event_data.get('L')
                runners_table['teams'] = f"{event_data['O1E']} - {event_data['O2E']}"
                runners_table['market'] = "Тотал"
                for runner in market.get('E'):
                    for item in runner:
                        if item.get('T') == 7 and "B" not in item:
                            handicap = item.get('P')
                            if not runners_table['runners'].get(handicap):
                                runners_table['runners'][handicap] = {'home': item.get('C'), 'away': 'closed'}
                            else:
                                runners_table['runners'][handicap]['home'] = item.get('C')
                        elif item.get('T') == 8 and "B" not in item:
                            handicap = item.get('P')
                            if not runners_table['runners'].get(handicap):
                                runners_table['runners'][handicap] = {'home': 'closed', 'away': item.get('C')}
                            else:
                                runners_table['runners'][handicap]['away'] = item.get('C')
        return runners_table


if __name__ == '__main__':
    import pprint
    import time

    for _ in range(10):
        start_time = time.time()
        parser = XstavkaParser(game_type=1, betline='prematch', market='Тотал')
        result = asyncio.run(parser.start_parse())
        work_time = time.time() - start_time
        print(work_time)
        pprint.pprint(result)
        print(len(result))
        #pprint.pprint(result)