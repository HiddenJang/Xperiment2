import os
import logging
from logging import handlers

from . import settings


def init_logger(name):
    """Инициализация логгера"""
    if not os.path.exists(settings.LOGS_PATH):
        os.mkdir(settings.LOGS_PATH)

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
        filename=settings.FILENAME,
        encoding="UTF-8",
        maxBytes=settings.MAX_BYTES_FILE_SIZE,
        backupCount=settings.LOG_FILES_COUNT,
    )
    fh.setFormatter(logging.Formatter(settings.FORMAT))
    fh.setLevel(LOGLEVEL)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')
