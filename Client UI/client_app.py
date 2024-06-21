import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import settings
from Xperiment2 import Ui_desktopClient


settings.init_logger()

class DesktopApp(QMainWindow):
    def __init__(self):
        super(DesktopApp, self).__init__()
        self.ui = Ui_desktopClient()
        self.ui.setupUi(self)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = DesktopApp()
        w.show()
        sys.exit(app.exec_())
    except Exception as ex:
        DesktopApp.diagMessagesOutput(f'{time} Модуль LeakScanner, цикл отображения MainWindow, error message: {ex}')
        logger.error(f'Ошибка цикла отображения MainWindow, error message: {ex}')
