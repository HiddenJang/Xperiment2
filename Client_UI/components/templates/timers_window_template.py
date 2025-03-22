# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timers_window_template.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_timers_settings(object):
    def setupUi(self, timers_settings):
        timers_settings.setObjectName("timers_settings")
        timers_settings.setWindowModality(QtCore.Qt.ApplicationModal)
        timers_settings.resize(381, 219)
        timers_settings.setModal(True)
        self.spinBox_betPreparingTimeout = QtWidgets.QSpinBox(timers_settings)
        self.spinBox_betPreparingTimeout.setGeometry(QtCore.QRect(16, 36, 65, 25))
        self.spinBox_betPreparingTimeout.setMaximum(9999)
        self.spinBox_betPreparingTimeout.setProperty("value", 10)
        self.spinBox_betPreparingTimeout.setObjectName("spinBox_betPreparingTimeout")
        self.label_betPreparingTimeout_1 = QtWidgets.QLabel(timers_settings)
        self.label_betPreparingTimeout_1.setGeometry(QtCore.QRect(16, 14, 211, 16))
        self.label_betPreparingTimeout_1.setObjectName("label_betPreparingTimeout_1")
        self.label_betLastTestTimeout_1 = QtWidgets.QLabel(timers_settings)
        self.label_betLastTestTimeout_1.setGeometry(QtCore.QRect(16, 68, 321, 16))
        self.label_betLastTestTimeout_1.setObjectName("label_betLastTestTimeout_1")
        self.spinBox_betLastTestTimeout = QtWidgets.QSpinBox(timers_settings)
        self.spinBox_betLastTestTimeout.setGeometry(QtCore.QRect(16, 90, 65, 25))
        self.spinBox_betLastTestTimeout.setMaximum(9999)
        self.spinBox_betLastTestTimeout.setProperty("value", 5)
        self.spinBox_betLastTestTimeout.setObjectName("spinBox_betLastTestTimeout")
        self.label_betPreparingTimeout_2 = QtWidgets.QLabel(timers_settings)
        self.label_betPreparingTimeout_2.setGeometry(QtCore.QRect(86, 40, 31, 16))
        self.label_betPreparingTimeout_2.setObjectName("label_betPreparingTimeout_2")
        self.label_betLastTestTimeout_2 = QtWidgets.QLabel(timers_settings)
        self.label_betLastTestTimeout_2.setGeometry(QtCore.QRect(86, 94, 31, 16))
        self.label_betLastTestTimeout_2.setObjectName("label_betLastTestTimeout_2")
        self.spinBox_resultExtractionInterval = QtWidgets.QSpinBox(timers_settings)
        self.spinBox_resultExtractionInterval.setGeometry(QtCore.QRect(16, 143, 65, 25))
        self.spinBox_resultExtractionInterval.setMaximum(9999)
        self.spinBox_resultExtractionInterval.setProperty("value", 6000)
        self.spinBox_resultExtractionInterval.setObjectName("spinBox_resultExtractionInterval")
        self.label_resultExtractionInterval_2 = QtWidgets.QLabel(timers_settings)
        self.label_resultExtractionInterval_2.setGeometry(QtCore.QRect(86, 147, 31, 16))
        self.label_resultExtractionInterval_2.setObjectName("label_resultExtractionInterval_2")
        self.label_resultExtractionInterval_1 = QtWidgets.QLabel(timers_settings)
        self.label_resultExtractionInterval_1.setGeometry(QtCore.QRect(16, 121, 311, 16))
        self.label_resultExtractionInterval_1.setObjectName("label_resultExtractionInterval_1")
        self.frame_timersSettings = QtWidgets.QFrame(timers_settings)
        self.frame_timersSettings.setGeometry(QtCore.QRect(2, 4, 375, 211))
        self.frame_timersSettings.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_timersSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_timersSettings.setLineWidth(3)
        self.frame_timersSettings.setMidLineWidth(1)
        self.frame_timersSettings.setObjectName("frame_timersSettings")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame_timersSettings)
        self.buttonBox.setGeometry(QtCore.QRect(16, 171, 341, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.frame_timersSettings.raise_()
        self.spinBox_betPreparingTimeout.raise_()
        self.label_betPreparingTimeout_1.raise_()
        self.label_betLastTestTimeout_1.raise_()
        self.spinBox_betLastTestTimeout.raise_()
        self.label_betPreparingTimeout_2.raise_()
        self.label_betLastTestTimeout_2.raise_()
        self.spinBox_resultExtractionInterval.raise_()
        self.label_resultExtractionInterval_2.raise_()
        self.label_resultExtractionInterval_1.raise_()

        self.retranslateUi(timers_settings)
        self.buttonBox.accepted.connect(timers_settings.accept) # type: ignore
        self.buttonBox.rejected.connect(timers_settings.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(timers_settings)

    def retranslateUi(self, timers_settings):
        _translate = QtCore.QCoreApplication.translate
        timers_settings.setWindowTitle(_translate("timers_settings", "Настройки таймеров"))
        self.label_betPreparingTimeout_1.setText(_translate("timers_settings", "Таймаут подготовки к ставке"))
        self.label_betLastTestTimeout_1.setText(_translate("timers_settings", "Таймаут последней проверки перед ставкой"))
        self.label_betPreparingTimeout_2.setText(_translate("timers_settings", "сек"))
        self.label_betLastTestTimeout_2.setText(_translate("timers_settings", "сек"))
        self.label_resultExtractionInterval_2.setText(_translate("timers_settings", "сек"))
        self.label_resultExtractionInterval_1.setText(_translate("timers_settings", "Запрос результатов событий через каждые"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    timers_settings = QtWidgets.QDialog()
    ui = Ui_timers_settings()
    ui.setupUi(timers_settings)
    timers_settings.show()
    sys.exit(app.exec_())
