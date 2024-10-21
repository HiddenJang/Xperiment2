import requests
import json
import logging
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread

logger = logging.getLogger('Client UI.components.services')


class Scanner(QObject):
    """Класс запуска сканирования в отдельном потоке"""
    
    server_status_signal = QtCore.pyqtSignal(dict)
    stop_status_requests_signal = QtCore.pyqtSignal(str)

    scan_result_signal = QtCore.pyqtSignal(dict)
    scan_stopped_signal = QtCore.pyqtSignal(str)

    def __init__(self, elements_states: dict, con_settings: dict):
        super(Scanner, self).__init__()
        self.elements_states = elements_states
        self.con_settings = con_settings

    def get_server_status(self) -> None:
        """Получение статуса сервера при запуске приложения. Отправка статуса сервера в GUI"""

        while True:
            if QThread.currentThread().isInterruptionRequested():
                self.stop_status_requests_signal.emit("Проверка подключения к серверу остановлена пользователем")
                return
            try:
                status = requests.get(
                    url=self.con_settings['api_url'],
                    timeout=self.con_settings['response_timeout']
                ).status_code
                context = ''
            except BaseException as ex:
                status = ''
                context = ex
            self.server_status_signal.emit({'status': str(status), 'context': context})
            QThread.currentThread().msleep(int(self.con_settings['status_request_frequency']*1000))

    def start(self) -> dict | None:
        """Запуск сканнера и получение результатов"""
        
        with requests.session() as session:
            try:
                session.get(
                    url=self.con_settings['api_url'],
                    timeout=self.con_settings['response_timeout']
                )
            except BaseException as ex:
                self.scan_stopped_signal.emit(f"Сканирование остановлено {ex}")
                return

            while True:
                if QThread.currentThread().isInterruptionRequested():
                    self.scan_stopped_signal.emit("Сканирование остановлено пользователем")
                    return
                try:
                    scan_results = session.post(
                        url=self.con_settings['api_url'],
                        headers={'X-CSRFToken': session.cookies['csrftoken']},
                        data=json.dumps(self.elements_states),
                        timeout=90
                    )
                    self.scan_result_signal.emit(scan_results.json())
                    QThread.currentThread().msleep(int(self.con_settings['pars_request_frequency']*1000))
                except BaseException as ex:
                    self.scan_stopped_signal.emit(f"Сканирование остановлено {ex}")
                    return

