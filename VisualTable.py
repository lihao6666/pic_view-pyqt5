# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\编程文件\python\图片筛查系统-ROI\Visual_Table.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class VisualTable(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 670)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 651))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 15, 600, 15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,150)
        self.tableWidget.setColumnWidth(3,200)

        self.tableWidget.setHorizontalHeaderLabels(["长宽比","文件位置","图片位置","长宽"])
        self.tableWidget.setObjectName("tableWidget")

        # self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        # self.textEdit.setSizePolicy(sizePolicy)
        # self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "长宽比分布"))
        self.comboBox.setItemText(0, _translate("Form", "A"))
        self.comboBox.setItemText(1, _translate("Form", "B"))
        self.comboBox.setItemText(2, _translate("Form", "C"))
        self.comboBox.setItemText(3, _translate("Form", "D"))
        self.comboBox.setItemText(4, _translate("Form", "E"))
        # self.comboBox.setItemText(5, _translate("Form", "F"))

