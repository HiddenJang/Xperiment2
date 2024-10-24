import requests
import json
import logging
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, QTimer

logger = logging.getLogger('Client UI.components.services')


class Scanner(QObject):
    """Класс запуска сканирования в отдельном потоке"""

    server_status_signal = QtCore.pyqtSignal(dict)
    scan_result_signal = QtCore.pyqtSignal(dict)

    def __init__(self, con_settings: dict, elements_states: dict = None):
        super(Scanner, self).__init__()
        self.con_settings = con_settings
        self.elements_states = elements_states

    def get_server_status(self) -> None:
        """Получение статуса сервера при запуске приложения. Отправка статуса сервера в GUI"""
        try:
            status = requests.get(url=self.con_settings['api_url'],
                                  timeout=self.con_settings['status_response_timeout']).status_code
            context = ''
        except BaseException as ex:
            status = ''
            context = ex
        self.server_status_signal.emit({'status': str(status), 'context': context})

    def get_data_from_server(self) -> dict:
        """Запуск сканнера"""
        with requests.session() as scan_session:
            try:
                scan_session.get(url=self.con_settings['api_url'],
                                 timeout=self.con_settings['pars_response_timeout'])
                scan_results = scan_session.post(url=self.con_settings['api_url'],
                                                 headers={'X-CSRFToken': scan_session.cookies['csrftoken']},
                                                 data=json.dumps(self.elements_states),
                                                 timeout=90)
                scan_results = scan_results.json()
                print(scan_results)
            except BaseException as ex:
                logger.error(f'Ошибка при попытке запроса данных от сервера {ex}')
                scan_results = {'fail': f'Ошибка при попытке запроса данных от сервера {ex}'}
            self.scan_result_signal.emit(scan_results)


