from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog
import pprint
from .result_window_template import Ui_Form_scanResults

class ResultWindow(Ui_Form_scanResults, QDialog):
    """Класс-обертка для окна отрисовки результатов поиска"""

    closeResultWindow = QtCore.pyqtSignal()
    openResultWindow = QtCore.pyqtSignal()

    def __init__(self):
        super(ResultWindow, self).__init__()
        self.ui = Ui_Form_scanResults()
        self.ui.setupUi(self)

        self._translate = QtCore.QCoreApplication.translate

    def render_results(self, scan_result: dict) -> None:
        """Отрисовка результатов сканирования в таблицу"""

        for row in range(1, self.ui.tableWidget_scanResults.rowCount()):
            self.ui.tableWidget_scanResults.removeRow(row)
        self.ui.tableWidget_scanResults.setRowCount(0)

        row_num = 0
        for fork_data in eval(scan_result["Success"]):
            for bkmkr_data in fork_data:
                self.ui.tableWidget_scanResults.insertRow(row_num)
                item_bookmaker = QtWidgets.QTableWidgetItem()
                item_bookmaker.setText(self._translate("Form_scanResults", bkmkr_data['bookmaker']))
                self.ui.tableWidget_scanResults.setItem(row_num, 0, item_bookmaker)

                item_teams = QtWidgets.QTableWidgetItem()
                item_teams.setText(self._translate("Form_scanResults", bkmkr_data['teams']))
                self.ui.tableWidget_scanResults.setItem(row_num, 1, item_teams)

                item_region_league = QtWidgets.QTableWidgetItem()
                item_region_league.setText(self._translate("Form_scanResults", f"{bkmkr_data['region']}/{bkmkr_data['league']}"))
                self.ui.tableWidget_scanResults.setItem(row_num, 2, item_region_league)

                item_date = QtWidgets.QTableWidgetItem()
                item_date.setText(self._translate("Form_scanResults", bkmkr_data['date']))
                self.ui.tableWidget_scanResults.setItem(row_num, 3, item_date)

                item_market = QtWidgets.QTableWidgetItem()
                item_market.setText(self._translate("Form_scanResults", bkmkr_data['market']))
                self.ui.tableWidget_scanResults.setItem(row_num, 4, item_market)

                nom = bkmkr_data['runners'].keys()
                type_total = bkmkr_data['runners'].values()
                type_total = list(type_total)[0].keys()
                koeff = bkmkr_data['runners'].values()
                koeff = list(koeff)[0].values()
                item_nom_type_koeff = QtWidgets.QTableWidgetItem()
                item_nom_type_koeff.setText(self._translate("Form_scanResults", f"{list(nom)[0]}/{list(type_total)[0]}/{list(koeff)[0]}"))
                self.ui.tableWidget_scanResults.setItem(row_num, 5, item_nom_type_koeff)

                item_url = QtWidgets.QTableWidgetItem()
                item_url.setText(self._translate("Form_scanResults", bkmkr_data['url']))
                self.ui.tableWidget_scanResults.setItem(row_num, 6, item_url)
                row_num += 1

            self.ui.tableWidget_scanResults.insertRow(row_num)
            for column in range(self.ui.tableWidget_scanResults.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                brush = QtGui.QBrush(QtGui.QColor(15, 248, 12))
                brush.setStyle(QtCore.Qt.SolidPattern)
                item.setBackground(brush)
                self.ui.tableWidget_scanResults.setItem(row_num, column, item)

            row_num += 1

    def showEvent(self, event):
        self.openResultWindow.emit()

    def closeEvent(self, event):
        self.ui.tableWidget_scanResults.clearContents()
        self.close()
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

## INPUT DATA EXAMPLE ##
##