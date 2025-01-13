import sys
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QThread, QSettings
from apscheduler.schedulers.qt import QtScheduler

from components import settings
from components import logger_init
from components.connection_service import Scanner
from components.secondary_windows.scan_result import ResultWindow
from components.secondary_windows.connection_settings import ServerSettings
from components.secondary_windows.browser_control_settings import BrowserControlSettings
from components.secondary_windows.telegram_settings import TelegramSettings
from components.templates.client_app_template import Ui_MainWindow_client
from components.browsers_control.core import BrowserControl, BetResultExtractor
from components.telegram import TelegramService
from components.statistic_management.statistic import StatisticManager

## Принудительное переключение рабочей директории ##
file_path = Path(__file__).resolve().parent
os.chdir(file_path)

## Инициализация логгера ##
logger_init.init_logger('Client UI')
logger = logging.getLogger('Client UI.client_app')


class DesktopApp(QMainWindow):
    """Класс-обертка основного окна приложения"""
    def __init__(self):
        super(DesktopApp, self).__init__()
        self.ui = Ui_MainWindow_client()
        self.ui.setupUi(self)
        # создание папки для скриншотов
        self.create_screenshot_dir()
        # добавление виджетов и настроек
        self.statusbar_message = QLabel()
        self.statusbar_message.setObjectName("statusbar_message")
        self.ui.statusbar.addWidget(self.statusbar_message)
        self._translate = QtCore.QCoreApplication.translate
        self.ui.comboBox_firstBkmkr.addItems(settings.BOOKMAKERS.keys())
        self.ui.comboBox_secondBkmkr.addItems(settings.BOOKMAKERS.keys())
        self.ui.comboBox_secondBkmkr.setCurrentIndex(1)
        # создание экземпляров вспомогательных окон
        self.result_window = ResultWindow()
        self.server_set_window = ServerSettings()
        self.browser_control_set_window = BrowserControlSettings()
        self.telegram_set_window = TelegramSettings()
        self.result_window_closed = True
        # загрузка установленных ранее пользователем состояний элементов GUI
        self.settings = QSettings('client_app', 'GuiSettings', self)
        self.active_bets_list = QSettings('client_app', 'activeBetList', self)
        self.load_settings()
        # добавление обработчиков действий пользователя в GUI
        self.add_functions()
        # добавление планировщика периодически запускаемых задач
        self.scheduler = QtScheduler()
        self.scheduler.start()
        # запуск проверки доступности сервера
        self.render_server_status()
        self.request_server_status()
        # таймер опроса состояния потока автоматического управления браузером
        self.thread_status_timer = QtCore.QTimer()
        # экземпляр менеджера ститистики для взаимодействия с файлом статистики xlsx
        self.statistic_manager = StatisticManager()
        # проверка наличия активных ставок, по которым не получен результат


    ###### Add handling functions #####

    def add_functions(self) -> None:
        """Добавление функций обработки действий пользователя в GUI"""

        self.ui.pushButton_startScan.clicked.connect(self.start_scan)
        self.ui.pushButton_startScan.clicked.connect(self.open_results_window)
        self.ui.pushButton_stopScan.clicked.connect(self.stop_scan)

        self.result_window.closeResultWindow.connect(self.result_window_close_slot)
        self.result_window.closeResultWindow.connect(self.stop_scan)
        self.result_window.openResultWindow.connect(self.result_window_open_slot)

        self.ui.comboBox_marketType.currentTextChanged.connect(self.change_coeff_labels)

        self.ui.action_serverSettings.triggered.connect(self.open_server_set_window)
        self.server_set_window.ui.buttonBox.accepted.connect(self.restart_scheduler_status_job)

        self.ui.action_browserControlSettings.triggered.connect(self.open_browser_control_set_window)
        self.browser_control_set_window.diag_signal.connect(self.render_diagnostics)

        self.ui.action_telegramSettings.triggered.connect(self.open_telegram_set_window)

        self.ui.pushButton_startAutoBet.clicked.connect(self.preload_websites_and_authorize)
        self.ui.pushButton_closeBrowsers.clicked.connect(self.close_browsers)

        self.ui.checkBox_telegramMessageSwitch.clicked.connect(self.enable_telegram_messages)
        if self.ui.checkBox_telegramMessageSwitch.isChecked():
            self.enable_telegram_messages()

    ###### Auto betting ######

    def preload_websites_and_authorize(self) -> None:
        """Запуск алгоритма автоматического размещения ставок"""
        if not os.path.exists(settings.WEBDRIVER_DIR.get(sys.platform)):
            logger.info(f"Webdriver не найден:  {settings.WEBDRIVER_DIR.get(sys.platform)} does not exist. Необходимо скачать двебдрайвер в указанную директорию")
            self.render_diagnostics(f"Webdriver не найден:  {settings.WEBDRIVER_DIR.get(sys.platform)} does not exist. Необходимо скачать двебдрайвер в указанную директорию")
            return
        self.ui.pushButton_startAutoBet.setDisabled(True)

        control_settings = self.browser_control_set_window.get_control_settings()
        excluded_urls = [x.replace('https:/', 'https://') for x in self.active_bets_list.allKeys()]
        control_settings['excluded_urls'] = excluded_urls

        if hasattr(self, 'browser_control_thread'):
            del self.browser_control_thread
        self.browser_control_thread = QThread()
        self.browser_control = BrowserControl(control_settings)
        self.browser_control.moveToThread(self.browser_control_thread)
        self.browser_control_thread.started.connect(self.browser_control.preload_sites_and_authorize)
        self.browser_control.diag_signal.connect(self.render_diagnostics)
        self.browser_control.bet_finish_signal.connect(self.add_event_to_active_bets_list_and_xlsx)
        self.browser_control.thread_finish_signal.connect(self.browser_control_thread.quit)
        self.browser_control.thread_finish_signal.connect(self.browser_control.threads_status_timer.stop)
        self.browser_control.close_all_signal.connect(self.close_browsers)
        self.browser_control_thread.start()

    def close_browsers(self) -> None:
        """Закрытие браузеров"""
        if self.browser_control_thread.isRunning():
            try:
                self.browser_control.close_browsers()
                if not self.thread_status_timer.isActive():
                    self.thread_status_timer.setInterval(500)
                    self.thread_status_timer.timeout.connect(self.thread_timer_slot)
                    self.thread_status_timer.start()
            except BaseException as ex:
                self.render_diagnostics(str(ex))
                logger.error(ex)

    def thread_timer_slot(self) -> None:
        """Проверка состояния потока автоматического управления браузером"""
        if not self.browser_control_thread.isRunning():
            self.thread_status_timer.stop()
            self.browser_control.bet_in_progress = False
            self.ui.pushButton_startAutoBet.setDisabled(False)

    def place_bet(self, scan_results: dict) -> None:
        """Сделать ставку на найденное событие"""
        if self.browser_control_thread.isRunning() and \
                not self.browser_control.bet_in_progress and \
                scan_results.get('Success'):
            BrowserControl.bet_params = self.get_autobet_settings()
            self.browser_control.start_betting(scan_results['Success'])

    def get_autobet_settings(self) -> dict:
        """Получение состояний элементов GUI фрейма НАСТРОЙКИ АВТОМАТИЧЕСКИХ СТАВОК"""
        return {self.ui.comboBox_firstBkmkr.currentText().lower(): {'bet_size': self.ui.spinBox_betSizeFirst.value(),
                                                                    'min_koeff': self.ui.doubleSpinBox_minKfirstBkmkr.value()},
                self.ui.comboBox_secondBkmkr.currentText().lower(): {'bet_size': self.ui.spinBox_betSizeSecond.value(),
                                                                     'min_koeff': self.ui.doubleSpinBox_minKsecondBkmkr.value()},
                'bet_imitation': self.ui.checkBox_betImitation.isChecked()}

    def add_event_to_active_bets_list_and_xlsx(self, event_data) -> None:
        """Добавление собятия, на которое сделана ставка, в реестр настроек для последующего получения результата"""
        for bkmkr_data in event_data:
            self.active_bets_list.setValue(bkmkr_data['url'], bkmkr_data)
        if event_data:
            self.statistic_manager.insert_data(event_data)

    def write_event_result_to_xlsx(self, event_data: list) -> None:
        """Запуск процесса получения и записи результатов события в файл xlsx"""
        if event_data:
            if hasattr(self, 'result_extraction_thread'):
                del self.result_extraction_thread
            self.result_extraction_thread = QThread()
            self.bet_result_extractor = BetResultExtractor(event_data)
            self.bet_result_extractor.moveToThread(self.result_extraction_thread)
            self.result_extraction_thread.started.connect(self.bet_result_extractor.write_event_result)
            self.bet_result_extractor.diag_signal.connect(self.render_diagnostics)
            self.bet_result_extractor.results_extracted_signal.connect(self.result_extraction_thread.quit)
            self.result_extraction_thread.start()

    ###### Test connection slots ######

    def request_server_status(self) -> None:
        """Запрос статуса сервера"""
        if not self.scheduler.get_job('get_server_status_job'):
            con_settings = self.server_set_window.get_connection_settings()
            scanner = Scanner(con_settings)
            self.scheduler.add_job(scanner.get_server_status,
                                   'interval',
                                   seconds=con_settings['status_request_interval'],
                                   id='get_server_status_job',
                                   max_instances=1)
            scanner.server_status_signal.connect(self.render_server_status)

    def restart_scheduler_status_job(self) -> None:
        """Перезапуск планировщика после изменения настроек подключения к серверу"""
        self.ui.pushButton_startScan.setDisabled(True)
        if self.scheduler.get_job('get_server_status_job'):
            self.scheduler.remove_job('get_server_status_job')
        self.request_server_status()

    ##### Change GUI elements states #####
    def deactivate_elements(self, state: bool) -> None:
        """Деактивация/активация элементов после начала поиска"""
        self.ui.comboBox_firstBkmkr.setDisabled(state)
        self.ui.comboBox_secondBkmkr.setDisabled(state)
        self.ui.comboBox_sportType.setDisabled(state)
        self.ui.comboBox_marketType.setDisabled(state)
        self.ui.comboBox_gameStatus.setDisabled(state)

        self.ui.doubleSpinBox_minKfirstBkmkr.setDisabled(state)
        self.ui.doubleSpinBox_minKsecondBkmkr.setDisabled(state)
        self.ui.doubleSpinBox_corridor.setDisabled(state)

        self.ui.label_firstBkmkr.setDisabled(state)
        self.ui.label_secondBkmkr.setDisabled(state)
        self.ui.label_sportType.setDisabled(state)
        self.ui.label_marketType.setDisabled(state)
        self.ui.label_gameStatus.setDisabled(state)
        self.ui.label_minKfirstBkmkr.setDisabled(state)
        self.ui.label_minKsecondBkmkr.setDisabled(state)
        self.ui.label_corridor.setDisabled(state)

        self.ui.pushButton_startScan.setDisabled(state)
        self.ui.pushButton_stopScan.setDisabled(not state)

        self.ui.menubar.setDisabled(state)

    def change_coeff_labels(self) -> None:
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
        """Получение состояний элементов GUI фрейма НАСТРОЙ СКАНИРОВАНИЯ"""

        return {'first_bkmkr': self.ui.comboBox_firstBkmkr.currentText().lower(),
                'second_bkmkr': self.ui.comboBox_secondBkmkr.currentText().lower(),
                'game_type': self.ui.comboBox_sportType.currentText(),
                'market': self.ui.comboBox_marketType.currentText(),
                'betline': self.ui.comboBox_gameStatus.currentText().lower(),
                'region': 'all',
                'league': 'all',
                'optional': {'min_k_first_bkmkr': self.ui.doubleSpinBox_minKfirstBkmkr.value(),
                             'min_k_second_bkmkr': self.ui.doubleSpinBox_minKsecondBkmkr.value(),
                             'corridor': self.ui.doubleSpinBox_corridor.value(),
                             'min_k_home': self.ui.doubleSpinBox_minKfirstBkmkr.value(),
                             'min_k_away': self.ui.doubleSpinBox_minKsecondBkmkr.value(),
                             'min_k_draw': self.ui.doubleSpinBox_corridor.value()}}

    def open_results_window(self) -> None:
        """Открытие окна вывода результатов сканирования"""
        if self.result_window_closed:
            self.result_window.show()
            self.result_window.exec_()

    def open_server_set_window(self) -> None:
        """Открытие окна настроек подключения к серверу"""
        self.server_set_window.widget_states = self.server_set_window.get_connection_settings()
        self.server_set_window.show()
        self.server_set_window.exec_()

    def open_browser_control_set_window(self) -> None:
        """Открытие окна настроек автоматического управления браузерами"""
        self.browser_control_set_window.show()
        self.browser_control_set_window.exec_()

    def open_telegram_set_window(self) -> None:
        """Открытие окна настроек взаимодействия с telegram"""
        self.telegram_set_window.widget_states = self.telegram_set_window.get_telegram_settings()
        self.telegram_set_window.show()
        self.telegram_set_window.exec_()

    def enable_telegram_messages(self) -> None:
        """Включение/отключение отправки сообщений в telegram"""
        if self.ui.checkBox_telegramMessageSwitch.isChecked():
            widgets_states = self.telegram_set_window.get_telegram_settings()
            TelegramService.group_id = widgets_states.get("group_id")
            TelegramService.token = widgets_states.get("token")
        TelegramService.turn_on(self.ui.checkBox_telegramMessageSwitch.isChecked())

    def start_scan(self) -> None:
        """Запуск сканирования"""
        self.deactivate_elements(True)

        elements_states = self.get_elements_states()
        con_settings = self.server_set_window.get_connection_settings()
        self.scanner = Scanner(con_settings, elements_states)

        self.scheduler.add_job(self.scanner.get_data_from_server,
                               'interval',
                               seconds=con_settings['pars_request_interval'],
                               id='scan_job',
                               coalesce=True,
                               max_instances=1)
        self.scanner.scan_result_signal.connect(self.render_scan_result)
        self.scanner.scan_result_signal.connect(self.place_bet)
        self.render_diagnostics("Сканирование запущено...")

    def stop_scan(self) -> None:
        """Останов сканирования"""
        self.ui.pushButton_stopScan.setDisabled(True)
        if hasattr(self, 'scanner'):
            self.scanner.interruption_requested = True
        if self.scheduler.get_job('scan_job'):
            self.scheduler.get_job('scan_job').remove()
            self.render_diagnostics("Сканирование остановлено пользователем")
        self.deactivate_elements(False)

    ###### Rendering #####

    def render_diagnostics(self, info: str) -> None:
        """Вывод диагностической и системной информации"""
        message = f'{datetime.now().strftime("%d.%m.%y %H:%M:%S")}:  {info}'

        item = QtWidgets.QListWidgetItem()
        item.setText(self._translate("MainWindow_client", message))
        self.ui.listWidget_diagnostics.addItem(item)

    def render_server_status(self, status_data: dict = None) -> None:
        """Отображение проверки доступности сервера и активация кнопки Начать сканирование"""

        if not status_data:
            self.ui.statusbar.showMessage("Проверка соединения с сервером...")
        elif "200" in status_data["status"]:
            if not self.scheduler.get_job('scan_job'):
                self.ui.pushButton_startScan.setDisabled(False)
            self.ui.statusbar.clearMessage()
            self.ui.statusbar.showMessage("Статус сервера: активен")
        else:
            self.ui.pushButton_startScan.setDisabled(True)
            self.ui.statusbar.clearMessage()
            self.ui.statusbar.showMessage("Статус сервера: недоступен")
            self.render_diagnostics(f"Ошибка подключения: статус-код {status_data['status']} {status_data['context']}")

    def render_scan_result(self, scan_results: dict) -> None:
        """Отрисовка результатов поиска"""
        if scan_results.get('Success'):
            self.result_window.render_results(scan_results['Success'])
        elif scan_results.get('fail'):
            self.render_diagnostics(scan_results.get('fail'))

    ###### Save and load user settings #####

    def save_settings(self) -> None:
        ## LineEdit ##
        for line_edit in self.server_set_window.findChildren(QtWidgets.QLineEdit):
            if line_edit.objectName() == 'lineEdit_serverAddress' and not line_edit.text():
                line_edit.setText(settings.DEFAULT_API_URL)
            self.settings.setValue(line_edit.objectName(), line_edit.text())

        for line_edit in self.telegram_set_window.findChildren(QtWidgets.QLineEdit):
            self.settings.setValue(line_edit.objectName(), line_edit.text())
        ## ComboBox ##
        for combo_box in self.ui.desktopClient.findChildren(QtWidgets.QComboBox):
            self.settings.setValue(combo_box.objectName(), combo_box.currentText())
        ## SpinBox ##
        for spin_box in self.ui.desktopClient.findChildren(QtWidgets.QSpinBox):
            self.settings.setValue(spin_box.objectName(), spin_box.value())

        for spin_box in self.server_set_window.findChildren(QtWidgets.QSpinBox):
            self.settings.setValue(spin_box.objectName(), spin_box.value())
        ## DoubleSpinBox ##
        for double_spin_box in self.ui.desktopClient.findChildren(QtWidgets.QDoubleSpinBox):
            self.settings.setValue(double_spin_box.objectName(), double_spin_box.value())
        ## Label ##
        for label in self.ui.desktopClient.findChildren(QtWidgets.QLabel):
            self.settings.setValue(label.objectName(), label.text())
        ## CheckBox ##
        for check_box in self.ui.desktopClient.findChildren(QtWidgets.QCheckBox):
            self.settings.setValue(check_box.objectName(), check_box.isChecked())

    def load_settings(self) -> None:
        try:
            ## LineEdit ##
            for line_edit in self.server_set_window.findChildren(QtWidgets.QLineEdit): # я уж не знаю по каким причинам, но это поле должно стоять перед DoubleSpinBox. Почемуто QT воспринимает QDoubleSpinBox как QLineEdit.
                if self.settings.value(line_edit.objectName()):
                    line_edit.setText(self.settings.value(line_edit.objectName()))

            for line_edit in self.telegram_set_window.findChildren(QtWidgets.QLineEdit):
                if self.settings.value(line_edit.objectName()):
                    line_edit.setText(self.settings.value(line_edit.objectName()))
            ## ComboBox ##
            for combo_box in self.ui.desktopClient.findChildren(QtWidgets.QComboBox):
                if self.settings.value(combo_box.objectName()):
                    combo_box.setCurrentText(self.settings.value(combo_box.objectName()))
            ## SpinBox ##
            for spin_box in self.ui.desktopClient.findChildren(QtWidgets.QSpinBox):
                if self.settings.value(spin_box.objectName()):
                    spin_box.setValue(int(self.settings.value(spin_box.objectName())))

            for spin_box in self.server_set_window.findChildren(QtWidgets.QSpinBox):
                if self.settings.value(spin_box.objectName()):
                    spin_box.setValue(int(self.settings.value(spin_box.objectName())))
            ## DoubleSpinBox ##
            for double_spin_box in self.ui.desktopClient.findChildren(QtWidgets.QDoubleSpinBox):
                if self.settings.value(double_spin_box.objectName()):
                    double_spin_box.setValue(float(self.settings.value(double_spin_box.objectName())))
            ## Label ##
            for label in self.ui.desktopClient.findChildren(QtWidgets.QLabel):
                if self.settings.value(label.objectName()):
                    label.setText(self.settings.value(label.objectName()))
            ## CheckBox ##
            for check_box in self.ui.desktopClient.findChildren(QtWidgets.QCheckBox):
                if self.settings.value(check_box.objectName()) == 'true':
                    check_box.setChecked(True)
                elif self.settings.value(check_box.objectName()) == 'false':
                    check_box.setChecked(False)

            ## Browser control settings window ##
            self.browser_control_set_window.set_control_settings_from_env()
        except BaseException as ex:
            logger.info("Ошибка при загрузке установленных ранее состояний GUI:", ex)

    def create_screenshot_dir(self):
        """Создание папки для скриншотов"""
        if not os.path.exists(settings.SCREENSHOTS_DIR):
            os.mkdir(settings.SCREENSHOTS_DIR)

    def closeEvent(self, event):
        self.save_settings()
        self.scheduler.shutdown(wait=False)
        self.result_window.close()
        self.close()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = DesktopApp()
        w.show()
        sys.exit(app.exec_())
    except BaseException as ex:
        logger.error(f'Ошибка цикла отображения MainWindow, {ex}')
