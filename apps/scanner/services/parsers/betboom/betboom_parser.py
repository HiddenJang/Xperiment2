import asyncio
import aiohttp
import logging
import json

from apps.scanner.services.parsers import parse_settings

logger = logging.getLogger('Xperiment2.apps.scanner.betboom.betboom_parser')
CONNECTION_ATTEMPTS = 20
CONNECTION_TIMEOUT = aiohttp.ClientTimeout(
    total=None,
    sock_connect=parse_settings.CONNECTION_TIMEOUT["sock_connect"],
    sock_read=parse_settings.CONNECTION_TIMEOUT["sock_read"]
)

########### HEADERS ##############

HEADERS = {
    'authority': 'sport.betboom.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # 'cookie': '_ga=GA1.2.71020424.1713800846; _gid=GA1.2.123564127.1713800846; supportOnlineTalkID=BV121L6asmSNRtevELwa3vsn2d0vm1Tq; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXFN5JyEWfW8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=jtfpqw==; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXFN5JyEWfW8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=jtfpqw==; cfidsgib-w-bb=NZ3cuDEjBWx5XptyhUWxEkCQWTtmgMJCiqgRN0BePK67VF4VC2wYH6EM4WCbLnE6O1rqEEyedFc6XxkJTchxF5cZV6kiv9JMjeeebd7TEhhelQh9K3imcHceYI9YbWprILhfObkUOatNNxrZ0B9bOJ6dqe/D7qT/42bgGf0=; cfidsgib-w-bb=tvrDh7m5uwqNpMqh8D3xyLmo0QOmPuMJeeAqscL1YAMLUh+8EhGNPuZFoarJyzC/Rl8z8OkW7Rs7y0DMZFKCPuVvvm6tXS/+urN2FNf9OWAv/Wf5VmhO6RVvf664s9jrpQVinaDU2u1Yj0n8J0JKP28aDMoueFz/FU5a9EA=',
    'origin': 'https://sport.betboom.ru',
    'referer': 'https://sport.betboom.ru/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

#### POST URL's #####
COUNTRY_LIST_URL = 'https://sport.betboom.ru/Prematch/GetCountryList'
CHAMPS_LIST_URL = 'https://sport.betboom.ru/Prematch/GetChampsList'

#### GET URL's ####
PREMATCH_CHAMP_URL = 'https://sport.betboom.ru/prematch/geteventslist?champId=%d&timeFilter=0&langId=1&partnerId=147&countryCode='
PREMATCH_EVENT_URL = 'https://sport.betboom.ru/common/getevent?eventId=%d&isLive=false&langId=1&partnerId=147&countryCode='
LIVE_EVENTS_URL = 'https://sport.betboom.ru/live/getliveevents?sportId=%d&checkIsActiveAndBetStatus=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&partnerId=147&langId=1&countryCode='

#### URL FOR SELENIUM ####
SELENIUM_URL = 'https://betboom.ru/sport/EventView/%d'

class BetboomParser:
    """
        Класс получения данных букмекера Betboom
        Свойства:
        1. game_type (тип игры): Soccer (1), Basketball (4), IceHockey (10), etc...
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
                self.__game_type = 4
            case "IceHockey":
                self.__game_type = 10
        match market:
            case "Победитель" | "Исход":
                self.__market = "Исход"
            case _:
                self.__market = market
        self.__betline = betline
        self.__region = region
        self.__league = league

    async def start_parse(self):
        """Запуск асинхронного парсинга, обработки результатов и получения списка данных по каждому событию (матчу)"""

        if self.__betline == 'inplay':
            async with aiohttp.ClientSession(timeout=CONNECTION_TIMEOUT) as session:
                all_events_data = await asyncio.create_task(self.__get_live_events_data(session))

        elif self.__betline == 'prematch':
            async with aiohttp.ClientSession(timeout=CONNECTION_TIMEOUT) as session:
                champs_data_list = await self.get_all_leagues_data(session)
                champs_id_list = [x for y in champs_data_list['betboom'].values() for x in y]

                tasks = []
                for champ_id in champs_id_list:
                    task = asyncio.create_task(self.__get_events_id(session, champ_id))
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

    async def get_all_leagues_data(self, session: aiohttp.ClientSession) -> dict:
        """Получение списка id национальных лиг каждого региона (имя страны и параметры с id для дальнейшего POST-запроса) """

        countries_data_list = await asyncio.create_task(self.__get_regions_list(session))

        tasks = []
        for country_data in countries_data_list.items():
            task = asyncio.create_task(self.__get_leagues_data(session, country_data))
            tasks.append(task)
        champs_data_list = await asyncio.gather(*tasks)
        champs_data_list = {'betboom': {x: z for y in champs_data_list for x, z in zip(y.keys(), y.values())}}
        return champs_data_list

    async def __get_regions_list(self, session: aiohttp.ClientSession) -> dict:
        """Получение списка регионов (имя страны и параметры с id для дальнейшего POST-запроса лиг каждого региона) """

        try:
            json_data = {
                'sportId': self.__game_type,
                'timeFilter': 0,
                'langId': 1,
                'partnerId': 147,
                'countryCode': None,
            }
            async with session.post(url=COUNTRY_LIST_URL, json=json_data, headers=HEADERS) as r:
                countries_list = await r.text()

            countries_data_list = {}
            for country in json.loads(countries_list):
                if country.get('N') and (self.__region == 'all' or self.__region == country.get('N')):
                    req_params = {
                        'countryId': country.get('Id'),
                        'timeFilter': 0,
                        'langId': 1,
                        'partnerId': 147,
                        'countryCode': None,
                    }
                    countries_data_list[country.get('N')] = req_params
                    if self.__region == country.get('N'):
                        return countries_data_list

            return countries_data_list

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return {'betboom': {}}



    async def __get_leagues_data(self, session: aiohttp.ClientSession, country_data: dict) -> dict:
        """Получение данных чемпионата (имя чемпионата и id для дальнейшего GET-запроса событий)"""

        country_name = country_data[0]
        params = country_data[1]

        try:
            async with session.post(url=CHAMPS_LIST_URL, json=params, headers=HEADERS) as r:
                champs_list = await r.text()

            champs_data_list = {country_name: []}
            for champ in json.loads(champs_list):
                if champ.get('N') and (self.__league == 'all' or self.__league == champ.get('N')):
                    champs_data_list[country_name].append(champ.get('Id'))
                    if self.__league == champ.get('N'):
                        return champs_data_list
            return champs_data_list

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return {}



    async def __get_events_id(self, session: aiohttp.ClientSession, champ_id: dict) -> list:
        """Получение id событий каждого чемпионата для дальнейшего GET-запроса данных по каждому событию"""

        try:
            async with session.get(url=PREMATCH_CHAMP_URL % champ_id, headers=HEADERS) as r:
                events_list = await r.text()

            events_id = []
            for event in json.loads(events_list):
                if event.get('Id'):
                    events_id.append(event.get('Id'))
            return events_id

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return []



    async def __get_event_data(self, session: aiohttp.ClientSession, event_id: list) -> list:
        """Получение данных prematch события по id"""

        try:
            async with session.get(url=PREMATCH_EVENT_URL % event_id, headers=HEADERS) as r:
                common_event_data = await r.text()
            for event_data in json.loads(common_event_data):
                if event_data.get("PN") == "":
                    return event_data
            return []

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return []

    async def __get_live_events_data(self, session: aiohttp.ClientSession) -> list:
        """Получение данных всех LIVE-событий"""

        try:
            async with session.get(url=LIVE_EVENTS_URL % self.__game_type, headers=HEADERS) as r:
                countries_data = await r.text()

            events_data = []
            for country_data in json.loads(countries_data).get('CNT'):
                if country_data.get('N') == self.__region or self.__region == 'all':
                    for champs_data in country_data.get("CL"):
                        if champs_data.get('N') == self.__league or self.__league == 'all':
                            for event_data in champs_data.get("E"):
                                events_data.append(event_data)
            return events_data

        except Exception:
            logger.info(f'Критическая ошибка соединения')
            return []

    def __process_parse_data(self, all_events_data: list) -> list:
        """Обработка данных парсинга и фомирование выходных данных в требуемом формате"""

        output_data = []
        for event_data in all_events_data:
            if not event_data:
                continue
            processed_event_data = self.__get_markets(event_data)
            if not processed_event_data['runners']:
                continue
            output_data.append(processed_event_data)
        return output_data

    def __get_markets(self, event_data: dict) -> dict:
        """Получение требуемых данных событий"""

        runners_table = {
            'bookmaker': 'betboom',
            'region': 'closed',
            'league': 'closed',
            'teams': 'closed',
            'market': 'closed',
            'runners': {},
            'url': SELENIUM_URL % event_data['Id']
        }

        if self.__market == 'Исход':
            return self.__get_markets_winner(event_data, runners_table)
        elif self.__market == 'Тотал':
            return self.__get_markets_total(event_data, runners_table)
        elif self.__market == 'Фора':
            return self.__get_markets_handicap(event_data, runners_table)
        else:
            return {}

    def __get_markets_winner(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Исход' (1Х2)"""

        if 'StakeTypes' in event_data:
            for market in event_data['StakeTypes']:
                if market.get('N') == 'Исход':
                    runners_table['region'] = event_data.get('CtN')
                    runners_table['league'] = event_data.get('CN')
                    runners_table['teams'] = event_data.get('N')
                    runners_table['market'] = market.get('N')
                    runners_table['runners'] = {'home': 'closed', 'draw': 'closed', 'away': 'closed'}
                    for runner in market.get('Stakes'):
                        if runner.get('N') == 'П1' and runner.get("IsA"):
                            runners_table['runners']['home'] = runner.get('F')
                        if runner.get('N') == 'X' and runner.get('IsA'):
                            runners_table['runners']['draw'] = runner.get('F')
                        if runner.get('N') == 'П2' and runner.get('IsA'):
                            runners_table['runners']['away'] = runner.get('F')
        return runners_table

    def __get_markets_total(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Тотал' """

        if 'StakeTypes' in event_data:
            for market in event_data['StakeTypes']:
                if market.get('N') == 'Тотал':
                    runners_table['region'] = event_data.get('CtN')
                    runners_table['league'] = event_data.get('CN')
                    runners_table['teams'] = event_data.get('N')
                    runners_table['market'] = market.get('N')
                    for runner in market.get('Stakes'):
                        handicap = runner.get('A')
                        if not runners_table['runners'].get(handicap):
                            runners_table['runners'][handicap] = {'under': 'closed', 'over': 'closed'}
                        if runner.get('N') == "Меньше" and runner.get("IsA"):
                            runners_table['runners'][handicap]['under'] = runner.get('F')
                        elif runner.get('N') == "Больше" and runner.get("IsA"):
                            runners_table['runners'][handicap]['over'] = runner.get('F')
        return runners_table

    def __get_markets_handicap(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Фора' """

        if 'StakeTypes' in event_data:
            for market in event_data['StakeTypes']:
                if market.get('N') == 'Фора':
                    runners_table['region'] = event_data.get('CtN')
                    runners_table['league'] = event_data.get('CN')
                    runners_table['teams'] = event_data.get('N')
                    runners_table['market'] = market.get('N')
                    for runner in market.get('Stakes'):
                        handicap = runner.get('A')
                        if handicap == 0 and handicap in runners_table['runners'].keys():
                            handicap = '-0'
                        if "Фора1" in runner.get('N') and runner.get("IsA"):
                            runners_table['runners'][handicap] = {'home': runner.get('F')}
                        elif "Фора2" in runner.get('N') and runner.get("IsA"):
                            runners_table['runners'][handicap] = {'away': runner.get('F')}

        return runners_table


if __name__ == '__main__':
    import pprint
    import time

    for _ in range(10):
        start_time = time.time()
        parser = BetboomParser(game_type=1, betline='prematch', market='Тотал')
        result = asyncio.run(parser.start_parse())
        work_time = time.time() - start_time
        print(work_time)
        pprint.pprint(result)
        print(len(result))
        #pprint.pprint(result)