from celery import shared_task
from .services.parsers import parsing_core


@shared_task(name='start_scan')
def start_scan(
        first_bkmkr: str="leon",
        second_bkmkr: str="betboom",
        game_type: str ="Soccer",
        betline: str ="prematch",
        market: str ="Тотал",
        region: str="all",
        league: str="all"
) -> list:
    return parsing_core.start_scan()

