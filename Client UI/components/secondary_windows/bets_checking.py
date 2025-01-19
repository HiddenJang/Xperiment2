from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore

from ..templates.bets_checking_window_template import Ui_bets_checking


class BetsChecking(Ui_bets_checking, QDialog):
    """Класс-обертка для окна ожидания получения результата ранее сделанных ставок"""
    skip_bets_checking_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(BetsChecking, self).__init__()
        self.ui = Ui_bets_checking()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.ui.pushButton_skipBetsCheking.clicked.connect(self.skip_bets_checking_signal.emit)
