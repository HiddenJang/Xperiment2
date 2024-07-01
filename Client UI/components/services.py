from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread


import requests
import json
import logging

from . import settings

logger = logging.getLogger('Client UI.services')


class Scanner(QObject):
    """Класс запуска сканирования в отдельном потоке"""
    
    server_status_signal = QtCore.pyqtSignal(str)
    scan_result_signal = QtCore.pyqtSignal(dict)

    def __init__(self, elements_states: dict):
        super(Scanner, self).__init__()
        self.elements_states = elements_states

    def get_server_status(self):
        """Получение статуса сервера"""

        try:
            resp = requests.get(url=settings.api_url, timeout=10).status_code
            if resp == 200:
                server_status = 'Status 200. Server is ready'
            else:
                server_status = f'Status {resp}'
        except ConnectionError:
            server_status = "Connection error"
        except BaseException as ex:
            server_status = str(ex)
        self.server_status_signal.emit(server_status)

    def start(self) -> dict:
        """Запуск сканнера и получение результатов"""
        
        with requests.session() as session:
            session.get(url=settings.api_url)
            scan_results = session.post(
                url=settings.api_url,
                headers={'X-CSRFToken': session.cookies['csrftoken']},
                data=json.dumps(self.elements_states)
            )
        if QThread.currentThread().isInterruptionRequested():
            self.scan_result_signal.emit({})
        else:
            self.scan_result_signal.emit(scan_results.json())
