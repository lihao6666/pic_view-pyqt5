# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lh\Desktop\图片分类查询系统\ui\test-Menu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuview = QtWidgets.QMenu(self.menubar)
        self.menuview.setObjectName("menuview")
        self.menuview_one = QtWidgets.QMenu(self.menuview)
        self.menuview_one.setObjectName("menuview_one")
        self.menuview_many = QtWidgets.QMenu(self.menuview)
        self.menuview_many.setObjectName("menuview_many")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionVisual_Menu = QtWidgets.QAction(MainWindow)
        self.actionVisual_Menu.setObjectName("actionVisual_Menu")
        self.actionVisual_Menu_2 = QtWidgets.QAction(MainWindow)
        self.actionVisual_Menu_2.setObjectName("actionVisual_Menu_2")
        self.menuview_one.addSeparator()
        self.menuview_one.addAction(self.actionVisual_Menu)
        self.menuview_many.addAction(self.actionVisual_Menu_2)
        self.menuview.addAction(self.menuview_one.menuAction())
        self.menuview.addAction(self.menuview_many.menuAction())
        self.menubar.addAction(self.menuview.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuview.setTitle(_translate("MainWindow", "View"))
        self.menuview_one.setTitle(_translate("MainWindow", "View-One"))
        self.menuview_many.setTitle(_translate("MainWindow", "View-Many"))
        self.actionVisual_Menu.setText(_translate("MainWindow", "Visual_Menu"))
        self.actionVisual_Menu_2.setText(_translate("MainWindow", "Visual-Menu"))
