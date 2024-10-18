import os
import logging
from logging import handlers
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Xperiment2.settings.base')
app = Celery('Xperiment2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks

app.conf.beat_schedule = {
    'start_pars_periodically': {
        'task': 'main.apps.scanner.tasks.start_scan',
        'schedule': crontab(minute='*/1'),
    }
}

settings.LOGGING = {}

# Настройка логирования для Celery.
@setup_logging.connect
def config_loggers(*args, **kwargs) -> None:
    logger = logging.getLogger('celery')
    logger.setLevel(logging.INFO)
    FORMAT = "%(asctime)s -- %(name)s -- %(lineno)s -- %(levelname)s -- %(message)s"

    fh_formatter = logging.Formatter(fmt=FORMAT)
    file_handler = handlers.RotatingFileHandler(
        filename=settings.LOGS_DIR_CELERY / 'Celery.log',
        maxBytes=300000,
        backupCount=5,
    )
    file_handler.setFormatter(fh_formatter)
    file_handler.setLevel('WARNING')
    logger.addHandler(file_handler)

    sh_formatter = logging.Formatter(fmt=FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(sh_formatter)
    stream_handler.setLevel('INFO')
    logger.addHandler(stream_handler)
