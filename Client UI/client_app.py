import sys
import logging
import os
from datetime import datetime
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread, QSettings

from components import settings
from components import logging_init
from components.services import Scanner
from components.result_window import ResultWindow
from components.server_settings_input import ServerSettingsInput
from components.forms.client_app_template import Ui_MainWindow_client


## Принудительное переключение рабочей директории ##
file_path = Path(__file__).resolve().parent
os.chdir(file_path)

## Инициализация логгера ##
logging_init.init_logger('Client UI')
logger = logging.getLogger('Client UI.client_app')


class DesktopApp(QMainWindow):
    def __init__(self):
        super(DesktopApp, self).__init__()
        self.ui = Ui_MainWindow_client()
        self.ui.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate

        self.result_window = ResultWindow()
        self.server_set_window = ServerSettingsInput()

        self.result_window_closed = True

        self.settings = QSettings('client_app', 'Gcompany', self)
        self.load_settings()

        self.add_functions()

    ###### Add handling functions #####

    def add_functions(self) -> None:
        """Добавление функций обработки действий пользователя в GUI"""

        self.ui.pushButton_startScan.clicked.connect(self.start_scan)
        self.ui.pushButton_startScan.clicked.connect(self.open_results_window)
        self.ui.pushButton_stopScan.clicked.connect(self.stop_scan)

        self.result_window.closeResultWindow.connect(self.result_window_close_slot)
        self.result_window.closeResultWindow.connect(self.stop_scan)
        self.result_window.openResultWindow.connect(self.result_window_open_slot)

        self.ui.pushButton_connect.clicked.connect(self.request_server_status)
        self.ui.pushButton_disconnect.clicked.connect(self.disconnect_from_server)
        self.ui.comboBox_marketType.currentTextChanged.connect(self.change_koeff_labels)

        self.ui.action_serverSettings.triggered.connect(self.open_server_set_window)

    ###### Test connection slots ######

    def request_server_status(self) -> None:
        """Запрос статуса сервера"""

        self.render_diagnostics("Проверка соединения с сервером...")
        self.ui.pushButton_connect.setDisabled(True)

        api_url = self.server_set_window.get_server_address()
        self.scanner_status = Scanner(elements_states={}, api_url=api_url)
        self.get_status_thread = QThread()
        self.scanner_status.moveToThread(self.get_status_thread)
        self.get_status_thread.started.connect(self.scanner_status.get_server_status)
        self.scanner_status.server_status_signal.connect(self.render_server_status)
        self.scanner_status.stop_status_requests_signal.connect(self.get_status_thread.quit)
        self.scanner_status.stop_status_requests_signal.connect(self.change_con_buttons_states)
        self.get_status_thread.start()

    def disconnect_from_server(self) -> None:
        """Отключение от сервера"""

        if hasattr(self, 'get_status_thread'):
            self.get_status_thread.requestInterruption()
        self.ui.pushButton_disconnect.setDisabled(True)

        if not (hasattr(self, 'scanThread') and self.scanThread.isRunning()):
            self.ui.pushButton_startScan.setDisabled(True)

    ##### Change GUI elements states #####

    def change_con_buttons_states(self, context) -> None:
        """Изменение состояний кнопок подключения/отключения"""

        self.ui.pushButton_connect.setDisabled(False)
        self.render_diagnostics(context)
        self.ui.label_serverStatus.setText(self._translate("MainWindow_client", "Статус"))
        self.ui.label_serverStatus.setStyleSheet("")

    def deactivate_elements(self) -> None:
        """Деактивация элементов после начала поиска"""

        self.ui.comboBox_firstBkmkr.setDisabled(True)
        self.ui.comboBox_secondBkmkr.setDisabled(True)
        self.ui.comboBox_sportType.setDisabled(True)
        self.ui.comboBox_marketType.setDisabled(True)
        self.ui.comboBox_gameStatus.setDisabled(True)

        self.ui.doubleSpinBox_minKfirstBkmkr.setDisabled(True)
        self.ui.doubleSpinBox_minKsecondBkmkr.setDisabled(True)
        self.ui.doubleSpinBox_corridor.setDisabled(True)

        self.ui.label_firstBkmkr.setDisabled(True)
        self.ui.label_secondBkmkr.setDisabled(True)
        self.ui.label_sportType.setDisabled(True)
        self.ui.label_marketType.setDisabled(True)
        self.ui.label_gameStatus.setDisabled(True)
        self.ui.label_minKfirstBkmkr.setDisabled(True)
        self.ui.label_minKsecondBkmkr.setDisabled(True)
        self.ui.label_corridor.setDisabled(True)

        self.ui.pushButton_startScan.setDisabled(True)
        self.ui.menubar.setDisabled(True)

    def activate_elements(self) -> None:
        """Активация элементов после остановки поиска"""

        self.ui.comboBox_firstBkmkr.setDisabled(False)
        self.ui.comboBox_secondBkmkr.setDisabled(False)
        self.ui.comboBox_sportType.setDisabled(False)
        self.ui.comboBox_marketType.setDisabled(False)
        self.ui.comboBox_gameStatus.setDisabled(False)

        self.ui.doubleSpinBox_minKfirstBkmkr.setDisabled(False)
        self.ui.doubleSpinBox_minKsecondBkmkr.setDisabled(False)
        self.ui.doubleSpinBox_corridor.setDisabled(False)

        self.ui.label_firstBkmkr.setDisabled(False)
        self.ui.label_secondBkmkr.setDisabled(False)
        self.ui.label_sportType.setDisabled(False)
        self.ui.label_marketType.setDisabled(False)
        self.ui.label_gameStatus.setDisabled(False)
        self.ui.label_minKfirstBkmkr.setDisabled(False)
        self.ui.label_minKsecondBkmkr.setDisabled(False)
        self.ui.label_corridor.setDisabled(False)

        if hasattr(self, 'get_status_thread') and self.ui.label_serverStatus.text() == "Сервер активен":
            self.ui.pushButton_startScan.setDisabled(False)
        self.ui.pushButton_stopScan.setDisabled(True)

        self.ui.menubar.setDisabled(False)

    def change_koeff_labels(self) -> None:
        """Изменение названий коэффициентов"""
        match self.ui.comboBox_marketType.currentText().lower():
            case "тотал" | "фора":
                self.ui.label_minKfirstBkmkr.setText("Min коэфф. БК1")
                self.ui.label_minKsecondBkmkr.setText("Min коэфф. БК2")
                self.ui.label_corridor.setText("Коридор")
            case "победитель":
                self.ui.label_minKfirstBkmkr.setText("Min коэфф. на ком. 1")
                self.ui.label_minKsecondBkmkr.setText("Min коэфф. на ком. 2")
                self.ui.label_corridor.setText("Min коэфф. на ничью")

    ###### Slots ######

    def result_window_open_slot(self) -> None:
        """Состояние окна result_window"""

        self.result_window_closed = False

    def result_window_close_slot(self) -> None:
        """Состояние окна result_window"""

        self.result_window_closed = True

    def get_elements_states(self) -> dict:
        """Получение состояний всех элементов GUI"""

        return {
            'first_bkmkr': self.ui.comboBox_firstBkmkr.currentText().lower(),
            'second_bkmkr': self.ui.comboBox_secondBkmkr.currentText().lower(),
            'game_type': self.ui.comboBox_sportType.currentText(),
            'market': self.ui.comboBox_marketType.currentText(),
            'betline': self.ui.comboBox_gameStatus.currentText().lower(),
            'region': 'all',
            'league': 'all',
            'optional': {
                'min_k_first_bkmkr': self.ui.doubleSpinBox_minKfirstBkmkr.value(),
                'min_k_second_bkmkr': self.ui.doubleSpinBox_minKsecondBkmkr.value(),
                'corridor': self.ui.doubleSpinBox_corridor.value(),
                'min_k_home': self.ui.doubleSpinBox_minKfirstBkmkr.value(),
                'min_k_away': self.ui.doubleSpinBox_minKsecondBkmkr.value(),
                'min_k_draw': self.ui.doubleSpinBox_corridor.value(),
            }

        }

    def open_results_window(self) -> None:
        """Открытие окна вывода результатов сканирования"""

        if self.result_window_closed:
            self.result_window.show()
            self.result_window.exec_()

    def open_server_set_window(self) -> None:
        """Открытие окна настроек подключения к серверу"""

        self.server_set_window.show()
        self.server_set_window.exec_()

    def start_scan(self) -> None:
        """Запуск сканирования"""

        self.deactivate_elements()
        self.ui.pushButton_stopScan.setDisabled(False)

        elements_states = self.get_elements_states()
        api_url = self.server_set_window.get_server_address()
        self.scanner = Scanner(elements_states=elements_states, api_url=api_url)
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

        if hasattr(self, 'scanThread') and self.scanThread.isRunning():
            self.render_diagnostics("Идет завершение сканирования, ожидайте...")
            self.scanThread.requestInterruption()
        self.ui.pushButton_stopScan.setDisabled(True)

    ###### Rendering #####

    def render_diagnostics(self, info: str) -> None:
        """Вывод диагностической и системной информации"""

        message = f'{datetime.now().strftime("%d.%m.%y %H:%M:%S")}:  {info}'

        item = QtWidgets.QListWidgetItem()
        item.setText(self._translate("MainWindow_client", message))
        self.ui.listWidget_diagnostics.addItem(item)

    def render_server_status(self, status_data: dict) -> None:
        """Отображение проверки доступности сервера и активация кнопки Начать сканирование"""

        if "200" in status_data["status"]:
            if not self.ui.label_serverStatus.text() == "Сервер активен":
                self.ui.pushButton_disconnect.setDisabled(False)
                if not (hasattr(self, 'scanThread') and self.scanThread.isRunning()):
                    self.ui.pushButton_startScan.setDisabled(False)
                self.ui.label_serverStatus.setText(self._translate("MainWindow_client", "Сервер активен"))
                self.ui.label_serverStatus.setStyleSheet("background-color: rgb(15, 248, 12);border-color: rgb(0, 0, 0);")
                self.render_diagnostics("Сервер активен. Статус 200.")
        elif not self.ui.label_serverStatus.text() == "Сервер недоступен":
            self.ui.pushButton_disconnect.setDisabled(False)
            self.ui.pushButton_startScan.setDisabled(True)
            self.ui.label_serverStatus.setText(self._translate("MainWindow_client", "Сервер недоступен"))
            self.ui.label_serverStatus.setStyleSheet("background-color: rgb(246, 4, 4);border-color: rgb(0, 0, 0);")
            self.render_diagnostics(f"Сервер недоступен. Ошибка подключения: статус-код {status_data['status']} {status_data['context']}")

    def render_scan_result(self, scan_results: dict) -> None:
        """Отрисовка результатов поиска"""

        if scan_results.get('Success'):
            self.result_window.render_results(scan_results['Success'])

    ###### Save and load user settings #####

    def save_settings(self) -> None:
        ## ComboBox ##
        for combo_box in self.ui.desktopClient.findChildren(QtWidgets.QComboBox):
            self.settings.setValue(combo_box.objectName(), combo_box.currentText())
        ## DoubleSpinBox ##
        for double_spin_box in self.ui.desktopClient.findChildren(QtWidgets.QDoubleSpinBox):
            self.settings.setValue(double_spin_box.objectName(), double_spin_box.value())
        ## Label ##
        for label in self.ui.desktopClient.findChildren(QtWidgets.QLabel):
            if label.objectName() == 'label_serverStatus':
                label.setText("Статус")
            self.settings.setValue(label.objectName(), label.text())
        ## LineEdit ##
        for line_edit in self.server_set_window.findChildren(QtWidgets.QLineEdit):
            if line_edit.objectName() == 'lineEdit_serverAddress' and not line_edit.text():
                line_edit.setText(settings.API_URL)
            self.settings.setValue(line_edit.objectName(), line_edit.text())

    def load_settings(self) -> None:
        try:
            ## ComboBox ##
            for combo_box in self.ui.desktopClient.findChildren(QtWidgets.QComboBox):
                combo_box.setCurrentText(self.settings.value(combo_box.objectName()))
            ## DoubleSpinBox ##
            for double_spin_box in self.ui.desktopClient.findChildren(QtWidgets.QDoubleSpinBox):
                double_spin_box.setValue(float(self.settings.value(double_spin_box.objectName())))
            ## Label ##
            for label in self.ui.desktopClient.findChildren(QtWidgets.QLabel):
                label.setText(self.settings.value(label.objectName()))
            ## LineEdit ##
            for line_edit in self.server_set_window.findChildren(QtWidgets.QLineEdit):
                line_edit.setText(self.settings.value(line_edit.objectName()))
        except BaseException as ex:
            logger.info("Ошибка при загрузке установленных ранее состояний GUI", ex)

    def closeEvent(self, event):
        self.save_settings()
        self.close()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = DesktopApp()
        w.show()
        sys.exit(app.exec_())
    except BaseException as ex:
        logger.error(f'Ошибка цикла отображения MainWindow, error message: {ex}')
