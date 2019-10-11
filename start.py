# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt

class Ui_Start(object):
    def setupUi(self, start):
        start.setObjectName("start")
        start.resize(400, 300)
        start.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
        palette1 = QtGui.QPalette()
        palette1.setColor(QtGui.QPalette.Background, QtGui.QColor(192,253,123))   # 设置背景颜色
        palette1.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("./background/start.jpg").scaled(start.size())))  # 设置背景图片
        start.setPalette(palette1)
        self.label = QtWidgets.QLabel(start)
        self.label.setGeometry(QtCore.QRect(10, 270, 111, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(start)
        self.label_2.setGeometry(QtCore.QRect(85, 60, 231, 51))
        self.label_2.setObjectName("label_2")
        # self.label_3 = QtWidgets.QLabel(start)
        # self.label_3.setObjectName("label_3")
        self.retranslateUi(start)
        QtCore.QMetaObject.connectSlotsByName(start)

    def retranslateUi(self, start):
        _translate = QtCore.QCoreApplication.translate
        start.setWindowTitle(_translate("start", "Form"))
        # png = QtGui.QPixmap("./test1/3.jpg").scaled(start.size())
        # self.label_3.setPixmap(png)
        self.label.setText(_translate("start", "正在启动中......"))
        self.label_2.setText(_translate("start", "       愿你不负韶华，以梦为马"))
