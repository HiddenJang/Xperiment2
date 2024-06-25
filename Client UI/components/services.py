from PyQt5 import QtCore
from PyQt5.QtCore import QObject

import requests

from . import settings


class Scanner(QObject):
    """Класс запуска сканирования в отдельном потоке"""

    finishSignal = QtCore.pyqtSignal(dict)

    def __init__(self, elements_states: dict):
        super(Scanner, self).__init__()
        self.elements_states = elements_states

    def start(self):
        print(self.elements_states)
        scan_results = requests.get(url=settings.api_url, params=self.elements_states)
        print(scan_results.text)
        #self.finishSignal.emit(scan_results.text)