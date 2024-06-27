from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import QThread, QObject
import random
from .result_window_template import Ui_Form_scanResults

class ResultWindow(Ui_Form_scanResults, QDialog):
    """Класс-обертка для окна отрисовки результатов поиска"""

    closeResultWindow = QtCore.pyqtSignal()
    openResultWindow = QtCore.pyqtSignal()

    def __init__(self):
        super(ResultWindow, self).__init__()
        self.ui = Ui_Form_scanResults()
        self.ui.setupUi(self)

    def render_results(self, scan_result: dict) -> None:
        """Отрисовка результатов сканирования в таблицу"""

        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_scanResults.setItem(random.randint(0, 9), 1, item)
        item.setText(_translate("Form_scanResults", scan_result["Success"]))

    def showEvent(self, event):
        self.openResultWindow.emit()

    def closeEvent(self, event):
        self.closeResultWindow.emit()

    # def event(self, event):
    #     if event.type() == QtCore.QEvent.WindowActivate:
    #         print(f"Oкно стало активным; (WindowActivate).")
    #     elif event.type() == QtCore.QEvent.WindowDeactivate:
    #         print(f"Oкно стало НЕактивным; (WindowDeactivate).")
    #     elif event.type() == QtCore.QEvent.Close:
    #         print(f"Oкно закрытo (QCloseEvent).")
    #
    #     return QtWidgets.QWidget.event(self, event)
