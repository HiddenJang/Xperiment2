import os
from celery import Celery
from celery.schedules import crontab

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