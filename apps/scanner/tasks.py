from celery import shared_task
from Xperiment2.settings.celery import app
from .services.parsers import parsing_core


@shared_task(task_name='start_scan')
#@app.task
def start_scan():
    res = parsing_core.start_scan(
        first_bkmkr="leon",
        second_bkmkr="betboom",
        game_type="Soccer",
        betline="prematch",
        market="Тотал",
        region="all",
        league="all"
    )
    return res
