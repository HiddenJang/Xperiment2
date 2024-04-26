import asyncio
import json

import aiohttp
import logging
import requests
import pprint

logger = logging.getLogger('Xperiment2.apps.scanner.betboom.betboom_parser')
CONNECTION_ATTEMPTS = 20

########### HEADERS ##############
HEADERS_GET = {
    'authority': 'sport.betboom.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': '_ga=GA1.2.71020424.1713800846; _gid=GA1.2.123564127.1713800846; supportOnlineTalkID=BV121L6asmSNRtevELwa3vsn2d0vm1Tq; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXE95LiETeG8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=ZYxPiQ==; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXE95LiETeG8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=ZYxPiQ==; cfidsgib-w-bb=Vclgais8eMFpQszHGCfvQ6kVVs43KFbwj6V8+FRmKMtD5zu0fenT5yy9MUe0W7TJcxgcNLPayOWd5WLpPefG6m/JSFZ7r6MONYu7Or031D6KkYnXJre3xdN8EsefyHensu2/mHtgJ5FFbldYViCu/7hCv+p5TRa3k9hAbsE=; cfidsgib-w-bb=Vclgais8eMFpQszHGCfvQ6kVVs43KFbwj6V8+FRmKMtD5zu0fenT5yy9MUe0W7TJcxgcNLPayOWd5WLpPefG6m/JSFZ7r6MONYu7Or031D6KkYnXJre3xdN8EsefyHensu2/mHtgJ5FFbldYViCu/7hCv+p5TRa3k9hAbsE=',
    'if-modified-since': 'Wed, 24 Apr 2024 15:21:44 GMT',
    'referer': 'https://sport.betboom.ru/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

HEADERS_POST = {
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

############# JSON DATA FOR POST #############
json_data_countries = {
    'sportId': 1,
    'timeFilter': 0,
    'langId': 1,
    'partnerId': 147,
    'countryCode': None,
}

json_data_champs = {
    'countryId': 1343,
    'timeFilter': 0,
    'langId': 1,
    'partnerId': 147,
    'countryCode': None,
}

############ PARAMS ##############
PARAMS_PREMATCH_CHAMP_EVENTS = {
    'champId': '4584',
    'timeFilter': '0',
    'langId': '1',
    'partnerId': '147',
    'countryCode': '',
}


PARAMS_EVENT = {
    'eventId': '18117592',
    'isLive': 'false',
    'langId': '1',
    'partnerId': '147',
    'countryCode': '',
}

PARAMS_LIVE = {
    'sportId': '1',
    'checkIsActiveAndBetStatus': 'false',
    'stakeTypes': [
        '1',
        '702',
        '2',
        '3',
        '37',
    ],
    'partnerId': '147',
    'langId': '1',
    'countryCode': 'CA',
}

#### POST URL #####
COUNTRY_LIST_URL = 'https://sport.betboom.ru/Prematch/GetCountryList'
CHAMPS_LIST_URL = 'https://sport.betboom.ru/Prematch/GetChampsList'

#### GET URL ####
PREMATCH_CHAMP_EVENTS_URL = 'https://sport.betboom.ru/prematch/geteventslist'
EVENT_URL = 'https://sport.betboom.ru/common/getevent'
LIVE_URL = 'https://sport.betboom.ru/Live/GetLiveEvents'



class BetboomParser:
    """
        Класс получения данных букмекера Betboom
        Входные параметры:
        1. game_type (тип игры): 1 (Soccer), 4 (Basketball), 10 (IceHockey)
        2. betline (стадия игры): inplay, prematch
        3. market (тип раннера): Исход (Победитель), Тотал, Фора
    """

    def __init__(self, game_type, betline, market):
        self.__game_type = game_type
        self.__betline = betline
        self.__market = market

    async def start_parse(self):
        """Запуск асинхронного парсинга, обработки результатов и получения списка данных по каждому событию (матчу)"""

        async with aiohttp.ClientSession() as session:
            params_with_countries_id = await asyncio.create_task(self.__get_params_with_countries_id(session))

            tasks = []
            for params_with_country_id in params_with_countries_id:
                task = asyncio.create_task(self.__get_params_with_champs_id(session, params_with_country_id))
                tasks.append(task)
            params_with_champs_id = await asyncio.gather(*tasks)

            tasks = []
            for params_with_champ_id in params_with_champs_id:
                task = asyncio.create_task(self.__get_params_with_events_id(session, params_with_champ_id))
                tasks.append(task)
            params_with_events_id = await asyncio.gather(*tasks)

            tasks = []
            for params_with_event_id in params_with_events_id:
                task = asyncio.create_task(self.__get_events_data(session, params_with_event_id))
                tasks.append(task)
            events_data = await asyncio.gather(*tasks)
            #pprint.pprint(events_data)

        # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        #     await asyncio.create_task(self.__get_countries_params(session))

        # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        #     tasks = []
        #     for league_api_url in leagues_api_urls:
        #         task = asyncio.create_task(self.__get_events_urls(session, league_api_url))
        #         tasks.append(task)
        #     events_api_urls = await asyncio.gather(*tasks)
        #     events_api_urls = [x for y in events_api_urls for x in y]
        #
        # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        #     tasks = []
        #     for event_api_url in events_api_urls:
        #         task = asyncio.create_task(self.__get_events_data(session, event_api_url))
        #         tasks.append(task)
        #     all_events_data = await asyncio.gather(*tasks)
        #
        # return self.__process_parse_data(all_events_data)

    async def __get_params_with_countries_id(self, session: aiohttp.ClientSession) -> list:
        """Получение параметров с id стран для POST-запроса"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.post(url=COUNTRY_LIST_URL, json=json_data_countries, headers=HEADERS_POST) as r:
                    async for line in r.content:
                        countries_list = json.loads(line)

                params_with_countries_id = []
                for country in countries_list:
                    params_with_country_id = {
                        'countryId': country.get('Id'),
                        'timeFilter': 0,
                        'langId': 1,
                        'partnerId': 147,
                        'countryCode': None,
                    }
                    params_with_countries_id.append(params_with_country_id)
                return params_with_countries_id

            except Exception as ex:
                if attempt == 20:
                    logger.info(f'Критическая ошибка соединения (более 20 попыток).Событие пропущено.{ex}')
                    return []
                else:
                    continue

    async def __get_params_with_champs_id(self, session: aiohttp.ClientSession, params_with_country_id: list) -> list:
        """Получение параметров с id чампионатов каждой страны для POST-запроса"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.post(url=CHAMPS_LIST_URL, json=params_with_country_id, headers=HEADERS_POST) as r:
                    async for line in r.content:
                        champs_list = json.loads(line)

                params_with_champs_id = []
                for champ in champs_list:
                    params_with_champ_id = {
                        'champId': str(champ.get('Id')),
                        'timeFilter': '0',
                        'langId': '1',
                        'partnerId': '147',
                        'countryCode': '',
                    }
                    params_with_champs_id.append(params_with_champ_id)
                return params_with_champs_id

            except Exception as ex:
                if attempt == 20:
                    logger.info(f'Критическая ошибка соединения (более 20 попыток).Событие пропущено.{ex}')
                    return []
                else:
                    continue

    async def __get_params_with_events_id(self, session: aiohttp.ClientSession, params_with_champ_id: list) -> list:
        """Получение параметров с id событий каждого чампионата для GET-запроса"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                print('flag1')
                async with session.get(url=PREMATCH_CHAMP_EVENTS_URL, params=params_with_champ_id, headers=HEADERS_GET) as r:
                    async for line in r.content:
                        events_list = json.loads(line)
                    print('flag2')

                    print(events_list)
                params_with_events_id = []
                for event in events_list:
                    params_with_event_id = {
                        'champId': str(event.get('Id')),
                        'timeFilter': '0',
                        'langId': '1',
                        'partnerId': '147',
                        'countryCode': '',
                    }
                    params_with_events_id.append(params_with_event_id)
                return params_with_events_id

            except Exception as ex:
                if attempt == 20:
                    logger.info(f'Критическая ошибка соединения (более 20 попыток).Событие пропущено.{ex}')
                    return []
                else:
                    continue

    async def __get_events_data(self, session: aiohttp.ClientSession, params_with_event_id: list) -> list:
        """Получение параметров с id событий каждого чампионата для GET-запроса"""

        for attempt in range(CONNECTION_ATTEMPTS):
            try:
                async with session.get(url=EVENT_URL, params=params_with_event_id, headers=HEADERS_GET) as r:
                    events_data = await r.json()
                    return events_data

            except Exception as ex:
                if attempt == 20:
                    logger.info(f'Критическая ошибка соединения (более 20 попыток).Событие пропущено.{ex}')
                    return []
                else:
                    continue


if __name__ == '__main__':

    parser = BetboomParser(game_type=1, betline='prematch', market='Исход')
    asyncio.run(parser.start_parse())

    # res = requests.get(url=COUNTRYS_URL, params=PARAMS_PREMATCH, headers=HEADERS)
    # print(res)
    # r = res.json()
    # pprint.pprint(len(r))

    #res_post = requests.post(url=COUNTRY_LIST_URL, headers=HEADERS_POST, json=json_data_countries)
    #print(res_post)
    # answer = res_post.get("replies")
    # print(*answer)
    #pprint.pprint(res_post.json())