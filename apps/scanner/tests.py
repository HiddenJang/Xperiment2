import asyncio

import aiohttp
import requests
import logging

logger = logging.getLogger('test')

RESULT_API_URL = {'olimp': 'https://www.olimp.bet/api/results'}


class ApiResponseParser:
    """Получение результатов путем запроса к API сайта букмекера"""

    def __init__(self, active_bets_data: list):
        super(ApiResponseParser, self).__init__()
        self.active_bets_data = active_bets_data

    def start(self) -> None:
        """Запуск"""
        asyncio.run(self.start_async())

    async def start_async(self) -> list:
        results_data = {'status': 'Результаты событий получены по всем ранее сделанным ставкам',
                        'results': {}}
        tasks = []
        async with aiohttp.ClientSession() as session:
            for event_data in self.active_bets_data:

                try:
                    func = getattr(self, event_data["bookmaker"])
                except AttributeError as ex:
                    logger.info(ex)
                    continue

                task = asyncio.create_task(func(session, event_data))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        print(results)
        return results

    async def olimp(self,
                    session: aiohttp.ClientSession,
                    event_data: dict) -> str | None:
        """Получение результата события (в формате '2:3')"""

        date = event_data["date"]
        print(date)
        #sport_type = int(event_data["sport_type_num"])
        sport_type = 1
        api_url = RESULT_API_URL.get(event_data["bookmaker"])
        json_data = {
            'time_shift': -240,
            'id': 1,
            'date': '2025-01-23',
            'date_end': '2025-01-23',
            'lang_id': '0',
            'platforma': 'SITE_CUPIS',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'baggage': 'sentry-environment=production,sentry-release=1737968550226,sentry-public_key=103e26ab0315f2335e929876414ae8d8,sentry-trace_id=934fed6e31e4439b9c6c0a68143ccb5e,sentry-sample_rate=1,sentry-sampled=true',
            'content-type': 'application/json',
            # 'cookie': 'Path=/; _sa=SA1.cfc06580-dedd-4a85-a2b1-a3b9d7b87369.1719406286; visitor_id=82cc43ab0d3e1fcb24fff0ef8242dd70; visitor_id_version=2; _ga=GA1.2.1887908695.1719406287; __exponea_etc__=aae1d5de-c0c2-4a9b-aa42-a1823a04f11f; user_ukey=b2e7f9c5-2823-40b9-90da-83bfca6c4898; acceptedCookiesPolicy=1; __exponea_time2__=-0.11153674125671387',
            'origin': 'https://www.olimp.bet',
            'priority': 'u=1, i',
            'referer': 'https://www.olimp.bet/results?sportId=1&startDate=2025-01-22&endDate=2025-01-22&shouldSearchByChamps=false',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '934fed6e31e4439b9c6c0a68143ccb5e-884f10bb21cabe1e-1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-cupis': '1',
            'x-guid': '82cc43ab0d3e1fcb24fff0ef8242dd70',
            'x-token': '61d2a69d2c8872501f1c775c999b7ebc',
        }
        # headers = {
        #     'x-token': '02ced4de2fab79eb6a2d08c040664335',
        # }
        async with session.post(url=api_url, json=json_data, headers=headers) as response:
            result = await response.text()
        print(result)
        return result


if __name__ == '__main__':
    events_data = [{'balance_after_bet': '198',
                    'bet_imitation': True,
                    'bet_size': 22,
                    'betting_time': 8.484900951385498,
                    'bookmaker': 'olimp',
                    'date': '2025-01-23',
                    'screenshot_name': '/usr/pythonProjects/Xperiment2/Client UI/screenshots/olimp-2025-01-22 20-25-38.731788.png',
                    'start_balance': '198',
                    'teams': 'Аль-Гарафа - Аль-Ахли Доха',
                    'total_koeff': 1.95,
                    'total_koeff_type': 'over',
                    'total_nominal': '3',
                    'url': 'https://www.olimp.bet/line/1/675327/81514787'}]
    parser = ApiResponseParser(events_data)
    parser.start()
    #sync_request()
