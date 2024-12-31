from PyQt5.QtWidgets import QDialog

from .templates.telegram_settings_window_template import Ui_telegram_settings


class TelegramSettings(Ui_telegram_settings, QDialog):
    """Класс-обертка для окна настроек взаимодействия с Telegram"""

    widget_states = {}

    def __init__(self):
        super(TelegramSettings, self).__init__()
        self.ui = Ui_telegram_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.close_without_saving)

    def get_telegram_settings(self) -> dict:
        """Получение состояний виджетов окна настроек взаимодействия с Telegram"""
        return {'group_id': self.ui.lineEdit_telegramGroupId.text(),
                'token': self.ui.lineEdit_telegramBotToken.text()}

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""
        self.ui.lineEdit_telegramGroupId.setText(self.widget_states["group_id"])
        self.ui.lineEdit_telegramBotToken.setText(self.widget_states["token"])

    def closeEvent(self, event) -> None:
        self.close_without_saving()
        self.close()
