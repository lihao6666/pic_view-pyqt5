import sys
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit


class BoxInput(QWidget):
    def __init__(self):
        super(BoxInput,self).__init__()
        self.initUi()

    def initUi(self):
        # self.setWindowTitle("login")
        layout = QGridLayout()
        # self.setGeometry(600, 600, 400, 400)

        lowLabel = QLabel("下限")
        self.lowLineEdit = QLineEdit("")
        highLabel = QLabel("上限")
        self.highLineEdit = QLineEdit("")

        # layout.setSpacing(10)
        layout.addWidget(lowLabel,1,0)
        layout.addWidget(self.lowLineEdit,1,1)
        layout.addWidget(highLabel, 2, 0)
        layout.addWidget(self.highLineEdit, 2, 1)

        self.setLayout(layout)

    def get_num(self):
        low = self.lowLineEdit.text()
        high = self.highLineEdit.text()
        return low, high
