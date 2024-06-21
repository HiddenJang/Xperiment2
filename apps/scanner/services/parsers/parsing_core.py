import asyncio
import logging

from .leon.leon_parser import LeonParser
from .betboom.betboom_parser import BetboomParser
from .olimp.olimp_parser import OlimpParser
from .events_map import get_events_map
from .runner_analysis import RunnersAnalysis


logger = logging.getLogger('Xperiment2.apps.scanner.parsers.parsing_core')


async def get_events_data(first_bkmkr_parser, second_bkmkr_parser) -> list:
    """Получение всех событий двух букмекеров"""

    task_first = asyncio.create_task(first_bkmkr_parser.start_parse())
    task_second = asyncio.create_task(second_bkmkr_parser.start_parse())
    return await asyncio.gather(task_first, task_second)


def start_scan(
        first_bkmkr: str="leon",
        second_bkmkr: str="betboom",
        game_type: str ="Soccer",
        betline: str ="prematch",
        market: str ="Тотал",
        region: str="all",
        league: str="all"
) -> list:
    """
    Запуск сканирования по паре букмекеров в соответствии с заданными настройками
        Допустимые параметры:
        1. first_bkmkr (первый букмекер): leon, betboom, olimp
        2. second_bkmkr (второй букмекер): leon, betboom, olimp
        3. game_type (тип игры): Soccer, Basketball, IceHockey
        4. betline (стадия игры): inplay, prematch
        5. market (тип ставки): Победитель, Тотал, Фора
        6. region (страна): country_name(lang=ru, exp: 'Россия') или all
        7. league (региональная лига): league_name(lang=ru, exp: 'NHL. Плей-офф') или all
    """

    leon_parser = LeonParser(
                game_type=game_type,
                betline=betline,
                market=market,
                region=region,
                league=league
            )
    betboom_parser = BetboomParser(
                game_type=game_type,
                betline=betline,
                market=market,
                region=region,
                league=league
            )

    olimp_parser = OlimpParser(
                game_type=game_type,
                betline=betline,
                market=market,
                region=region,
                league=league
            )

    match first_bkmkr:
        case "leon":
            first_bkmkr_parser = leon_parser
        case "betboom":
            first_bkmkr_parser = betboom_parser
        case "olimp":
            first_bkmkr_parser = olimp_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {first_bkmkr}!")
            return []

    match second_bkmkr:
        case "leon":
            second_bkmkr_parser = leon_parser
        case "betboom":
            second_bkmkr_parser = betboom_parser
        case "olimp":
            second_bkmkr_parser = olimp_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {second_bkmkr}!")
            return []

    # start_time = time.time()

    all_events_data = asyncio.run(get_events_data(first_bkmkr_parser, second_bkmkr_parser))

    # stop_time = time.time() - start_time
    # print(stop_time)

    events_map = get_events_map(all_events_data)
    analyzer = RunnersAnalysis()
    forks = analyzer.find_totals_forks(events_map, 1.9, 1.9, 0)
    # redis_client = redis.Redis()
    # redis_client.set(name='forks', value=json.dumps(forks))

    # stop_time = time.time() - start_time
    # print(f'events map len={len(events_map)}')
    # print(f'forks amount={len(forks)}')
    # pprint.pprint(forks)
    # print(stop_time)
    return forks


if __name__ == '__main__':
    import time
    import pprint
    from leon.leon_parser import LeonParser
    from betboom.betboom_parser import BetboomParser
    from olimp.olimp_parser import OlimpParser
    from events_map import get_events_map
    from runner_analysis import RunnersAnalysis
    # for _ in range(1):
    #     res = start_scan(first_bkmkr="leon", second_bkmkr="olimp", market="Тотал")
    #     print(res)

    def start_scanner(
            first_bkmkr="leon",
            second_bkmkr="betboom",
            game_type="Soccer",
            betline="prematch",
            market="Тотал",
            region="all",
            league="all"
    ) -> list:
        return start_scan(first_bkmkr, second_bkmkr, game_type, betline, market, region, league)

    res = start_scanner()
    print(res)