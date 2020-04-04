import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtWidgets,QtGui
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt, QDir, QModelIndex, QUrl
from VisualMenu import VisualMenu
from VisualMenu2 import VisualMenu2
from VisualMenu3 import VisualMenu3
from VisualTable import VisualTable
from MakeHtml import Classes_Bar_Line,Classes_Bar_Pie,WH_AREA_Compose,WH_Bi_Bar_Pie
from Start import Ui_Start
from Login import Ui_Login
from RoiPicMenu import Pic_Menu
from RemotePicMenu import Pic_Menu2
from PyQt5.QtCore import QTimer
import os

class Visual_Menu(QtWidgets.QWidget,VisualMenu):
    def __init__(self, parent=None):
        super(Visual_Menu,self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_2)
        self.comboBox.currentIndexChanged.connect(lambda: self.change_html(self.comboBox.currentIndex(),self.comboBox_2.currentIndex()))
        self.comboBox_2.currentIndexChanged.connect(lambda: self.change_style(self.comboBox_2.currentIndex()))
    def change_style(self,box):
        if box == 0:
            self.comboBox.setItemText(0,"饼图-直方图")
            self.comboBox.setItemText(1, "折线图-直方图")
            print("sss")
            self.myHtml.reload()
            self.myHtml.load(QUrl("file:///"+"./html/class_bar_pie.html"))
        elif box == 1:
            self.comboBox.setItemText(0, "长宽分布")
            self.comboBox.setItemText(1, "更新中")
            print("www")
            self.myHtml.reload()
            self.myHtml.load(QUrl("file:///"+"./html/wh_area_compose.html"))

    def change_html(self,box2,box1): # 第二个是风格选项，第一个是图像选择
        if box1 == 0:
            if  box2 == 0:
                self.myHtml.reload()
                self.myHtml.load(QUrl("file:///"+"./html/class_bar_pie.html"))
            elif box2 == 1:
                self.myHtml.reload()
                self.myHtml.load(QUrl("file:///"+"./html/class_bar_line.html"))
        elif box1 == 1:
            if box2 ==0:
                self.myHtml.reload()
                self.myHtml.load(QUrl("file:///"+"./html/wh_area_compose.html"))
            else:
                pass
class Visual_Menu2(QtWidgets.QWidget, VisualMenu2):
    def __init__(self, parent=None):
        super(Visual_Menu2, self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_2)

class Visual_Menu3(QtWidgets.QWidget, VisualMenu3):
    def __init__(self, parent=None):
        super(Visual_Menu3, self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout_2)


class Visual_Table(QtWidgets.QWidget, VisualTable):
    def __init__(self, parent=None):
        super(Visual_Table, self).__init__(parent)
        self.setupUi(self)
        self.setLayout(self.verticalLayout)
        self.comboBox.currentIndexChanged.connect(lambda: self.change_type(self.comboBox.currentIndex()))
        self.classA = []  # w:h<0.5
        self.classB = []  # w:h>0.5<1
        self.classC = []  # w:h>1<2
        self.classD = []  # w:h>2<2.5
        self.classE = []  # w:h>2.5
        self.dict_index = {
            "0": self.classA,
            "1": self.classB,
            "2": self.classC,
            "3": self.classD,
            "4": self.classE
        }

    def load_data(self, rois):
        # 将roi按早长宽比分类
        for roi in rois:
            rate = roi.width / roi.height
            if rate < 0.5:
                self.classA.append(roi)
            elif 0.5 <= rate < 1:
                self.classB.append(roi)
            elif 1 <= rate < 2:
                self.classC.append(roi)
            elif 2 <= rate < 2.5:
                self.classD.append(roi)
            else:
                self.classE.append(roi)
        l = len(self.classA)
        self.tableWidget.setRowCount(l)
        i = 0
        for roi in self.classA:
            rate = QtWidgets.QTableWidgetItem("1:" + str(format(roi.height / roi.width, ".1f")))
            file_location = QtWidgets.QTableWidgetItem(roi.location)
            roi_location = QtWidgets.QTableWidgetItem("x: " + str(roi.xmin) + " y: " + str(roi.ymin))
            width_and_height = QtWidgets.QTableWidgetItem("长: " + str(roi.width) + " 宽: " + str(roi.height))
            self.tableWidget.setItem(i, 0, rate)
            self.tableWidget.setItem(i, 1, file_location)
            self.tableWidget.setItem(i, 2, roi_location)
            self.tableWidget.setItem(i, 3, width_and_height)
            i += 1

    def change_type(self, box1):
        self.tableWidget.clearContents()
        l = len(self.dict_index[str(box1)])
        self.tableWidget.setRowCount(l)
        i = 0
        for roi in self.dict_index[str(box1)]:
            rate = QtWidgets.QTableWidgetItem("1:" + str(format(roi.height / roi.width, ".1f")))
            file_location = QtWidgets.QTableWidgetItem(roi.location)
            roi_location = QtWidgets.QTableWidgetItem("x: " + str(roi.xmin) + " y: " + str(roi.ymin))
            width_and_height = QtWidgets.QTableWidgetItem("长: " + str(roi.width) + " 宽: " + str(roi.height))
            self.tableWidget.setItem(i, 0, rate)
            self.tableWidget.setItem(i, 1, file_location)
            self.tableWidget.setItem(i, 2, roi_location)
            self.tableWidget.setItem(i, 3, width_and_height)
            i += 1
            
