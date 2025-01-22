import os
import json
import logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog

from ..templates.browser_control_window_template import Ui_browser_control_settings
from .. import settings

logger = logging.getLogger('Client UI.components.secondary_windows.browser_control_settings')


class BrowserControlSettings(Ui_browser_control_settings, QDialog):
    """Класс-обертка для окна настроек автоматического управления браузерами"""
    widget_states = {}

    def __init__(self):
        super(BrowserControlSettings, self).__init__()
        self.ui = Ui_browser_control_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.set_control_settings_from_env)
        self.ui.buttonBox.rejected.connect(self.close_without_saving)
        self.ui.buttonBox.accepted.connect(self.close_with_saving)

    def set_control_settings_from_env(self) -> None:
        """Установка состояний виджетов окна настроек управления браузерами из переменных окружения"""
        user_auth_data = os.environ.get('BKMKR_SITES_AUTH_DATA')

        if user_auth_data:
            try:
                user_auth_data = json.loads(user_auth_data.replace("'", '"'))
            except BaseException as ex:
                logger.info(ex)
                return
            for bkmkr_name in user_auth_data.keys():
                for line_edit in self.findChildren(QtWidgets.QLineEdit):
                    if bkmkr_name in line_edit.objectName().lower() and 'login' in line_edit.objectName().lower():
                        line_edit.setText(user_auth_data[bkmkr_name]['login'])
                    elif bkmkr_name in line_edit.objectName().lower() and 'password' in line_edit.objectName().lower():
                        line_edit.setText(user_auth_data[bkmkr_name]['password'])

    def get_control_settings(self) -> dict:
        """Получение состояний виджетов окна настроек управления браузерами"""
        states = {'auth_data': {}, 'timeouts': {}}
        for bkmkr_name in settings.BOOKMAKERS.keys():
            states['auth_data'][bkmkr_name] = {'login': '', 'password': ''}
            for line_edit in self.findChildren(QtWidgets.QLineEdit):
                if bkmkr_name in line_edit.objectName().lower() and 'login' in line_edit.objectName().lower():
                    states['auth_data'][bkmkr_name]['login'] = line_edit.text()
                elif bkmkr_name in line_edit.objectName().lower() and 'password' in line_edit.objectName().lower():
                    states['auth_data'][bkmkr_name]['password'] = line_edit.text()
        states['timeouts']['authorization_page_load_timeout'] = self.ui.spinBox_authorizationPageLoadTimeout.value()
        states['timeouts']['bet_page_load_timeout'] = self.ui.spinBox_betPageLoadTimeout.value()
        states['timeouts']['result_page_load_timeout'] = self.ui.spinBox_resultPageLoadTimeout.value()
        return states

    def close_with_saving(self) -> None:
        """Закрытие окна с сохранением изменений"""
        states = self.get_control_settings()
        with open(settings.ENV_PATH, "w") as env_file:
            env_file.write(f'BKMKR_SITES_AUTH_DATA={str(states["auth_data"])}')
        os.environ['BKMKR_SITES_AUTH_DATA'] = str(states["auth_data"])

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""
        self.ui.spinBox_authorizationPageLoadTimeout.setValue(self.widget_states['timeouts']['authorization_page_load_timeout'])
        self.ui.spinBox_authorizationPageLoadTimeout.setValue(self.widget_states['timeouts']['bet_page_load_timeout'])
        self.ui.spinBox_resultPageLoadTimeout.setValue(self.widget_states['timeouts']['result_page_load_timeout'])

    def closeEvent(self, event) -> None:
        self.set_control_settings_from_env()
        self.close_without_saving()
        self.close()
