from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog

from .forms.server_set_window_template import Ui_servers_settings


class ServerSettingsInput(Ui_servers_settings, QDialog):
    """Класс-обертка для окна настроек подключения к серверу"""

    def __init__(self):
        super(ServerSettingsInput, self).__init__()

        self.ui = Ui_servers_settings()
        self.ui.setupUi(self)

        self._translate = QtCore.QCoreApplication.translate

        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.accepted.connect(self.save_server_address)

    def save_server_address(self) -> None:
        """Сохранение адреса сервера в файл пользовательских настроек"""

