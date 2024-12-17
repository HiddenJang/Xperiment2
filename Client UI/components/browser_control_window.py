from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog

from .templates.browser_control_window_template import Ui_browser_control_settings
from . import settings


class BrowserControlSettings(Ui_browser_control_settings, QDialog):
    """Класс-обертка для окна настроек автоматического управления браузерами"""

    widget_states = {}

    def __init__(self):
        super(BrowserControlSettings, self).__init__()
        self.ui = Ui_browser_control_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.close_without_saving)

    def get_control_settings(self) -> dict:
        """Получение состояний виджетов окна настроек управления браузерами"""

        states = {}
        for bkmkr_name in settings.BOOKMAKERS.keys():
            states[bkmkr_name] = {'login': '', 'password': ''}
            for line_edit in self.findChildren(QtWidgets.QLineEdit):
                if bkmkr_name in line_edit.objectName().lower() and 'login' in line_edit.objectName().lower():
                    states[bkmkr_name]['login'] = line_edit.text()
                elif bkmkr_name in line_edit.objectName().lower() and 'password' in line_edit.objectName().lower():
                    states[bkmkr_name]['password'] = line_edit.text()
        return states

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""
        for bkmkr_name in self.widget_states.keys():
            for line_edit in self.findChildren(QtWidgets.QLineEdit):
                if bkmkr_name in line_edit.objectName().lower() and 'login' in line_edit.objectName().lower():
                    line_edit.setText(self.widget_states[bkmkr_name]['login'])
                elif bkmkr_name in line_edit.objectName().lower() and 'password' in line_edit.objectName().lower():
                    line_edit.setText(self.widget_states[bkmkr_name]['password'])

    def closeEvent(self, event) -> None:
        self.close_without_saving()
        self.close()
