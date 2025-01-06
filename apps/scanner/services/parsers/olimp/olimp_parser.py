import asyncio
import aiohttp
from datetime import datetime

from apps.scanner.services.parsers import parse_settings
from celery.utils.log import get_task_logger

logger = get_task_logger('Xperiment2.apps.scanner.services.parsers.olimp.olimp_parser')

CONNECTION_ATTEMPTS = 20
CONNECTION_TIMEOUT = aiohttp.ClientTimeout(
    total=None,
    sock_connect=parse_settings.CONNECTION_TIMEOUT["sock_connect"],
    sock_read=parse_settings.CONNECTION_TIMEOUT["sock_read"]
)

########### HEADERS ##############
HEADERS = {
    'authority': 'www.olimp.bet',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'visitor_id=82cc43ab0d3e1fcb24fff0ef8242dd70; visitor_id_version=2; user_ukey=cb581955-ac5d-4074-b400-211ff12dfee6',
    'referer': 'https://www.olimp.bet/line/1',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-guid': '82cc43ab0d3e1fcb24fff0ef8242dd70',
}

#### GET URL's ####
REGIONS_AND_LEAGUES_LIST_URL = 'https://www.olimp.bet/api/v4/0/line/sports-with-categories-with-competitions?vids%5B%5D='
EVENTS_TOP_LIST_URL = 'https://www.olimp.bet/api/v4/0/line/top/sports-with-competitions-with-events?vids%5B%5D='
LEAGUES_EVENTS_LIST_URL = 'https://www.olimp.bet/api/v4/0/line/sports-with-competitions-with-events?vids%5B%5D={sport_type}%3A'
LIVE_LEAGUES_EVENTS_LIST_URL = 'https://www.olimp.bet/api/v4/0/live/sports-with-competitions-with-events?vids%5B%5D={sport_type}%3A'

#### URL FOR SELENIUM ####
SELENIUM_URL = 'https://www.olimp.bet/line/%s/%s/%s'

