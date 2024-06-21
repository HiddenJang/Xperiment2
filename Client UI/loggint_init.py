import os
from datetime import datetime
import logging


def init_logger(name):
    """Инициализация логгеров"""

    logs_path = os.getcwd() + '\\'
    if os.path.exists(logs_path + 'Logs.txt'):
        if not os.path.exists(logs_path + 'old_logs'):
            os.mkdir(logs_path + 'old_logs')
        os.rename(
            f'{logs_path}Logs.txt',
            f'{logs_path + "old_logs"}\\old_Log_{datetime.now().strftime("%d.%m.%y %H.%M")}.txt'
        )

    logger = logging.getLogger(name)
    FORMAT = "%(asctime)s -- %(name)s -- %(lineno)s -- %(levelname)s -- %(message)s"
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename="Logs.txt", encoding="UTF-8")
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')