from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('MYSQL_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, "static")

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_EXTERNAL_PORT = os.environ.get('REDIS_EXTERNAL_PORT')

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_EXTERNAL_PORT}/0'  # URL брокера сообщений
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_EXTERNAL_PORT}/0'  # URL backend'а результатов