class OlimpParser:
    """
        Класс получения данных букмекера Leon
        Свойства:
        1. game_type (тип игры): Soccer, Basketball, IceHockey
        2. betline (стадия игры): inplay, prematch
        3. market (тип ставки): Победитель, Тотал, Фора
        4. region (страна): country_name(lang=ru, exp: 'Россия') или all
        5. league (региональная лига): league_name(lang=ru, exp: 'NHL. Плей-офф') или all
    """

    def __init__(self, scan_params: dict):
        match scan_params['game_type']:
            case "Soccer":
                self.__game_type = "1"
            case "Basketball":
                self.__game_type = "5"
            case "IceHockey":
                self.__game_type = "2"
        self.__market = scan_params['market']
        self.__betline = scan_params['betline']
        self.__region = scan_params['region']
        self.__league = scan_params['league']

    async def start_parse(self) -> list | None:
        """Запуск асинхронного парсинга, обработки результатов и получения списка данных по каждому событию (матчу)"""

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=CONNECTION_TIMEOUT) as session:

            if self.__betline == 'inplay':
                sorted_all_events_data = await asyncio.create_task(
                    self.__get_events_data(session, LIVE_LEAGUES_EVENTS_LIST_URL.format(sport_type=self.__game_type))
                )

            elif self.__betline == 'prematch':
                task_top_events = asyncio.create_task(
                    self.__get_events_data(session, EVENTS_TOP_LIST_URL)
                )
                task_leagues_events = asyncio.create_task(
                    self.__get_events_data(session, LEAGUES_EVENTS_LIST_URL.format(sport_type=self.__game_type))
                )
                all_events_data = await asyncio.gather(task_top_events, task_leagues_events)
                all_events_data = [x for y in all_events_data if y for x in y]

                sorted_all_events_data = list({v['id']: v for v in all_events_data}.values())
            else:
                return

        if sorted_all_events_data:
            return self.__process_parse_data(sorted_all_events_data)

    async def get_regions_and_leagues_list(self, session: aiohttp.ClientSession) -> dict:
        """Получение названий регионов и всех чемпионатов всех региональных лиг (имя и id)"""

        try:
            async with session.get(REGIONS_AND_LEAGUES_LIST_URL, headers=HEADERS) as r:
                common_data = await r.json()

            regions_data = {'olimp': {'regions': [], 'leagues': {}}}
            for sport_type_data in common_data:
                if sport_type_data and sport_type_data["payload"]["id"] == self.__game_type:
                    for region in sport_type_data["payload"]["categoriesWithCompetitions"]:
                        if region.get('name') and (self.__region == 'all' or self.__region == region['name']):
                            regions_data['olimp']['regions'].append(region['name'])
                            for league in region['competitions']:
                                if self.__league == 'all' or self.__league == league['name']:
                                    regions_data['olimp']['leagues'][league['name']] = league['id']

                    break
            return regions_data
        except Exception as ex:
            logger.info(f'Ошибка выполнения запроса {ex}')

    async def __get_events_data(self, session: aiohttp.ClientSession, api_url) -> list:
        """Получение данных всех событий от API"""

        try:
            async with session.get(api_url, headers=HEADERS) as r:
                common_data = await r.json()

            all_events_data_list = []
            for sport_type_data in common_data:
                if sport_type_data and sport_type_data["payload"].get("id") == self.__game_type:
                    for league in sport_type_data["payload"].get("competitionsWithEvents"):
                        if league.get('competition') and 'Статистика' in league['competition']['name']:
                            continue
                        if self.__region == 'all' and self.__league == 'all':
                            all_events_data_list.extend(league['events'])
                        elif self.__region == league['competition']['name'].split('.')[0] and \
                                self.__league == 'all':
                            all_events_data_list.extend(league['events'])
                        elif self.__league != 'all' and \
                                '.' in league['competition']['name'] and \
                                league['competition']['name'].replace(" ", "").split('.')[1]:
                            return league['events']
                break

            return all_events_data_list
        except Exception as ex:
            logger.info(f'Ошибка выполнения запроса {ex}')

    def __process_parse_data(self, all_events_data: dict) -> list:
        """Обработка данных парсинга и фомирование выходных данных в требуемом формате"""

        output_data = []
        for event_data in all_events_data:
            if not event_data:
                continue
            processed_event_data = self.__get_markets(event_data)
            if not processed_event_data.get('runners'):
                continue
            output_data.append(processed_event_data)

        return output_data

    def __get_markets(self, event_data: dict) -> dict:
        """Получение требуемых данных событий"""

        try:
            region = event_data['competitionName'].split('.')[0]
            league = event_data['competitionName']
            teams = event_data['name']
            date = datetime.fromtimestamp(event_data['startDateTime']).strftime('%Y-%m-%d')
            url = SELENIUM_URL % (event_data['sportId'], event_data['competitionId'], event_data['id'])

            runners_table = {
                'bookmaker': 'olimp',
                'region': region,
                'league': league,
                'teams': teams,
                'market': None,
                'runners': {},
                'date': date,
                'url': url
            }
        except Exception:
            return {}

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

        if 'outcomes' in event_data:
            for runner in event_data['outcomes']:
                if runner.get('groupName') == 'Исход матча (основное время)':
                    if not runners_table['market']:
                        runners_table['market'] = 'Победитель'
                        runners_table['runners'] = {'home': 0, 'draw': 0, 'away': 0}
                    match runner.get('shortName'):
                        case 'П1':
                            runners_table['runners']['home'] = float(runner.get('probability'))
                        case 'Х':
                            runners_table['runners']['draw'] = float(runner.get('probability'))
                        case 'П2':
                            runners_table['runners']['away'] = float(runner.get('probability'))
        return runners_table

    def __get_markets_total(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Тотал' """

        if 'outcomes' in event_data:
            for runner in event_data['outcomes']:
                if runner.get('tableType') == 'TOTAL':
                    if not runners_table['market']:
                        runners_table['market'] = 'Тотал'
                    handicap = str(round(float(runner.get('param')), 1))
                    if not runners_table['runners'].get(handicap):
                        runners_table['runners'][handicap] = {'under': 'closed', 'over': 'closed'}
                    if "мен" in runner.get('unprocessedName'):
                        runners_table['runners'][handicap]['under'] = float(runner.get('probability'))
                    elif "бол" in runner.get('unprocessedName'):
                        runners_table['runners'][handicap]['over'] = float(runner.get('probability'))

        return runners_table

    def __get_markets_handicap(self, event_data: dict, runners_table: dict) -> dict:
        """Отбор коэффициентов на ставку типа 'Фора' """

        if 'outcomes' in event_data:
            for runner in event_data['outcomes']:
                if runner.get('tableType') == 'HANDICAP':
                    if not runners_table['market']:
                        runners_table['market'] = 'Фора'
                    handicap = runner.get('param')
                    if not runners_table['runners'].get(handicap):
                        runners_table['runners'][handicap] = {'home': 'closed', 'away': 'closed'}
                    if "Ф1К" in runner.get('shortName'):
                        runners_table['runners'][handicap]['home'] = float(runner.get('probability'))
                    elif "Ф2К" in runner.get('shortName'):
                        runners_table['runners'][handicap]['away'] = float(runner.get('probability'))
        return runners_table


if __name__ == '__main__':
    import time
    import pprint
    # async  def starter():
    #     olimp_parser = OlimpParser(game_type="Soccer", betline="prematch")
    #     async with aiohttp.ClientSession() as session:
    #         leagues = await asyncio.create_task(olimp_parser.get_regions_and_leagues_list(session))
    #     return leagues

    olimp_parser = OlimpParser({
        'game_type': "Soccer",
        'betline': "inplay",
        'market': "Тотал",
        'region': 'all',
        'league': 'all'
    })
    for _ in range(1):
        start = time.time()
        events_data = asyncio.run(olimp_parser.start_parse())
        #events_data = asyncio.run(starter())
        work_time = time.time() - start
        #pprint.pprint(events_data)
        print(events_data)
        print(work_time)
        #pprint.pprint(events_data)
