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


def start_scan(scan_params: dict) -> list:
    """
    Запуск сканирования по паре букмекеров в соответствии с заданными настройками
        Допустимые параметры словаря scan_params:
        1. first_bkmkr (первый букмекер): leon, betboom, olimp
        2. second_bkmkr (второй букмекер): leon, betboom, olimp
        3. game_type (тип игры): Soccer, Basketball, IceHockey
        4. betline (стадия игры): inplay, prematch
        5. market (тип ставки): Победитель, Тотал, Фора
        6. region (страна): country_name(lang=ru, exp: 'Россия') или all
        7. league (региональная лига): league_name(lang=ru, exp: 'NHL. Плей-офф') или all
        8. optional:
            8.1 for total: - min_k_first_bkmkr: float
                           - min_k_second_bkmkr: float
                           - corridor: float
            8.2 for winner: - min_k_home: float
                            - min_k_draw: float
                            - min_k_away: float
    """

    leon_parser = LeonParser(scan_params)
    betboom_parser = BetboomParser(scan_params)
    olimp_parser = OlimpParser(scan_params)

    match scan_params['first_bkmkr']:
        case "leon":
            first_bkmkr_parser = leon_parser
        case "betboom":
            first_bkmkr_parser = betboom_parser
        case "olimp":
            first_bkmkr_parser = olimp_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {scan_params['first_bkmkr']}!")
            return []

    match scan_params['second_bkmkr']:
        case "leon":
            second_bkmkr_parser = leon_parser
        case "betboom":
            second_bkmkr_parser = betboom_parser
        case "olimp":
            second_bkmkr_parser = olimp_parser
        case _:
            logger.error(f"Недопустимое название букмекера - {scan_params['second_bkmkr']}!")
            return []

    all_events_data = asyncio.run(get_events_data(first_bkmkr_parser, second_bkmkr_parser))
    events_map = get_events_map(all_events_data)
    analyzer = RunnersAnalysis()
    if scan_params['market'] == "Тотал":
        forks = analyzer.find_totals_forks(events_map, scan_params['optional'])
    elif scan_params['market'] == "Победитель":
        forks = analyzer.find_winner_forks(events_map, scan_params['optional'])
    else:
        return []

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
    params = {
        'first_bkmkr': "leon",
        'second_bkmkr': "olimp",
        'game_type': "Soccer",
        'betline': "prematch",
        'market': "Тотал",
        'region': "all",
        'league': "all",
        'optional': {
            'min_k_first_bkmkr': 1.9,
            'min_k_second_bkmkr': 1.9,
            'corridor': 0,
            'min_k_home': 2,
            'min_k_draw': 2,
            'min_k_away': 2
        }
    }

    res = start_scan(params)
    #print(res)