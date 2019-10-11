# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\编程文件\python\图片分类查询系统\main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1460, 1000)
        # palette1 = QtGui.QPalette()
        # palette1.setColor(QtGui.QPalette.Background, QtGui.QColor(192,253,123))   # 设置背景颜色
        # palette1.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("./background/start.jpg").scaled(MainWindow.size())))  # 设置背景图片
        # MainWindow.setPalette(palette1)
        # 背景图片设置，后面美化使用
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menuview = QtWidgets.QMenu(self.menubar)
        self.menuview.setObjectName("menuview")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionviusal_menu = QtWidgets.QAction(MainWindow)
        self.actionviusal_menu.setObjectName("actionviusal_menu")
        self.actionviusal_menu.setEnabled(False)
        self.menufile.addAction(self.actionopen)
        self.menuview.addAction(self.actionviusal_menu)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuview.menuAction())

        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "数据集图像筛查系统"))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.actionopen.setText(_translate("MainWindow", "Open         "))
        self.actionopen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.menuview.setTitle(_translate("MainWindow", "View"))
        self.actionviusal_menu.setText(_translate("MainWindow", "Viusal_Menu"))
        self.actionviusal_menu.setShortcut(_translate("MainWindow","Ctrl+W"))


