from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog
import webbrowser
from .forms.result_window_template import Ui_Form_scanResults


class ResultWindow(Ui_Form_scanResults, QDialog):
    """Класс-обертка для окна отрисовки результатов поиска"""

    closeResultWindow = QtCore.pyqtSignal()
    openResultWindow = QtCore.pyqtSignal()

    def __init__(self):
        super(ResultWindow, self).__init__()
        self.ui = Ui_Form_scanResults()
        self.ui.setupUi(self)

        self._translate = QtCore.QCoreApplication.translate
        self.ui.tableWidget_scanResults.itemDoubleClicked.connect(self.open_link)

    def render_results(self, scan_result: dict) -> None:
        """Отрисовка результатов сканирования в таблицу"""

        for row in range(1, self.ui.tableWidget_scanResults.rowCount()):
            self.ui.tableWidget_scanResults.removeRow(row)
        self.ui.tableWidget_scanResults.setRowCount(0)

        for column in (0, 3, 4, 5, 6):
            self.ui.tableWidget_scanResults.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)

        match scan_result[0][0]["market"].lower():
            case "тотал" | "total" | "фора":
                self.render_total(scan_result)
            case "победитель" | "result":
                self.render_winner(scan_result)

    def render_total(self, scan_result) -> None:
        """Отрисовка результатов типа Тотал/фора"""

        row_num = 0
        for fork_data in scan_result:
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
        for row in range(self.ui.tableWidget_scanResults.rowCount()):
            self.ui.tableWidget_scanResults.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.ResizeToContents)

    def render_winner(self, scan_result) -> None:
        """Отрисовка результатов типа Победитель"""

        row_num = 0
        for fork_data in scan_result:
            for bkmkr_data in fork_data:
                self.ui.tableWidget_scanResults.insertRow(row_num)
                item_bookmaker = QtWidgets.QTableWidgetItem()
                item_bookmaker.setText(self._translate("Form_scanResults", bkmkr_data['bookmaker']))
                self.ui.tableWidget_scanResults.setItem(row_num, 0, item_bookmaker)

                item_teams = QtWidgets.QTableWidgetItem()
                item_teams.setText(self._translate("Form_scanResults", bkmkr_data['teams']))
                self.ui.tableWidget_scanResults.setItem(row_num, 1, item_teams)

                item_region_league = QtWidgets.QTableWidgetItem()
                item_region_league.setText(
                    self._translate("Form_scanResults", f"{bkmkr_data['region']}/{bkmkr_data['league']}"))
                self.ui.tableWidget_scanResults.setItem(row_num, 2, item_region_league)

                item_date = QtWidgets.QTableWidgetItem()
                item_date.setText(self._translate("Form_scanResults", bkmkr_data['date']))
                self.ui.tableWidget_scanResults.setItem(row_num, 3, item_date)

                item_market = QtWidgets.QTableWidgetItem()
                item_market.setText(self._translate("Form_scanResults", bkmkr_data['market']))
                self.ui.tableWidget_scanResults.setItem(row_num, 4, item_market)

                home = bkmkr_data['runners'].get('home')
                draw =bkmkr_data['runners'].get('draw')
                away =bkmkr_data['runners'].get('away')
                item_home_draw_away = QtWidgets.QTableWidgetItem()
                item_home_draw_away.setText(
                    self._translate("Form_scanResults", f"{home}/{draw}/{away}"))
                self.ui.tableWidget_scanResults.setItem(row_num, 5, item_home_draw_away)

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
        for row in range(self.ui.tableWidget_scanResults.rowCount()):
            self.ui.tableWidget_scanResults.verticalHeader().setSectionResizeMode(row,
                                                                                  QtWidgets.QHeaderView.ResizeToContents)

    def showEvent(self, event):
        self.openResultWindow.emit()

    def closeEvent(self, event):
        self.ui.tableWidget_scanResults.clearContents()
        self.close()
        self.closeResultWindow.emit()

    def open_link(self, item) -> None:
        """Открытие URL-ссылок в браузере по двойному нажатию"""
        if item.column() == 6:
            webbrowser.open(item.text())
