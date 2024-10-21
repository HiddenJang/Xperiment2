from PyQt5.QtWidgets import QDialog

from .forms.server_set_window_template import Ui_servers_settings


class ServerSettingsInput(Ui_servers_settings, QDialog):
    """Класс-обертка для окна настроек подключения к серверу"""

    def __init__(self):
        super(ServerSettingsInput, self).__init__()
        self.ui = Ui_servers_settings()
        self.ui.setupUi(self)

    def get_connection_settings(self) -> dict:
        """Получение адреса api сервера"""
        return {
            'api_url': self.ui.lineEdit_serverAddress.text(),
            'status_request_frequency': self.ui.doubleSpinBox_statusRequestFrequency.value(),
            'pars_request_frequency': self.ui.doubleSpinBox_parsRequestFrequency.value(),
            'response_timeout': self.ui.doubleSpinBox_responseTimeout.value()
        }

    # def set_connection_settings(self, element_data: dict) -> None:
    #     """Установка ранне выставленных настроек при запуске приложения"""
    #     match element_data.get("field"):

