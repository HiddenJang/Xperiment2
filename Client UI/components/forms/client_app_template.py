# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_app_template.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_client(object):
    def setupUi(self, MainWindow_client):
        MainWindow_client.setObjectName("MainWindow_client")
        MainWindow_client.resize(563, 603)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow_client.sizePolicy().hasHeightForWidth())
        MainWindow_client.setSizePolicy(sizePolicy)
        MainWindow_client.setMinimumSize(QtCore.QSize(563, 603))
        MainWindow_client.setMaximumSize(QtCore.QSize(563, 603))
        self.desktopClient = QtWidgets.QWidget(MainWindow_client)
        self.desktopClient.setObjectName("desktopClient")
        self.frame = QtWidgets.QFrame(self.desktopClient)
        self.frame.setGeometry(QtCore.QRect(0, 0, 560, 370))
        self.frame.setStyleSheet("border-top-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(15, 12, 531, 241))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(2)
        self.frame_2.setObjectName("frame_2")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(31, 15, 495, 231))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_gameStatus = QtWidgets.QLabel(self.layoutWidget)
        self.label_gameStatus.setObjectName("label_gameStatus")
        self.gridLayout.addWidget(self.label_gameStatus, 0, 2, 1, 1)
        self.comboBox_marketType = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_marketType.sizePolicy().hasHeightForWidth())
        self.comboBox_marketType.setSizePolicy(sizePolicy)
        self.comboBox_marketType.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_marketType.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_marketType.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_marketType.setObjectName("comboBox_marketType")
        self.comboBox_marketType.addItem("")
        self.comboBox_marketType.addItem("")
        self.comboBox_marketType.addItem("")
        self.gridLayout.addWidget(self.comboBox_marketType, 5, 1, 1, 1)
        self.comboBox_secondBkmkr = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_secondBkmkr.sizePolicy().hasHeightForWidth())
        self.comboBox_secondBkmkr.setSizePolicy(sizePolicy)
        self.comboBox_secondBkmkr.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_secondBkmkr.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_secondBkmkr.setObjectName("comboBox_secondBkmkr")
        self.comboBox_secondBkmkr.addItem("")
        self.comboBox_secondBkmkr.addItem("")
        self.comboBox_secondBkmkr.addItem("")
        self.gridLayout.addWidget(self.comboBox_secondBkmkr, 3, 2, 1, 1)
        self.comboBox_sportType = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_sportType.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_sportType.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_sportType.setObjectName("comboBox_sportType")
        self.comboBox_sportType.addItem("")
        self.comboBox_sportType.addItem("")
        self.comboBox_sportType.addItem("")
        self.gridLayout.addWidget(self.comboBox_sportType, 1, 1, 1, 1)
        self.doubleSpinBox_corridor = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_corridor.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_corridor.setSizePolicy(sizePolicy)
        self.doubleSpinBox_corridor.setSingleStep(0.1)
        self.doubleSpinBox_corridor.setObjectName("doubleSpinBox_corridor")
        self.gridLayout.addWidget(self.doubleSpinBox_corridor, 7, 3, 1, 1)
        self.label_corridor = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_corridor.sizePolicy().hasHeightForWidth())
        self.label_corridor.setSizePolicy(sizePolicy)
        self.label_corridor.setMinimumSize(QtCore.QSize(150, 0))
        self.label_corridor.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_corridor.setObjectName("label_corridor")
        self.gridLayout.addWidget(self.label_corridor, 6, 3, 1, 1)
        self.label_minKsecondBkmkr = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_minKsecondBkmkr.sizePolicy().hasHeightForWidth())
        self.label_minKsecondBkmkr.setSizePolicy(sizePolicy)
        self.label_minKsecondBkmkr.setMinimumSize(QtCore.QSize(150, 0))
        self.label_minKsecondBkmkr.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_minKsecondBkmkr.setObjectName("label_minKsecondBkmkr")
        self.gridLayout.addWidget(self.label_minKsecondBkmkr, 6, 2, 1, 1)
        self.doubleSpinBox_minKfirstBkmkr = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_minKfirstBkmkr.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_minKfirstBkmkr.setSizePolicy(sizePolicy)
        self.doubleSpinBox_minKfirstBkmkr.setDecimals(2)
        self.doubleSpinBox_minKfirstBkmkr.setSingleStep(0.1)
        self.doubleSpinBox_minKfirstBkmkr.setProperty("value", 1.9)
        self.doubleSpinBox_minKfirstBkmkr.setObjectName("doubleSpinBox_minKfirstBkmkr")
        self.gridLayout.addWidget(self.doubleSpinBox_minKfirstBkmkr, 7, 1, 1, 1)
        self.label_sportType = QtWidgets.QLabel(self.layoutWidget)
        self.label_sportType.setObjectName("label_sportType")
        self.gridLayout.addWidget(self.label_sportType, 0, 1, 1, 1)
        self.doubleSpinBox_minKsecondBkmkr = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_minKsecondBkmkr.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_minKsecondBkmkr.setSizePolicy(sizePolicy)
        self.doubleSpinBox_minKsecondBkmkr.setSingleStep(0.1)
        self.doubleSpinBox_minKsecondBkmkr.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_minKsecondBkmkr.setProperty("value", 1.9)
        self.doubleSpinBox_minKsecondBkmkr.setObjectName("doubleSpinBox_minKsecondBkmkr")
        self.gridLayout.addWidget(self.doubleSpinBox_minKsecondBkmkr, 7, 2, 1, 1)
        self.label_secondBkmkr = QtWidgets.QLabel(self.layoutWidget)
        self.label_secondBkmkr.setObjectName("label_secondBkmkr")
        self.gridLayout.addWidget(self.label_secondBkmkr, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)
        self.label_minKfirstBkmkr = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_minKfirstBkmkr.sizePolicy().hasHeightForWidth())
        self.label_minKfirstBkmkr.setSizePolicy(sizePolicy)
        self.label_minKfirstBkmkr.setMinimumSize(QtCore.QSize(150, 0))
        self.label_minKfirstBkmkr.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_minKfirstBkmkr.setObjectName("label_minKfirstBkmkr")
        self.gridLayout.addWidget(self.label_minKfirstBkmkr, 6, 1, 1, 1)
        self.comboBox_gameStatus = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_gameStatus.sizePolicy().hasHeightForWidth())
        self.comboBox_gameStatus.setSizePolicy(sizePolicy)
        self.comboBox_gameStatus.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_gameStatus.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_gameStatus.setObjectName("comboBox_gameStatus")
        self.comboBox_gameStatus.addItem("")
        self.comboBox_gameStatus.addItem("")
        self.gridLayout.addWidget(self.comboBox_gameStatus, 1, 2, 1, 1)
        self.comboBox_firstBkmkr = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_firstBkmkr.sizePolicy().hasHeightForWidth())
        self.comboBox_firstBkmkr.setSizePolicy(sizePolicy)
        self.comboBox_firstBkmkr.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_firstBkmkr.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_firstBkmkr.setObjectName("comboBox_firstBkmkr")
        self.comboBox_firstBkmkr.addItem("")
        self.comboBox_firstBkmkr.addItem("")
        self.comboBox_firstBkmkr.addItem("")
        self.gridLayout.addWidget(self.comboBox_firstBkmkr, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.label_firstBkmkr = QtWidgets.QLabel(self.layoutWidget)
        self.label_firstBkmkr.setObjectName("label_firstBkmkr")
        self.gridLayout.addWidget(self.label_firstBkmkr, 2, 1, 1, 1)
        self.label_marketType = QtWidgets.QLabel(self.layoutWidget)
        self.label_marketType.setObjectName("label_marketType")
        self.gridLayout.addWidget(self.label_marketType, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 8, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(25, 22, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
        self.layoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.layoutWidget_2.setGeometry(QtCore.QRect(31, 270, 273, 58))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_startScan = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_startScan.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_startScan.sizePolicy().hasHeightForWidth())
        self.pushButton_startScan.setSizePolicy(sizePolicy)
        self.pushButton_startScan.setObjectName("pushButton_startScan")
        self.gridLayout_2.addWidget(self.pushButton_startScan, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 0, 1, 1)
        self.pushButton_stopScan = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_stopScan.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_stopScan.sizePolicy().hasHeightForWidth())
        self.pushButton_stopScan.setSizePolicy(sizePolicy)
        self.pushButton_stopScan.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_stopScan.setAutoDefault(False)
        self.pushButton_stopScan.setDefault(False)
        self.pushButton_stopScan.setObjectName("pushButton_stopScan")
        self.gridLayout_2.addWidget(self.pushButton_stopScan, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 2, 1, 1)
        self.label_serverStatus = QtWidgets.QLabel(self.frame)
        self.label_serverStatus.setGeometry(QtCore.QRect(340, 290, 181, 31))
        self.label_serverStatus.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.label_serverStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.label_serverStatus.setLineWidth(2)
        self.label_serverStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_serverStatus.setObjectName("label_serverStatus")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(305, 260, 241, 101))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(2)
        self.frame_3.setObjectName("frame_3")
        self.label_connectionToServer = QtWidgets.QLabel(self.frame_3)
        self.label_connectionToServer.setGeometry(QtCore.QRect(39, 5, 172, 20))
        self.label_connectionToServer.setObjectName("label_connectionToServer")
        self.pushButton_connect = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_connect.setGeometry(QtCore.QRect(6, 68, 111, 25))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_disconnect = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_disconnect.setEnabled(False)
        self.pushButton_disconnect.setGeometry(QtCore.QRect(123, 68, 111, 25))
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.layoutWidget_2.raise_()
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.layoutWidget.raise_()
        self.label_serverStatus.raise_()
        self.listWidget_diagnostics = QtWidgets.QListWidget(self.desktopClient)
        self.listWidget_diagnostics.setGeometry(QtCore.QRect(5, 390, 551, 161))
        self.listWidget_diagnostics.setObjectName("listWidget_diagnostics")
        self.label_systemInfo = QtWidgets.QLabel(self.desktopClient)
        self.label_systemInfo.setGeometry(QtCore.QRect(187, 370, 171, 20))
        self.label_systemInfo.setObjectName("label_systemInfo")
        MainWindow_client.setCentralWidget(self.desktopClient)
        self.menubar = QtWidgets.QMenuBar(MainWindow_client)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 563, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow_client.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_client)
        self.statusbar.setObjectName("statusbar")
        MainWindow_client.setStatusBar(self.statusbar)
        self.action_serverSettings = QtWidgets.QAction(MainWindow_client)
        self.action_serverSettings.setObjectName("action_serverSettings")
        self.menu.addAction(self.action_serverSettings)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow_client)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_client)

    def retranslateUi(self, MainWindow_client):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_client.setWindowTitle(_translate("MainWindow_client", "Client application"))
        self.label_gameStatus.setText(_translate("MainWindow_client", "Стадия игры"))
        self.comboBox_marketType.setItemText(0, _translate("MainWindow_client", "Победитель"))
        self.comboBox_marketType.setItemText(1, _translate("MainWindow_client", "Тотал"))
        self.comboBox_marketType.setItemText(2, _translate("MainWindow_client", "Фора"))
        self.comboBox_secondBkmkr.setItemText(0, _translate("MainWindow_client", "Olimp"))
        self.comboBox_secondBkmkr.setItemText(1, _translate("MainWindow_client", "Leon"))
        self.comboBox_secondBkmkr.setItemText(2, _translate("MainWindow_client", "Betboom"))
        self.comboBox_sportType.setItemText(0, _translate("MainWindow_client", "Soccer"))
        self.comboBox_sportType.setItemText(1, _translate("MainWindow_client", "Basketball"))
        self.comboBox_sportType.setItemText(2, _translate("MainWindow_client", "Icehockey"))
        self.label_corridor.setText(_translate("MainWindow_client", "Min коэфф. на ничью"))
        self.label_minKsecondBkmkr.setText(_translate("MainWindow_client", "Min коэфф. на ком. 2"))
        self.label_sportType.setText(_translate("MainWindow_client", "Вид спорта"))
        self.label_secondBkmkr.setText(_translate("MainWindow_client", "Второй букмекер"))
        self.label_minKfirstBkmkr.setText(_translate("MainWindow_client", "Min коэфф. на ком. 1"))
        self.comboBox_gameStatus.setItemText(0, _translate("MainWindow_client", "Prematch"))
        self.comboBox_gameStatus.setItemText(1, _translate("MainWindow_client", "Inplay"))
        self.comboBox_firstBkmkr.setItemText(0, _translate("MainWindow_client", "Leon"))
        self.comboBox_firstBkmkr.setItemText(1, _translate("MainWindow_client", "Olimp"))
        self.comboBox_firstBkmkr.setItemText(2, _translate("MainWindow_client", "Betboom"))
        self.label_firstBkmkr.setText(_translate("MainWindow_client", "Первый букмекер"))
        self.label_marketType.setText(_translate("MainWindow_client", "Тип ставки"))
        self.pushButton_startScan.setText(_translate("MainWindow_client", "Начать сканирование"))
        self.pushButton_stopScan.setText(_translate("MainWindow_client", "Остановить сканирование"))
        self.label_serverStatus.setText(_translate("MainWindow_client", "Статус"))
        self.label_connectionToServer.setText(_translate("MainWindow_client", "Подключение к серверу"))
        self.pushButton_connect.setText(_translate("MainWindow_client", "Подключиться"))
        self.pushButton_disconnect.setText(_translate("MainWindow_client", "Прервать"))
        self.label_systemInfo.setText(_translate("MainWindow_client", "Системная информация"))
        self.menu.setTitle(_translate("MainWindow_client", "Настройки"))
        self.action_serverSettings.setText(_translate("MainWindow_client", "Адрес сервера"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_client = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_client()
    ui.setupUi(MainWindow_client)
    MainWindow_client.show()
    sys.exit(app.exec_())