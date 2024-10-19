import os
import sys
from datetime import datetime
import logging
from logging import handlers

from . import settings

def init_logger(name):
    """Инициализация логгера"""

    match sys.platform:
        case 'linux':
            logs_path = os.getcwd() + '/' + settings.LOGS_PATH + '/'
        case 'windows':
            logs_path = os.getcwd() + '\\' + settings.LOGS_PATH + '\\'
        case _:
            logs_path = os.getcwd() + '/' + settings.LOGS_PATH + '/'

    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    match settings.LOGLEVEL:
        case "INFO":
            LOGLEVEL = logging.INFO
        case "WARNING":
            LOGLEVEL = logging.WARNING
        case "ERROR":
            LOGLEVEL = logging.ERROR
        case "CRITICAL":
            LOGLEVEL = logging.CRITICAL
        case _:
            LOGLEVEL = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(LOGLEVEL)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(settings.FORMAT))
    sh.setLevel(LOGLEVEL)

    fh = handlers.RotatingFileHandler(
        filename=logs_path + settings.FILENAME,
        encoding="UTF-8",
        maxBytes=300000,
        backupCount=5,
    )
    fh.setFormatter(logging.Formatter(settings.FORMAT))
    fh.setLevel(LOGLEVEL)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')
