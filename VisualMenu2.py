# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VisualMenu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame,QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class VisualMenu2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 670)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(50, 15, 400, 15)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        # self.comboBox_2.addItem("")
        # self.comboBox_2.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_2)
        # self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        # self.comboBox.setObjectName("comboBox")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("")
        # self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.myHtml = QWebEngineView()
        self.myHtml.load(QUrl("file:///"+"./html/wh_bi_bar_pie.html"))
        self.verticalLayout_2.addWidget(self.myHtml)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "可视化界面"))
        self.comboBox_2.setItemText(0, _translate("Form", "长宽分布"))
        # self.comboBox_2.setItemText(1, _translate("Form", "形态分布"))
        # self.comboBox_2.setItemText(2, _translate("Form", "面积分布"))
        # self.comboBox.setItemText(0, _translate("Form", "饼图-直方图"))
        # self.comboBox.setItemText(1, _translate("Form", "折线图-直方图"))
        # self.comboBox.setItemText(2, _translate("Form", "其它"))
