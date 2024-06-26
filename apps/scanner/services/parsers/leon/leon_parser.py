import asyncio
import aiohttp
import logging

logger = logging.getLogger('Xperiment2.apps.scanner.leon.leon_parser')
CONNECTION_ATTEMPTS = 20

########### HEADERS ##############
HEADERS = {
        'authority': 'leon.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': '__ddg1_=OC5sAabmJ2sBYl94XO5J; ABTestSeed=40; qtag=a1_t3637_c41_s0; qtag_rfrr=a1_t3637_c41_s0-https://www.google.com/; ipfrom=46.0.115.45; referer=https://www.google.com/; x-app-language=ru_RU; _ga=GA1.1.1815931383.1673430555; theme=DARK; firstTheme=DARK; _ym_uid=1673430560158172264; _ym_d=1673430560; _ym_isad=2; _ga_THNYNGV4VN=GS1.1.1673430554.1.1.1673430868.0.0.0',
        'referer': 'https://leon.ru/live/soccer',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-app-browser': 'chrome',
        'x-app-env': 'prod',
        'x-app-language': 'ru_RU',
        'x-app-layout': 'desktop',
        'x-app-modernity': '2019',
        'x-app-os': 'windows',
        'x-app-platform': 'web',
        'x-app-preferred-lang': '',
        'x-app-referrer': 'https://www.google.com/',
        'x-app-rendering': 'csr',
        'x-app-skin': 'default',
        'x-app-theme': 'DARK',
        'x-app-version': '6.54.0',
    }

#### GET URL's ####
COUNTRY_LIST_URL = 'https://leon.ru/api-2/betline/sports?ctag=ru-RU&flags=urlv2'
LEAGUE_URL = 'https://leon.ru/api-2/betline/changes/all?ctag=ru-RU&vtag=9c2cd386-31e1-4ce9-a140-28e9b63a9300&league_id=%d&hideClosed=true&flags=reg,urlv2,mm2,rrc,nodup'
EVENT_URL = 'https://leon.ru/api-2/betline/event/all?ctag=ru-RU&eventId=%d&flags=reg,urlv2,mm2,rrc,nodup,smg,outv2'