class MyStart(QtWidgets.QWidget, Ui_Start):
    def __init__(self, parent=None):
        super(MyStart, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        # 定义时间超时连接start_app
        self.timer.timeout.connect(self.go)
        # 定义时间任务是一次性任务
        self.timer.setSingleShot(True)
        # 启动时间任务
        self.timer.start(3000)

    def go(self):
        # time.sleep(5)
        self.timer.stop()
        self.close()
        self.firstPage = Main_Menu()
        self.firstPage.show()
class MyLogin(QMainWindow, Ui_Login):
    def __init__(self, parent=None):
        super(MyLogin, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)

    def login(self):
        stu_no = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        if stu_no == "2017214880" and passwd == "123456":
            self.close()
            self.main_menu = Main_Menu()
            self.main_menu.show()

        # if len(stu_no) == 10:
        #     if self.radioButton_2.isChecked():
        #         if db.login(stu_no, passwd, 0) == True:
        #             self.close()
        #             self.stu_menu = Stu_Menu()
        #             self.stu_menu.show()
        #         else:
        #             button = QMessageBox.warning(self, "失败", "是否重新登录",
        #                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        #             if button == QMessageBox.Ok:
        #                 self.lineEdit_2.setText("")
        #                 self.lineEdit.setText("")

        #             else:
        #                 self.close()
        #     else:
        #         if db.login(stu_no, passwd, 1) == True:
        #             self.close()
        #             self.manager_menu = Manager_Menu()
        #             self.manager_menu.show()
        #         else:
        #             button = QMessageBox.warning(self, "失败", "是否重新登录",
        #                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        #             if button == QMessageBox.Ok:
        #                 self.lineEdit_2.setText("")
        #                 self.lineEdit.setText("")

        #             else:
        #                 self.close()
        # else:
        #     button = QMessageBox.about(self, "失败", "学号错误")

    def register(self):
        stu_no = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        # if len(stu_no) == 10:
        #     if self.radioButton_2.isChecked():
        #         if db.register(stu_no, passwd, 0) == True:
        #             button = QMessageBox.about(self, "成功", "进入登录界面")
        #         else:
        #             button = QMessageBox.warning(self, "失败", "是否重新注册",
        #                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        #             if button == QMessageBox.Ok:
        #                 self.lineEdit_2.setText("")
        #                 self.lineEdit.setText("")
        #             else:
        #                 self.close()
        #     else:
        #         if db.register(stu_no, passwd, 1) == True:
        #             button = QMessageBox.about(self, "成功", "进入登录界面")
        #         else:
        #             button = QMessageBox.warning(self, "失败", "是否重新注册",
        #                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        #             if button == QMessageBox.Ok:
        #                 self.lineEdit_2.setText("")
        #                 self.lineEdit.setText("")
        #             else:
        #                 self.close()
        # else:
        #     button = QMessageBox.about(self, "失败", "学号错误")
class Main_Menu(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(Main_Menu,self).__init__(parent)
        self.setupUi(self)
        self.actionopen.triggered.connect(self.open_pic_menu)
        self.actionopen2.triggered.connect(self.open_pic_menu2)        
        self.actionviusal_menu1.triggered.connect(self.open_visual_menu)
        self.actionviusal_menu2.triggered.connect(self.open_visual_menu2)
        self.actionviusal_table2.triggered.connect(self.open_visual_table2)
        self.actionviusal_menu3.triggered.connect(self.open_visual_menu3)
    def open_pic_menu(self):
        self.pic_menu = Pic_Menu()
        self.pic_menu.openfile()
        # for i in range(self.centralwidget.count()):
        #     self.centralwidget.itemAt(i).widget().deleteLater()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.centralwidget.setLayout(self.pic_menu.mainLayout)
        self.actionviusal_menu1.setEnabled(True)
        self.actionviusal_table2.setEnabled(True)
    def open_pic_menu2(self):
        self.pic_menu2 = Pic_Menu2()
        self.pic_menu2.open_file()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.pic_menu2.horizontalLayout)
        self.actionviusal_menu3.setEnabled(True)
        # self.pic_menu2.make_html()
    def open_visual_menu(self):
        self.visual_menu = Visual_Menu()

        self.visual_menu.show()
    def open_visual_menu2(self):

        self.visual_menu = Visual_Menu2()
        self.visual_list1 = ["A", "B", "C", "D", "E"]
        self.visual_list2 = [len(self.visual_table.classA), len(self.visual_table.classB),
                             len(self.visual_table.classC), len(self.visual_table.classD),
                             len(self.visual_table.classE)]

        self.wh_bi_bar_pie = WH_Bi_Bar_Pie()
        self.wh_bi_bar_pie.make_bar_pie(self.visual_list1, self.visual_list2).render("./html/wh_bi_bar_pie.html")

        self.visual_menu.show()
    def open_visual_menu3(self):
        self.pic_menu2.make_html()
        self.visual_menu = Visual_Menu3()
        self.visual_menu.show()

        
    def open_visual_table2(self):
        self.visual_table = Visual_Table()
        self.actionviusal_menu2.setEnabled(True)
        self.visual_table.load_data(self.pic_menu.roi_list_many)
        self.visual_table.show()

    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Main_Menu()
    demo.show()
    sys.exit(app.exec_())
