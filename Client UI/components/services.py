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
    scan_prohibition_signal = QtCore.pyqtSignal(bool)
    scan_result_signal = QtCore.pyqtSignal(dict)
    scan_stopped_signal = QtCore.pyqtSignal(str)

    def __init__(self, elements_states: dict):
        super(Scanner, self).__init__()
        self.elements_states = elements_states

    def server_status_emit(self, status: str) -> None:
        """Отправка статуса сервера в GUI"""

        if status == '200' or status == '<Response [200]>':
            status = 'Status 200. The server is running'
        elif 'error' not in status.lower():
            status = f'Status {status}'
        self.server_status_signal.emit(status)

    def get_server_status(self) -> None:
        """Получение статуса сервера при запуске приложения"""

        while True:
            try:
                status = requests.get(url=settings.api_url, timeout=10).status_code
                self.server_status_emit(str(status))
                self.scan_prohibition_signal.emit(False)
                break
            except BaseException as ex:
                self.server_status_emit(f'Connection error {ex}')
                QThread.sleep(2)

    def start(self) -> dict | None:
        """Запуск сканнера и получение результатов"""
        
        with requests.session() as session:
            try:
                resp = session.get(url=settings.api_url, timeout=10)
                self.server_status_emit(str(resp))
            except BaseException as ex:
                self.server_status_emit(f'Connection error {ex}')
                self.scan_stopped_signal.emit("Сканирование остановлено")
                return

            while not QThread.currentThread().isInterruptionRequested():
                try:
                    scan_results = session.post(
                        url=settings.api_url,
                        headers={'X-CSRFToken': session.cookies['csrftoken']},
                        data=json.dumps(self.elements_states),
                        timeout=90
                    )
                    self.server_status_emit(str(scan_results.status_code))
                    if QThread.currentThread().isInterruptionRequested():
                        self.scan_stopped_signal.emit("Сканирование остановлено")
                    else:
                        self.scan_result_signal.emit(scan_results.json())
                except BaseException as ex:
                    self.server_status_emit(f'Connection error {ex}')
                    self.scan_stopped_signal.emit("Сканирование остановлено")
                    break