class LeonParser:
    """
        Класс получения данных букмекера Leon
        Свойства:
        1. game_type (тип игры): Soccer, Basketball, IceHockey
        2. betline (стадия игры): inplay, prematch
        3. market (тип раннера): Победитель, Тотал, Фора
        4. region (страна): country_name(lang=ru, exp: 'Россия') или all
        5. league (региональная лига): league_name(lang=ru, exp: 'NHL. Плей-офф') или all
    """

    def __init__(
            self,
            game_type: str,
            betline: str = 'prematch',
            market: str = 'Победитель',
            region: str = 'all',
            league: str = 'all'
    ):

        self.__game_type = game_type
        self.__betline = betline
        self.__market = market
        self.__region = region
        self.__league = league


    async def start_parse(self):
        """Запуск асинхронного парсинга, обработки результатов и получения списка данных по каждому событию (матчу)"""

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            leagues_data = await asyncio.create_task(self.get_leagues_data(session))

            tasks = []
            for league_data in leagues_data:
                task = asyncio.create_task(self.__get_events_urls(session, league_data))
                tasks.append(task)
            events_api_urls = await asyncio.gather(*tasks)
            events_api_urls = [x for y in events_api_urls for x in y]

            tasks = []
            for event_api_url in events_api_urls:
                task = asyncio.create_task(self.__get_events_data(session, event_api_url))
                tasks.append(task)
            all_events_data = await asyncio.gather(*tasks)

        return self.__process_parse_data(all_events_data)

    async def get_countries_list(self, session: aiohttp.ClientSession) -> list:
        """Получение списка стран заданного вида спорта"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.get(COUNTRY_LIST_URL, headers=HEADERS) as r:
                    common_data = await r.json()

                countries_list = []
                for sport_type_data in common_data:
                    if sport_type_data and sport_type_data["family"] == self.__game_type:
                        for region in sport_type_data["regions"]:
                            if region.get('name'):
                                country_data = {'country_name': region.get('name')}
                                countries_list.append(country_data)
                return countries_list

            except Exception:
                continue

        logger.info(f'Критическая ошибка соединения')
        return []

    async def get_leagues_data(self, session: aiohttp.ClientSession) -> list:
        """Получение списка URL API всех лиг заданного вида спорта"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.get(COUNTRY_LIST_URL, headers=HEADERS) as r:
                    common_data = await r.json()
                    leagues_data = []
                    for sport_type_data in common_data:
                        if sport_type_data and sport_type_data["family"] == self.__game_type:
                            for region in sport_type_data["regions"]:
                                if region.get('name') and (self.__region == 'all' or self.__region == region.get('name')):
                                    for league in region["leagues"]:
                                        if self.__league == 'all' or self.__league == league.get('name'):
                                            league_data = {'league_name': league.get('name'), 'league_url': LEAGUE_URL % league["id"]}
                                            leagues_data.append(league_data)

                                            if self.__league == league.get('name'):
                                                return leagues_data

                            break
                    return leagues_data
            except Exception:
                continue

        logger.info(f'Критическая ошибка соединения')
        return []

    async def __get_events_urls(self, session: aiohttp.ClientSession, league_data: dict) -> list:
        """Получение списка URL API всех событий лиги"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.get(league_data['league_url'], headers=HEADERS) as r:
                    common_data = await r.json()
                    events_urls = []
                    for event_data in common_data["data"]:
                        if event_data["betline"] == self.__betline:
                            events_urls.append(EVENT_URL % event_data["id"])
                    return events_urls
            except Exception:
                continue

        logger.info(f'Критическая ошибка соединения')
        return []

    async def __get_events_data(self, session: aiohttp.ClientSession, event_api_url: str) -> dict:
        """Получение данных события от API"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.get(event_api_url, headers=HEADERS) as r:
                    return await r.json()
            except Exception:
                continue

        logger.info(f'Критическая ошибка соединения')
        return {}

    def __process_parse_data(self, all_events_data: dict) -> list:
        """Обработка данных парсинга и фомирование выходных данных в требуемом формате"""

        output_data = []
        for event_data in all_events_data:
            if not event_data:
                continue
            processed_event_data = self.__get_markets(event_data)
            if not processed_event_data['runners']:
                continue

            ## Формирование url для selenium ##
            id = event_data['id']
            teams = event_data['url']
            league_url = event_data['league']['url']
            region_url = event_data['league']['region']['url']
            event_url = f'https://leon.ru/bets/{self.__game_type.lower()}/{region_url}/{league_url}/{str(id)}-{teams}'
            ###################################

            processed_event_data['url'] = event_url
            output_data.append(processed_event_data)
        return output_data

    def __get_markets(self, event_data: dict) -> dict:
        """Получение требуемых данных событий"""

        runners_table = {
            'region': 'closed',
            'league': 'closed',
            'teams': 'closed',
            'market': 'closed',
            'runners': {}
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
        """Отбор коэффициентов на ставку типа 'Победитель' (1Х2)"""

        if 'markets' in event_data:
            for market in event_data['markets']:
                if (market.get('name') == 'Победитель') and market.get('open'):
                    runners_table['region'] = event_data.get('league')['region']['name']
                    runners_table['league'] = event_data.get('league')['name']
                    runners_table['teams'] = event_data.get('name')
                    runners_table['market'] = market.get('name')
                    runners_table['runners'] = {'home': 'closed', 'draw': 'closed', 'away': 'closed'}
                    for runner in market.get('runners'):
                        if runner.get('tags') == ['HOME'] and runner.get('name') == '1':
                            runners_table['runners']['home'] = runner.get('price')
                        if runner.get('tags') == ['DRAW'] and runner.get('name') == 'X':
                            runners_table['runners']['draw'] = runner.get('price')
                        if runner.get('tags') == ['AWAY'] and runner.get('name') == '2':
                            runners_table['runners']['away'] = runner.get('price')
        return runners_table

    def __get_markets_total(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Тотал' """

        if 'markets' in event_data:
            for market in event_data.get('markets'):
                if (market.get('name') == 'Тотал') and market.get('open'):
                    runners_table['region'] = event_data.get('league')['region']['name']
                    runners_table['league'] = event_data.get('league')['name']
                    runners_table['teams'] = event_data.get('name')
                    runners_table['market'] = market.get('name')
                    for runner in market.get('runners'):
                        handicap = runner.get('handicap')
                        if not runners_table['runners'].get(handicap):
                            runners_table['runners'][handicap] = {'under': 'closed', 'over': 'closed'}
                        if runner.get('tags')[0] == "UNDER":
                            runners_table['runners'][handicap]['under'] = runner.get('price')
                        elif runner.get('tags')[0] == "OVER":
                            runners_table['runners'][handicap]['over'] = runner.get('price')
        return runners_table

    def __get_markets_handicap(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Фора' """

        if 'markets' in event_data:
            for market in event_data.get('markets'):
                if (market.get('name') == 'Фора') and market.get('open'):
                    runners_table['region'] = event_data.get('league')['region']['name']
                    runners_table['league'] = event_data.get('league')['name']
                    runners_table['teams'] = event_data.get('name')
                    runners_table['market'] = market.get('name')
                    for runner in market.get('runners'):
                        handicap = runner.get('handicap')
                        if handicap == '0' and handicap in runners_table['runners'].keys():
                            handicap = '-0'
                        if runner.get('tags')[0] == "HOME":
                            runners_table['runners'][handicap] = {'home': runner.get('price')}
                        elif runner.get('tags')[0] == "AWAY":
                            runners_table['runners'][handicap] = {'away': runner.get('price')}
        return runners_table


if __name__ == '__main__':
    import time
    import pprint
    leon_parser = LeonParser(game_type="IceHockey", betline="prematch", market="Фора", region='США', league='НХЛ')
    for i in range(1):
        start = time.time()
        events_data = asyncio.run(leon_parser.start_parse())
        work_time = time.time() - start
        print(work_time)
        print(events_data)
        print(len(events_data))
        #pprint.pprint(events_data)