from PyQt5.QtWidgets import QDialog

from .templates.server_set_window_template import Ui_server_settings


class ServerSettingsInput(Ui_server_settings, QDialog):
    """Класс-обертка для окна настроек подключения к серверу"""

    widget_states = {}

    def __init__(self):
        super(ServerSettingsInput, self).__init__()
        self.ui = Ui_server_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.close_without_saving)

    def get_connection_settings(self) -> dict:
        """Получение адреса api сервера"""
        return {
            'api_url': self.ui.lineEdit_serverAddress.text(),
            'status_request_interval': self.ui.spinBox_statusRequestInterval.value(),
            'pars_request_interval': self.ui.spinBox_parsRequestInterval.value(),
            'status_response_timeout': self.ui.spinBox_statusResponseTimeout.value(),
            'pars_response_timeout': self.ui.spinBox_parsResponseTimeout.value()
        }

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""

        self.ui.lineEdit_serverAddress.setText(self.widget_states["api_url"])
        self.ui.spinBox_statusRequestInterval.setValue(self.widget_states["status_request_interval"])
        self.ui.spinBox_parsRequestInterval.setValue(self.widget_states["pars_request_interval"])
        self.ui.spinBox_statusResponseTimeout.setValue(self.widget_states["status_response_timeout"])
        self.ui.spinBox_parsResponseTimeout.setValue(self.widget_states["pars_response_timeout"])

    def closeEvent(self, event) -> None:
        self.close_without_saving()
        self.close()
