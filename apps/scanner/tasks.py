from celery import shared_task
from Xperiment2.settings.celery import app
from .services.parsers import parsing_core
from celery.utils.log import get_task_logger

logger = get_task_logger('Xperiment2.apps.scanner.tasks')

@shared_task(task_name='start_scan')
# @app.task
def start_scan(**elements_states) -> list:
    return parsing_core.start_scan(elements_states)


