import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt5 import QtCore


class ImageList(QWidget):

    image_name = pyqtSignal(str)

    def __init__(self):
        super(ImageList, self).__init__()

        self.listwidget = QListWidget(self)
        self.listwidget.setFixedHeight(600)
        self.listwidget.clicked.connect(self.change_func)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.listwidget)

        self.setLayout(self.h_layout)

    def change_func(self):  # 7
        image_name = self.listwidget.currentItem().text()
        self.image_name.emit(image_name)

    def set_items(self, items):
        self.listwidget.clear()
        self.listwidget.addItems(items)

    def set_highlight(self, index):
        try:
            qt_index = self.listwidget.model().index(index)
            self.listwidget.setCurrentIndex(qt_index)
        except Exception as e:
            print(e)

