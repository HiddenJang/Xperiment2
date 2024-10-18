import copy
from celery.utils.log import get_task_logger

logger = get_task_logger('Xperiment2.apps.scanner.services.parsers.runner_analysis')

class RunnersAnalysis:
    """Класс анализа коэффициентов на различные типы ставок"""

    @staticmethod
    def find_totals_forks(
            events_data: list,
            optional: dict
    ) -> list:
        """Поиск вилок в ставках типа Тотал"""

        min_k_first_bkmkr = optional['min_k_first_bkmkr']
        min_k_second_bkmkr = optional['min_k_second_bkmkr']
        corridor = optional['corridor']

        total_forks = []
        for event_data in events_data:
            first_bkmkr_runners = event_data[0].get("runners")
            second_bkmkr_runners = event_data[1].get("runners")
            if first_bkmkr_runners and second_bkmkr_runners:
                for total_first_bkmkr in first_bkmkr_runners:  # переборка тоталов первого букмекера
                    for total_second_bkmkr in second_bkmkr_runners:  # переборка тоталов второго букмекера
                        k_first_bkmkr_under = first_bkmkr_runners[total_first_bkmkr]['under']
                        k_second_bkmkr_over = second_bkmkr_runners[total_second_bkmkr]['over']
                        k_first_bkmkr_over = first_bkmkr_runners[total_first_bkmkr]['over']
                        k_second_bkmkr_under = second_bkmkr_runners[total_second_bkmkr]['under']

                        first_bkmkr_data = copy.deepcopy(event_data[0])
                        second_bkmkr_data = copy.deepcopy(event_data[1])

                        # поиск коридора (тоталов по критериям): тотал МЕНЬШЕ первого букмекера с коэфф не менее2х и
                        # тотала БОЛЬШЕ второго букмекера с номиналом менее номинала тотала первого букмекера на
                        # величину коридора и коэфом более 2х
                        if isinstance(k_first_bkmkr_under, (float, int)) and isinstance(k_second_bkmkr_over, (float, int)) and (
                            float(total_first_bkmkr) - float(total_second_bkmkr) >= corridor
                        ) and (
                            k_first_bkmkr_under >= min_k_first_bkmkr
                        ) and (
                            k_second_bkmkr_over >= min_k_second_bkmkr
                        ):

                            first_bkmkr_data["runners"] = {total_first_bkmkr: {'under': k_first_bkmkr_under}}
                            second_bkmkr_data["runners"] = {total_second_bkmkr: {'over': k_second_bkmkr_over}}
                            total_forks.append([first_bkmkr_data, second_bkmkr_data])

                        # поиск коридора (тоталов по критериям): тотал БОЛЬШЕ первого букмекера с коэфф не менее2х и
                        # тотала МЕНЬШЕ второго букмекера с номиналом более номинала тотала первого букмекера на
                        # величину коридораи и коэфом более 2х
                        elif isinstance(k_first_bkmkr_over, (float, int)) and isinstance(k_second_bkmkr_under, (float, int)) and (
                                float(total_second_bkmkr) - float(total_first_bkmkr) >= corridor
                        ) and (
                                k_first_bkmkr_over >= min_k_first_bkmkr
                        ) and (
                                k_second_bkmkr_under >= min_k_second_bkmkr
                        ):

                            first_bkmkr_data["runners"] = {total_first_bkmkr: {'over': k_first_bkmkr_over}}
                            second_bkmkr_data["runners"] = {total_second_bkmkr: {'under': k_second_bkmkr_under}}
                            total_forks.append([first_bkmkr_data, second_bkmkr_data])

                        else:
                            continue

        return total_forks

    @staticmethod
    def find_winner_forks(
            events_data: list,
            optional: dict
    ) -> list:
        """Поиск вилок в ставках типа Победитель"""

        min_k_home = optional['min_k_home']
        min_k_draw = optional['min_k_draw']
        min_k_away = optional['min_k_away']

        winner_forks = []
        for event_data in events_data:
            first_bkmkr_runners = event_data[0].get("runners")
            second_bkmkr_runners = event_data[1].get("runners")
            if first_bkmkr_runners and second_bkmkr_runners:
                k_first_bkmkr_home = first_bkmkr_runners['home']
                k_first_bkmkr_away = first_bkmkr_runners['away']
                k_first_bkmkr_draw = first_bkmkr_runners['draw']
                k_second_bkmkr_home = second_bkmkr_runners['home']
                k_second_bkmkr_away = second_bkmkr_runners['away']
                k_second_bkmkr_draw = second_bkmkr_runners['draw']

                first_bkmkr_data = copy.deepcopy(event_data[0])
                second_bkmkr_data = copy.deepcopy(event_data[1])

                if (
                        max(k_second_bkmkr_home, k_first_bkmkr_home) >= min_k_home
                ) and (
                        max(k_second_bkmkr_draw, k_first_bkmkr_draw) >= min_k_draw
                ) and (
                        max(k_second_bkmkr_away, k_first_bkmkr_away) >= min_k_away
                ):

                    if k_second_bkmkr_home <= k_first_bkmkr_home >= min_k_home:
                        del second_bkmkr_data['runners']['home']
                    elif k_first_bkmkr_home <= k_second_bkmkr_home >= min_k_home:
                        del first_bkmkr_data['runners']['home']

                    if k_second_bkmkr_draw <= k_first_bkmkr_draw >= min_k_draw:
                        del second_bkmkr_data['runners']['draw']
                    elif k_first_bkmkr_draw <= k_second_bkmkr_draw >= min_k_draw:
                        del first_bkmkr_data['runners']['draw']

                    if k_second_bkmkr_away <= k_first_bkmkr_away >= min_k_away:
                        del second_bkmkr_data['runners']['away']
                    elif k_first_bkmkr_away <= k_second_bkmkr_away >= min_k_away:
                        del first_bkmkr_data['runners']['away']

                    winner_forks.append([first_bkmkr_data, second_bkmkr_data])

        return winner_forks


