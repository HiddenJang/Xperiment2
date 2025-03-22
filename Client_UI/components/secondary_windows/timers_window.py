from PyQt5.QtWidgets import QDialog

from ..templates.timers_window_template import Ui_timers_settings


class TimersSettings(Ui_timers_settings, QDialog):
    """Класс-обертка для окна настройки таймеров алгоритма размещения ставок"""
    widget_states = {}

    def __init__(self):
        super(TimersSettings, self).__init__()
        self.ui = Ui_timers_settings()
        self.ui.setupUi(self)
        self.add_functions()

    def add_functions(self) -> None:
        self.ui.buttonBox.rejected.connect(self.close_without_saving)

    def get_bet_timeouts_settings(self) -> dict:
        """Получение состояний виджетов окна настроек управления браузерами"""
        return {'bet_preparing_timeout': self.ui.spinBox_betPreparingTimeout.value(),
                'bet_last_test_timeout': self.ui.spinBox_betLastTestTimeout.value(),
                'result_extraction_interval': self.ui.spinBox_resultExtractionInterval.value()}

    def close_without_saving(self) -> None:
        """Закрытие окна без сохранения изменений"""
        self.ui.spinBox_betPreparingTimeout.setValue(self.widget_states["bet_preparing_timeout"])
        self.ui.spinBox_betLastTestTimeout.setValue(self.widget_states["bet_last_test_timeout"])
        self.ui.spinBox_resultExtractionInterval.setValue(self.widget_states["result_extraction_interval"])

    def closeEvent(self, event) -> None:
        self.close_without_saving()
        self.close()
