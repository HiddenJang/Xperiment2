import os
import sys
from datetime import datetime
import logging

from . import settings

def init_logger(name):
    """Инициализация логгера"""

    match sys.platform:
        case 'linux':
            logs_path = os.getcwd() + '/'
            old_logs_path = logs_path + 'old_logs/'
        case 'windows':
            logs_path = os.getcwd() + '\\'
            old_logs_path = logs_path + 'old_logs\\'
        case _:
            logs_path = os.getcwd() + '/'
            old_logs_path = logs_path + 'old_logs/'

    if os.path.exists(logs_path + settings.FILENAME):
        if not os.path.exists(old_logs_path):
            os.mkdir(old_logs_path)
        os.rename(
            logs_path + settings.FILENAME,
            f'{old_logs_path}old_log_{datetime.now().strftime("%d.%m.%y %H.%M.%S")}.txt'
        )

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

    fh = logging.FileHandler(filename=settings.FILENAME, encoding="UTF-8")
    fh.setFormatter(logging.Formatter(settings.FORMAT))
    fh.setLevel(LOGLEVEL)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')
