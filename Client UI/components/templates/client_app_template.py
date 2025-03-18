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
        MainWindow_client.resize(863, 603)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow_client.sizePolicy().hasHeightForWidth())
        MainWindow_client.setSizePolicy(sizePolicy)
        MainWindow_client.setMinimumSize(QtCore.QSize(863, 603))
        MainWindow_client.setMaximumSize(QtCore.QSize(863, 603))
        self.desktopClient = QtWidgets.QWidget(MainWindow_client)
        self.desktopClient.setObjectName("desktopClient")
        self.frame = QtWidgets.QFrame(self.desktopClient)
        self.frame.setGeometry(QtCore.QRect(1, 1, 560, 370))
        self.frame.setStyleSheet("border-top-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(15, 41, 531, 241))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(2)
        self.frame_2.setObjectName("frame_2")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(31, 44, 495, 231))
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
        self.comboBox_firstBkmkr.setDuplicatesEnabled(False)
        self.comboBox_firstBkmkr.setObjectName("comboBox_firstBkmkr")
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
        self.layoutWidget_2.setGeometry(QtCore.QRect(31, 299, 231, 58))
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
        self.label_scanSettings = QtWidgets.QLabel(self.frame)
        self.label_scanSettings.setGeometry(QtCore.QRect(200, 14, 181, 17))
        self.label_scanSettings.setTextFormat(QtCore.Qt.RichText)
        self.label_scanSettings.setObjectName("label_scanSettings")
        self.checkBox_telegramMessageSwitch = QtWidgets.QCheckBox(self.frame)
        self.checkBox_telegramMessageSwitch.setGeometry(QtCore.QRect(277, 302, 261, 23))
        self.checkBox_telegramMessageSwitch.setObjectName("checkBox_telegramMessageSwitch")
        self.layoutWidget_2.raise_()
        self.frame_2.raise_()
        self.layoutWidget.raise_()
        self.label_scanSettings.raise_()
        self.checkBox_telegramMessageSwitch.raise_()
        self.frame_autoBetSettings = QtWidgets.QFrame(self.desktopClient)
        self.frame_autoBetSettings.setGeometry(QtCore.QRect(564, 1, 296, 370))
        self.frame_autoBetSettings.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_autoBetSettings.setStyleSheet("border-top-color: rgb(0, 0, 0);")
        self.frame_autoBetSettings.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_autoBetSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_autoBetSettings.setLineWidth(3)
        self.frame_autoBetSettings.setMidLineWidth(1)
        self.frame_autoBetSettings.setObjectName("frame_autoBetSettings")
        self.label_autoBetSettings = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_autoBetSettings.setGeometry(QtCore.QRect(32, 16, 251, 20))
        self.label_autoBetSettings.setTextFormat(QtCore.Qt.RichText)
        self.label_autoBetSettings.setObjectName("label_autoBetSettings")
        self.pushButton_startAutoBet = QtWidgets.QPushButton(self.frame_autoBetSettings)
        self.pushButton_startAutoBet.setGeometry(QtCore.QRect(59, 132, 181, 25))
        self.pushButton_startAutoBet.setObjectName("pushButton_startAutoBet")
        self.label_betSizeFirst = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_betSizeFirst.setGeometry(QtCore.QRect(10, 86, 131, 15))
        self.label_betSizeFirst.setObjectName("label_betSizeFirst")
        self.pushButton_cleanRegistry = QtWidgets.QPushButton(self.frame_autoBetSettings)
        self.pushButton_cleanRegistry.setGeometry(QtCore.QRect(59, 196, 181, 23))
        self.pushButton_cleanRegistry.setStyleSheet("background-color: rgb(255, 84, 84);")
        self.pushButton_cleanRegistry.setObjectName("pushButton_cleanRegistry")
        self.label_betSizeSecond = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_betSizeSecond.setGeometry(QtCore.QRect(144, 86, 131, 15))
        self.label_betSizeSecond.setObjectName("label_betSizeSecond")
        self.spinBox_betSizeSecond = QtWidgets.QSpinBox(self.frame_autoBetSettings)
        self.spinBox_betSizeSecond.setGeometry(QtCore.QRect(164, 105, 70, 19))
        self.spinBox_betSizeSecond.setMaximum(99999)
        self.spinBox_betSizeSecond.setObjectName("spinBox_betSizeSecond")
        self.pushButton_closeBrowsers = QtWidgets.QPushButton(self.frame_autoBetSettings)
        self.pushButton_closeBrowsers.setGeometry(QtCore.QRect(74, 166, 151, 21))
        self.pushButton_closeBrowsers.setStyleSheet("background-color: rgb(255, 84, 84);")
        self.pushButton_closeBrowsers.setObjectName("pushButton_closeBrowsers")
        self.label_betSize = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_betSize.setGeometry(QtCore.QRect(81, 65, 101, 15))
        self.label_betSize.setObjectName("label_betSize")
        self.checkBox_betImitation = QtWidgets.QCheckBox(self.frame_autoBetSettings)
        self.checkBox_betImitation.setGeometry(QtCore.QRect(10, 44, 281, 15))
        self.checkBox_betImitation.setObjectName("checkBox_betImitation")
        self.spinBox_betSizeFirst = QtWidgets.QSpinBox(self.frame_autoBetSettings)
        self.spinBox_betSizeFirst.setGeometry(QtCore.QRect(30, 105, 70, 19))
        self.spinBox_betSizeFirst.setMaximum(99999)
        self.spinBox_betSizeFirst.setDisplayIntegerBase(10)
        self.spinBox_betSizeFirst.setObjectName("spinBox_betSizeFirst")
        self.label_resultExtractionTimeout_1 = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_resultExtractionTimeout_1.setGeometry(QtCore.QRect(10, 311, 231, 16))
        self.label_resultExtractionTimeout_1.setObjectName("label_resultExtractionTimeout_1")
        self.spinBox_resultExtractionTimeout = QtWidgets.QSpinBox(self.frame_autoBetSettings)
        self.spinBox_resultExtractionTimeout.setGeometry(QtCore.QRect(30, 330, 70, 20))
        self.spinBox_resultExtractionTimeout.setMaximum(99999)
        self.spinBox_resultExtractionTimeout.setProperty("value", 6000)
        self.spinBox_resultExtractionTimeout.setDisplayIntegerBase(10)
        self.spinBox_resultExtractionTimeout.setObjectName("spinBox_resultExtractionTimeout")
        self.line = QtWidgets.QFrame(self.frame_autoBetSettings)
        self.line.setGeometry(QtCore.QRect(14, 265, 270, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_resultExtractionTimeout_2 = QtWidgets.QLabel(self.frame_autoBetSettings)
        self.label_resultExtractionTimeout_2.setGeometry(QtCore.QRect(105, 330, 31, 20))
        self.label_resultExtractionTimeout_2.setObjectName("label_resultExtractionTimeout_2")
        self.pushButton_setBetTimers = QtWidgets.QPushButton(self.frame_autoBetSettings)
        self.pushButton_setBetTimers.setGeometry(QtCore.QRect(16, 282, 161, 25))
        self.pushButton_setBetTimers.setObjectName("pushButton_setBetTimers")
        self.pushButton_openBetStatistic = QtWidgets.QPushButton(self.frame_autoBetSettings)
        self.pushButton_openBetStatistic.setGeometry(QtCore.QRect(55, 230, 191, 25))
        self.pushButton_openBetStatistic.setObjectName("pushButton_openBetStatistic")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.desktopClient)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 380, 861, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(4, 0, 0, 4)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_systemInfo = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_systemInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_systemInfo.setObjectName("label_systemInfo")
        self.verticalLayout.addWidget(self.label_systemInfo)
        self.listWidget_diagnostics = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget_diagnostics.setMaximumSize(QtCore.QSize(853, 150))
        self.listWidget_diagnostics.setObjectName("listWidget_diagnostics")
        self.verticalLayout.addWidget(self.listWidget_diagnostics)
        MainWindow_client.setCentralWidget(self.desktopClient)
        self.menubar = QtWidgets.QMenuBar(MainWindow_client)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 863, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow_client.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_client)
        self.statusbar.setMinimumSize(QtCore.QSize(563, 22))
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow_client.setStatusBar(self.statusbar)
        self.action_serverSettings = QtWidgets.QAction(MainWindow_client)
        self.action_serverSettings.setObjectName("action_serverSettings")
        self.action_browserControlSettings = QtWidgets.QAction(MainWindow_client)
        self.action_browserControlSettings.setObjectName("action_browserControlSettings")
        self.action_telegramSettings = QtWidgets.QAction(MainWindow_client)
        self.action_telegramSettings.setObjectName("action_telegramSettings")
        self.menu.addAction(self.action_serverSettings)
        self.menu.addAction(self.action_browserControlSettings)
        self.menu.addAction(self.action_telegramSettings)
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
        self.label_firstBkmkr.setText(_translate("MainWindow_client", "Первый букмекер"))
        self.label_marketType.setText(_translate("MainWindow_client", "Тип ставки"))
        self.pushButton_startScan.setText(_translate("MainWindow_client", "Начать сканирование"))
        self.pushButton_stopScan.setText(_translate("MainWindow_client", "Остановить сканирование"))
        self.label_scanSettings.setText(_translate("MainWindow_client", "Настройки сканирования"))
        self.checkBox_telegramMessageSwitch.setText(_translate("MainWindow_client", "Отправка сообщений в Telegram"))
        self.label_autoBetSettings.setText(_translate("MainWindow_client", "Настройки автоматических ставок"))
        self.pushButton_startAutoBet.setText(_translate("MainWindow_client", "Запустить механизм!"))
        self.label_betSizeFirst.setText(_translate("MainWindow_client", "Первый букмекер"))
        self.pushButton_cleanRegistry.setText(_translate("MainWindow_client", "Очистить реестр ставок"))
        self.label_betSizeSecond.setText(_translate("MainWindow_client", "Второй букмекер"))
        self.pushButton_closeBrowsers.setText(_translate("MainWindow_client", "Закрыть браузеры"))
        self.label_betSize.setText(_translate("MainWindow_client", "Размер ставки"))
        self.checkBox_betImitation.setText(_translate("MainWindow_client", "Имитация ставок"))
        self.label_resultExtractionTimeout_1.setText(_translate("MainWindow_client", "Проверка результатов каждые"))
        self.label_resultExtractionTimeout_2.setText(_translate("MainWindow_client", "сек"))
        self.pushButton_setBetTimers.setText(_translate("MainWindow_client", "Установка таймеров"))
        self.pushButton_openBetStatistic.setText(_translate("MainWindow_client", "Открыть файл статистики"))
        self.label_systemInfo.setText(_translate("MainWindow_client", "Системная информация"))
        self.menu.setTitle(_translate("MainWindow_client", "Настройки"))
        self.action_serverSettings.setText(_translate("MainWindow_client", "Подключение"))
        self.action_browserControlSettings.setText(_translate("MainWindow_client", "Управление браузером"))
        self.action_telegramSettings.setText(_translate("MainWindow_client", "Взаимодействие с Telegram"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_client = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_client()
    ui.setupUi(MainWindow_client)
    MainWindow_client.show()
    sys.exit(app.exec_())
