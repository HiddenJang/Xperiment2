import sys
import logging
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread

from components import logging_init
from components.services import Scanner

from Xperiment2_client import Ui_desktopClient


## Принудительное переключение рабочей директории ##
file_path = Path(__file__).resolve().parent
os.chdir(file_path)

## Инициализация логгера ##
logging_init.init_logger('Client UI')
logger = logging.getLogger('Client UI.client_app')


class DesktopApp(QMainWindow):
    def __init__(self):
        super(DesktopApp, self).__init__()
        self.ui = Ui_desktopClient()
        self.ui.setupUi(self)

        self.add_functions()

    def add_functions(self) -> None:
        """Добавление функций обработки действий пользователя в GUI"""

        self.ui.pushButton_startScan.clicked.connect(self.start_scan)
        self.ui.pushButton_stopScan.clicked.connect(self.stop_scan)

    def deactivate_elements(self) -> None:
        """Деактивация элементов после начала поиска"""

        self.ui.comboBox_firstBkmkr.setDisabled(True)
        self.ui.comboBox_secondBkmkr.setDisabled(True)
        self.ui.comboBox_sportType.setDisabled(True)
        self.ui.comboBox_marketType.setDisabled(True)
        self.ui.comboBox_gameStatus.setDisabled(True)

        self.ui.label_firstBkmkr.setDisabled(True)
        self.ui.label_secondBkmkr.setDisabled(True)
        self.ui.label_sportType.setDisabled(True)
        self.ui.label_marketType.setDisabled(True)
        self.ui.label_gameStatus.setDisabled(True)

        self.ui.pushButton_startScan.setDisabled(True)

    def activate_elements(self) -> None:
        """Активация элементов после остановки поиска"""

        self.ui.comboBox_firstBkmkr.setDisabled(False)
        self.ui.comboBox_secondBkmkr.setDisabled(False)
        self.ui.comboBox_sportType.setDisabled(False)
        self.ui.comboBox_marketType.setDisabled(False)
        self.ui.comboBox_gameStatus.setDisabled(False)

        self.ui.label_firstBkmkr.setDisabled(False)
        self.ui.label_secondBkmkr.setDisabled(False)
        self.ui.label_sportType.setDisabled(False)
        self.ui.label_marketType.setDisabled(False)
        self.ui.label_gameStatus.setDisabled(False)

        self.ui.pushButton_startScan.setDisabled(False)

    def get_elements_states(self) -> dict:
        """Получение состояний всех элементов GUI"""

        return {
            'first_bkmkr': self.ui.comboBox_firstBkmkr.currentText().lower(),
            'second_bkmkr': self.ui.comboBox_secondBkmkr.currentText().lower(),
            'game_type': self.ui.comboBox_sportType.currentText(),
            'market': self.ui.comboBox_marketType.currentText(),
            'betline': self.ui.comboBox_gameStatus.currentText().lower()
        }

    def start_scan(self) -> None:
        """Запуск сканирования"""

        self.deactivate_elements()
        elements_states = self.get_elements_states()

        self.scanner = Scanner(elements_states)
        self.scanThread = QThread()
        self.scanner.moveToThread(self.scanThread)
        self.scanThread.started.connect(self.scanner.start)
        self.scanner.finishSignal.connect(self.scanThread.quit)
        self.scanner.finishSignal.connect(self.render_scan_result)
        self.scanThread.start()

    def render_scan_result(self, scan_results: dict) -> None:
        """Отрисовка результатов поиска"""

        print(scan_results)


    def stop_scan(self) -> None:
        """Останов сканирования"""

        self.activate_elements()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = DesktopApp()
        w.show()
        sys.exit(app.exec_())
    except Exception as ex:
        DesktopApp.diagMessagesOutput(f'{time} Модуль LeakScanner, цикл отображения MainWindow, error message: {ex}')
        logger.error(f'Ошибка цикла отображения MainWindow, error message: {ex}')
