import asyncio
import logging

from leon.leon_parser import LeonParser
from betboom.betboom_parser import BetboomParser

from events_map import get_events_map
from runner_analysis import RunnersAnalysis

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
        1. first_bkmkr (первый букмекер): leon, betboom
        2. second_bkmkr (второй букмекер): leon, betboom
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

    match first_bkmkr:
        case "leon":
            first_bkmkr_parser = leon_parser
        case "betboom":
            first_bkmkr_parser = betboom_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {first_bkmkr}!")
            return []

    match second_bkmkr:
        case "leon":
            second_bkmkr_parser = leon_parser
        case "betboom":
            second_bkmkr_parser = betboom_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {second_bkmkr}!")
            return []

    start_time = time.time()

    all_events_data = asyncio.run(get_events_data(first_bkmkr_parser, second_bkmkr_parser))

    stop_time = time.time() - start_time
    print(stop_time)

    events_map = get_events_map(all_events_data)
    analyzer = RunnersAnalysis()
    forks = analyzer.find_winner_forks(events_map, 2.8, 3.0, 3.0)

    stop_time = time.time() - start_time
    print(f'events map len={len(events_map)}')
    print(f'forks amount={len(forks)}')
    print(forks)
    print(stop_time)



if __name__ == '__main__':
    import time

    for _ in range(10):
        start_scan(market="Победитель")