from PyQt5.QtWidgets import QApplication
import sys
from VisualMenu3 import VisualMenu3
from PyQt5 import QtWidgets
from MakeHtml import Classes_Bar_Pie,WH_AREA_Compose

dic = ['101','102','101','101','102','105','103','104']
width = [43, 39, 61, 52, 55, 33, 50, 70]
height = [39, 37, 58, 43, 43, 25, 80, 90]

class Visual_Menu(QtWidgets.QWidget,VisualMenu3):
    def __init__(self, parent=None):
        super(Visual_Menu,self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_2)
if __name__ == '__main__':
    # class_bar_pie = Classes_Bar_Pie()
    # class_bar_pie.make_bar_pie(dic).render("./html/class_bar_pie.html")
    # wh_area_compose = WH_AREA_Compose()
    # wh_area_compose.make_compose(width,height).render("./html/wh_area_compose.html")
    
    app=QApplication(sys.argv)
    demo=Visual_Menu()
    demo.show()
    sys.exit(app.exec_())