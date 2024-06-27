from PyQt5 import QtCore
from PyQt5.QtCore import QObject

import requests
import json
import logging

from . import settings

logger = logging.getLogger('Client UI.services')


class Scanner(QObject):
    """Класс запуска сканирования в отдельном потоке"""

    finishSignal = QtCore.pyqtSignal(dict)

    def __init__(self, elements_states: dict):
        super(Scanner, self).__init__()
        self.elements_states = elements_states

    def start(self):
        with requests.session() as session:
            session.get(url=settings.api_url)
            scan_results = session.post(
                url=settings.api_url,
                headers={'X-CSRFToken': session.cookies['csrftoken']},
                data=json.dumps(self.elements_states)
            )
        self.finishSignal.emit(scan_results.json())

