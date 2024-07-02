import sys
import logging
import os
from datetime import datetime
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread

from components import logging_init
from components.services import Scanner

from forms.client_app_template import Ui_desktopClient
from forms.result_window import ResultWindow

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
        self._translate = QtCore.QCoreApplication.translate

        self.result_window = ResultWindow()
        self.result_window_closed = True

        self.add_functions()
        self.request_server_status()

    def add_functions(self) -> None:
        """Добавление функций обработки действий пользователя в GUI"""

        self.ui.pushButton_startScan.clicked.connect(self.start_scan)
        self.ui.pushButton_startScan.clicked.connect(self.open_results_window)
        self.ui.pushButton_stopScan.clicked.connect(self.stop_scan)

        self.result_window.closeResultWindow.connect(self.result_window_close_slot)
        self.result_window.openResultWindow.connect(self.result_window_open_slot)

    def request_server_status(self) -> None:
        """Запрос статуса сервера"""

        self.render_diagnostics("Проверка соединения с сервером...")

        self.scanner_status = Scanner({})
        self.get_status_thread = QThread()
        self.scanner_status.moveToThread(self.get_status_thread)
        self.get_status_thread.started.connect(self.scanner_status.get_server_status)
        self.scanner_status.server_status_signal.connect(self.render_diagnostics)
        self.scanner_status.server_status_signal.connect(self.render_server_status)
        self.scanner_status.server_status_signal.connect(self.get_status_thread.quit)
        self.scanner_status.scan_prohibition_signal.connect(self.ui.pushButton_startScan.setDisabled)
        self.get_status_thread.start()

    def result_window_open_slot(self) -> None:
        """Отображение состояния окна result_window"""

        self.result_window_closed = False

    def result_window_close_slot(self) -> None:
        """Отображение состояния окна result_window"""

        self.result_window_closed = True

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
        self.ui.pushButton_stopScan.setDisabled(True)

    def get_elements_states(self) -> dict:
        """Получение состояний всех элементов GUI"""

        return {
            'first_bkmkr': self.ui.comboBox_firstBkmkr.currentText().lower(),
            'second_bkmkr': self.ui.comboBox_secondBkmkr.currentText().lower(),
            'game_type': self.ui.comboBox_sportType.currentText(),
            'market': self.ui.comboBox_marketType.currentText(),
            'betline': self.ui.comboBox_gameStatus.currentText().lower()
        }

    def open_results_window(self) -> None:
        """Открытие окна вывода результатов сканирования"""

        if self.result_window_closed:
            self.result_window.show()
            self.result_window.exec_()

    def start_scan(self) -> None:
        """Запуск сканирования"""

        self.deactivate_elements()
        self.ui.pushButton_stopScan.setDisabled(False)
        elements_states = self.get_elements_states()

        self.scanner = Scanner(elements_states)
        self.scanThread = QThread()
        self.scanner.moveToThread(self.scanThread)
        self.scanThread.started.connect(self.scanner.start)

        self.scanner.server_status_signal.connect(self.render_diagnostics)
        self.scanner.server_status_signal.connect(self.render_server_status)

        self.scanner.scan_result_signal.connect(self.render_scan_result)

        self.scanner.scan_stopped_signal.connect(self.activate_elements)
        self.scanner.scan_stopped_signal.connect(self.render_diagnostics)
        self.scanner.scan_stopped_signal.connect(self.scanThread.quit)

        self.scanThread.start()
        self.render_diagnostics("Сканирование запущено...")

    def stop_scan(self) -> None:
        """Останов сканирования"""

        self.render_diagnostics("Идет завершение сканирования, ожидайте...")
        if hasattr(self, 'scanThread'):
            self.scanThread.requestInterruption()
        self.ui.pushButton_stopScan.setDisabled(True)

    ###### Rendering #####

    def render_diagnostics(self, info: str) -> None:
        """Вывод диагностической и системной информации"""

        message = f'{datetime.now().strftime("%d.%m.%y %H:%M:%S")}:  {info}'

        item = QtWidgets.QListWidgetItem()
        item.setText(self._translate("desktopClient", message))
        self.ui.listWidget_diagnostics.addItem(item)

    def render_server_status(self, info: str) -> None:
        """Отображение проверки доступности сервера и активация кнопки Начать сканирование"""

        if "Status 200" in info:
            self.ui.label_serverStatus.setText(self._translate("desktopClient", "Сервер активен"))
            self.ui.label_serverStatus.setStyleSheet("background-color: rgb(15, 248, 12);border-color: rgb(0, 0, 0);")
        else:
            self.ui.label_serverStatus.setText(self._translate("desktopClient", "Сервер недоступен"))
            self.ui.label_serverStatus.setStyleSheet("background-color: rgb(246, 4, 4);border-color: rgb(0, 0, 0);")

    def render_scan_result(self, scan_results: dict) -> None:
        """Отрисовка результатов поиска"""

        if scan_results:
            self.result_window.render_results(scan_results)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = DesktopApp()
        w.show()
        sys.exit(app.exec_())
    except BaseException as ex:
        #DesktopApp.diagMessagesOutput(f'{time} Модуль LeakScanner, цикл отображения MainWindow, error message: {ex}')
        logger.error(f'Ошибка цикла отображения MainWindow, error message: {ex}')
