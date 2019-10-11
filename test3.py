from PyQt5.QtWidgets import QApplication
import sys
from VisualMenu import VisualMenu
from PyQt5 import QtWidgets

class Visual_Menu(QtWidgets.QWidget,VisualMenu):
    def __init__(self, parent=None):
        super(Visual_Menu,self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_2)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Visual_Menu()
    demo.show()
    sys.exit(app.exec_())