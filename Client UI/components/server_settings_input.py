from PyQt5.QtWidgets import QDialog

from .forms.server_set_window_template import Ui_servers_settings


class ServerSettingsInput(Ui_servers_settings, QDialog):
    """Класс-обертка для окна настроек подключения к серверу"""

    widget_states = {}

    def __init__(self):
        super(ServerSettingsInput, self).__init__()
        self.ui = Ui_servers_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.close_without_saving)

    def get_connection_settings(self) -> dict:
        """Получение адреса api сервера"""
        return {
            'api_url': self.ui.lineEdit_serverAddress.text(),
            'status_request_frequency': self.ui.doubleSpinBox_statusRequestFrequency.value(),
            'pars_request_frequency': self.ui.doubleSpinBox_parsRequestFrequency.value(),
            'response_timeout': self.ui.doubleSpinBox_responseTimeout.value()
        }

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""

        self.ui.lineEdit_serverAddress.setText(self.widget_states["api_url"])
        self.ui.doubleSpinBox_statusRequestFrequency.setValue(self.widget_states["status_request_frequency"])
        self.ui.doubleSpinBox_parsRequestFrequency.setValue(self.widget_states["pars_request_frequency"])
        self.ui.doubleSpinBox_responseTimeout.setValue(self.widget_states["response_timeout"])

    def closeEvent(self, event) -> None:
        self.close_without_saving()
        self.close()