if __name__ == '__main__':
    pass


### events_data (Totals) example ##
# [{'bookmaker': 'leon', 'region': 'Россия', 'league': 'Премьер-лига', 'teams': 'Урал - Балтика', 'market': 'Тотал',
#   'runners': {'0.5': {'under': 7.8, 'over': 1.1}, '1': {'under': 6.0, 'over': 1.14},
#               '1.5': {'under': 2.65, 'over': 1.49}, '2': {'under': 2.02, 'over': 1.84},
#               '2.5': {'under': 1.57, 'over': 2.48}, '3': {'under': 1.27, 'over': 3.95},
#               '3.5': {'under': 1.2, 'over': 4.8}, '4': {'under': 1.07, 'over': 9.4},
#               '4.5': {'under': 1.06, 'over': 10.0}, '5': {'under': 1.01, 'over': 19.0},
#               '5.5': {'under': 1.01, 'over': 28.0}},
#   'url': 'https://leon.ru/bets/soccer/russia/premier-league/1970324843858340-fc-ural-yekaterinburg-baltika'},
#  {'bookmaker': 'betboom', 'region': 'Россия', 'league': 'Россия. Премьер-лига', 'teams': 'Урал - Балтика',
#   'market': 'Тотал', 'runners': {2: {'under': 1.98, 'over': 1.86}, 0.5: {'under': 7.85, 'over': 1.08},
#                                  1: {'under': 5.94, 'over': 1.13}, 1.5: {'under': 2.69, 'over': 1.47},
#                                  2.5: {'under': 1.52, 'over': 2.56}, 3: {'under': 1.26, 'over': 3.87},
#                                  3.5: {'under': 1.18, 'over': 4.92}, 4: {'under': 1.05, 'over': 10.13},
#                                  4.5: {'under': 1.04, 'over': 11.15}},
#   'url': 'https://betboom.ru/sport/EventView/18326640'}]

### events_data (Winner) example ##
# [{'bookmaker': 'leon', 'region': 'Россия', 'league': 'Премьер-лига', 'teams': 'ЦСКА - Рубин',
#   'market': 'Победитель', 'runners': {'home': 1.93, 'draw': 3.45, 'away': 4.1},
#   'url': 'https://leon.ru/bets/soccer/russia/premier-league/1970324843892744-cska-moscow-fc-rubin-kazan'},
#  {'bookmaker': 'betboom', 'region': 'Россия', 'league': 'Россия. Премьер-лига', 'teams': 'ЦСКА М - Рубин',
#   'market': 'Исход', 'runners': {'home': 1.84, 'draw': 3.47, 'away': 4.73},
#   'url': 'https://betboom.ru/sport/EventView/18326616'}]
