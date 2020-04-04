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
        MainWindow.resize(1460, 800)
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

        self.menuview_one = QtWidgets.QMenu(self.menuview)
        self.menuview_one.setObjectName("menuview_one")
        self.menuview_many = QtWidgets.QMenu(self.menuview)
        self.menuview_many.setObjectName("menuview_many")
        # self.menuview_pixel = QtWidgets.QMenu(self.menuview)
        # self.menuview_pixel.setObjectName("menuview_pixel")


        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionopen2 = QtWidgets.QAction(MainWindow)
        self.actionopen2.setObjectName("actionopen2")

        self.actionviusal_menu1 = QtWidgets.QAction(MainWindow)
        self.actionviusal_menu1.setObjectName("actionviusal_menu1")
        self.actionviusal_menu1.setEnabled(False)

        # self.actionviusal_table1 = QtWidgets.QAction(MainWindow)
        # self.actionviusal_table1.setObjectName("actionviusal_table1")
        # self.actionviusal_table1.setEnabled(False)

        self.actionviusal_menu2 = QtWidgets.QAction(MainWindow)
        self.actionviusal_menu2.setObjectName("actionviusal_menu2")
        self.actionviusal_menu2.setEnabled(False)

        self.actionviusal_table2 = QtWidgets.QAction(MainWindow)
        self.actionviusal_table2.setObjectName("actionviusal_table2")
        self.actionviusal_table2.setEnabled(False)

        self.actionviusal_menu3 = QtWidgets.QAction(MainWindow)
        self.actionviusal_menu3.setObjectName("actionviusal_menu3")
        self.actionviusal_menu3.setEnabled(False)


        self.menufile.addAction(self.actionopen)
        self.menufile.addAction(self.actionopen2)

        self.menuview_one.addAction(self.actionviusal_menu1)
        # self.menuview_one.addAction(self.actionviusal_table1)
        self.menuview_many.addAction(self.actionviusal_menu2)
        self.menuview_many.addAction(self.actionviusal_table2)
        self.menuview.addAction(self.menuview_one.menuAction())
        self.menuview.addAction(self.menuview_many.menuAction())
        self.menuview.addAction(self.actionviusal_menu3)




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
        self.actionopen.setText(_translate("MainWindow", "Open-Roi         "))
        self.actionopen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionopen2.setText(_translate("MainWindow", "Open-Remote         "))
        self.actionopen2.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.menuview.setTitle(_translate("MainWindow", "View"))
        self.menuview_one.setTitle(_translate("MainWindow", "View-One"))
        self.menuview_many.setTitle(_translate("MainWindow", "View-Many"))

        self.actionviusal_menu1.setText(_translate("MainWindow", "Viusal_Menu"))
        self.actionviusal_menu1.setShortcut(_translate("MainWindow","Ctrl+W"))
        # self.actionviusal_table1.setText(_translate("MainWindow", "Viusal_Table"))
        # self.actionviusal_table1.setShortcut(_translate("MainWindow","Ctrl+E"))

        self.actionviusal_menu2.setText(_translate("MainWindow", "Viusal_Menu"))
        self.actionviusal_menu2.setShortcut(_translate("MainWindow","Ctrl+B"))
        self.actionviusal_table2.setText(_translate("MainWindow", "Viusal_Table"))
        self.actionviusal_table2.setShortcut(_translate("MainWindow","Ctrl+N"))

        self.actionviusal_menu3.setText(_translate("MainWindow", "Viusal_Pixel"))
        self.actionviusal_menu3.setShortcut(_translate("MainWindow","Ctrl+G"))


        


