from PyQt5.QtWidgets import QDialog

from .forms.server_set_window_template import Ui_servers_settings


class ServerSettingsInput(Ui_servers_settings, QDialog):
    """Класс-обертка для окна настроек подключения к серверу"""

    def __init__(self):
        super(ServerSettingsInput, self).__init__()
        self.ui = Ui_servers_settings()
        self.ui.setupUi(self)

    def get_server_address(self) -> str:
        """Получение адреса api сервера"""
        return self.ui.lineEdit_serverAddress.text()


