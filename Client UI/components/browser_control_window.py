import os
import json
import logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog

from .templates.browser_control_window_template import Ui_browser_control_settings
from . import settings

logger = logging.getLogger('Client UI.components.browser_control_window')


class BrowserControlSettings(Ui_browser_control_settings, QDialog):
    """Класс-обертка для окна настроек автоматического управления браузерами"""
    diag_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(BrowserControlSettings, self).__init__()
        self.ui = Ui_browser_control_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.set_control_settings_from_env)
        self.ui.buttonBox.accepted.connect(self.close_with_saving)

    def set_control_settings_from_env(self) -> None:
        """Установка состояний виджетов окна настроек управления браузерами из переменных окружения"""
        if not os.path.exists(settings.ENV_PATH):
            open(settings.ENV_PATH, "w").close()
            diag_mess = f'Файл с переменными окружения отсутствует. Создан {settings.ENV_PATH}'
            logger.info(logger.info(diag_mess))
            self.diag_signal.emit(diag_mess)
            return

        user_auth_data = os.environ.get('BKMKR_SITES_AUTH_DATA')

        if user_auth_data:
            user_auth_data = json.loads(user_auth_data.replace("'", '"'))
            for bkmkr_name in user_auth_data.keys():
                for line_edit in self.findChildren(QtWidgets.QLineEdit):
                    if bkmkr_name in line_edit.objectName().lower() and 'login' in line_edit.objectName().lower():
                        line_edit.setText(user_auth_data[bkmkr_name]['login'])
                    elif bkmkr_name in line_edit.objectName().lower() and 'password' in line_edit.objectName().lower():
                        line_edit.setText(user_auth_data[bkmkr_name]['password'])

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

    def close_with_saving(self) -> None:
        """Закрытие окна с сохранением изменений"""
        states = self.get_control_settings()
        with open(settings.ENV_PATH, "w") as env_file:
            env_file.write(f'BKMKR_SITES_AUTH_DATA={str(states)}')
        os.environ.setdefault('BKMKR_SITES_AUTH_DATA', str(states))

    def closeEvent(self, event) -> None:
        self.set_control_settings_from_env()
        self.close()
