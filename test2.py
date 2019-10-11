import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtWidgets,QtGui,QtCore
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt, QDir, QModelIndex, QUrl
from ComboCheckBox import ComboCheckBox
from BoxesInputDialog import BoxInput
from ImageList import ImageList
from ImageArea import ImageArea
from VisualMenu import VisualMenu
from MakeHtml import Classes_Pie,Classes_Bar
from start import Ui_Start
from login import Ui_Login
from PyQt5.QtCore import QTimer
import numpy as np
import xml.etree.ElementTree as ET
import os
import cv2

THUMB_WIDTH = 128
THUMB_HEIGHT = 128
THUMB_MIN = 64
THUMB_MAX = 256
FILE_TYPE = ['png', 'jpg', 'jpeg', 'tif', 'bmp', 'gif']
CLASSES = ['101', '102', '103', '104', '105', '106', '107', '112', '119', '120']
COLORS = {
    '101': (128, 128, 128),
    '102': (0, 192, 255),
    '103': (202, 36, 204),
    '104': (77, 80, 192),
    '105': (0, 0, 255),
    '106': (0, 255, 255),
    '107': (245, 248, 10),
    '112': (0, 255, 0),
    '119': (0, 0, 0),
    '120': (75, 46, 72)
}

class Pic_Menu(QtWidgets.QWidget):
    def __init__(self,parent = None):
        self.image_dir = ''
        self.image_map_list = []
        self.image_map = []
        self.image_index = 0
        self.image_name = ''
        self.classes_list = CLASSES
        self.low = 0
        self.high = 1024 * 1024
        super(Pic_Menu, self).__init__(parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.containerLayout = QtWidgets.QVBoxLayout()  # 垂直图片展示布局管理器
        self.filtrate_area = QtWidgets.QHBoxLayout()  # 上部类别布局管理器
        self.image_area_layout = QtWidgets.QHBoxLayout()  # 中间图片展示布局管理包括文件列表和展示
        self.photo_change_area = QtWidgets.QHBoxLayout()  # 底部图片切换布局管理

        self.mainSpliter = QtWidgets.QSplitter(Qt.Horizontal)
        self.dirModel = QtWidgets.QDirModel(self)
        self.dirModel.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        # 文件夹列表view
        self.dirTreeView = QtWidgets.QTreeView()
        # 绑定model
        self.dirTreeView.setModel(self.dirModel)
        print(QDir.currentPath())
        # self.dirTreeView.setRootIndex(self.dirModel.index(dir))  # 设置文件夹路径
        # self.dirTreeView.expand(self.dirModel.index(dir)) #展开当前文件夹
        # self.dirTreeView.scrollTo(self.dirModel.index(dir)) #视图滚动
        self.dirTreeView.hideColumn(1)  # 控制显示列数据
        self.dirTreeView.hideColumn(2)
        self.dirTreeView.hideColumn(3)
        # DirTree事件响应
        self.dirTreeView.selectionModel().selectionChanged.connect(self.dirTreeClicked)
        self.mainSpliter.addWidget(self.dirTreeView)

        self.imageContainer = QtWidgets.QFrame(self.mainSpliter)
        self.imageContainer.setMinimumWidth(int(self.geometry().width() * 0.6))
        # 类别筛选框

        classLabel = QtWidgets.QLabel("类别选择")
        classLabel.setFixedWidth(60)
        self.filtrate_area.addWidget(classLabel)

        self.check_box = ComboCheckBox(CLASSES)
        self.check_box.setFixedWidth(350)
        self.filtrate_area.addWidget(self.check_box)

        # bounding-box筛选框
        self.box_input = BoxInput()
        self.box_input.setFixedWidth(200)
        self.filtrate_area.addWidget(self.box_input)

        self.confirm_button = QtWidgets.QPushButton('确定')
        self.confirm_button.setFixedWidth(150)
        self.confirm_button.clicked.connect(self.confim_choice)
        self.filtrate_area.addWidget(self.confirm_button)
        self.containerLayout.addLayout(self.filtrate_area)

        # 图片显示区域

        self.image_list = ImageList()
        self.image_list.image_name.connect(self.get_name)
        # self.image_list.connect(self, QtCore.SIGNAL("transfer_child"), self.w2.receive)
        self.image_area_layout.addWidget(self.image_list)

        # self.item_area = QtWidgets.QWidget()
        # self.item_area.setFixedSize(800, 800)
        #
        # self.image_area = QtWidgets.QLabel(self.item_area)
        # self.image_area.setFixedSize(800, 800)
        # self.image_area.setStyleSheet("background-color: rgb(255, 255, 255); border:1px solid black")
        #
        # self.image_area_layout.addWidget(self.item_area)
        self.image_area = ImageArea()

        self.image_area_layout.addWidget(self.image_area)
        self.containerLayout.addLayout(self.image_area_layout)

        # 图片切换按钮
        self.pre_photo_button = QtWidgets.QPushButton('上一张')
        self.next_photo_button = QtWidgets.QPushButton('下一张')
        self.pre_photo_button.setFixedWidth(150)
        self.next_photo_button.setFixedWidth(150)
        self.pre_photo_button.clicked.connect(self.pre_photo)
        self.next_photo_button.clicked.connect(self.next_photo)
        self.photo_change_area.addWidget(self.pre_photo_button)
        self.photo_change_area.addWidget(self.next_photo_button)
        self.containerLayout.addLayout(self.photo_change_area)

        self.imageContainer.setLayout(self.containerLayout)
        self.mainSpliter.addWidget(self.imageContainer)

        self.mainLayout.addWidget(self.mainSpliter)
        # self.setLayout(self.mainLayout)
    def openfile(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,"选取数据文件夹","./")
        print(dir)
        self.show_files(dir)
    def show_files(self,dir):

        self.dirTreeView.setRootIndex(self.dirModel.index(dir)) #设置文件夹路径
        # self.mainSpliter.replaceWidget(0,self.dirTreeView)
        # self.dirTreeView.selectAll()
        # self.dirTreeClicked()
    def get_name(self, name):
        self.image_name = name
        self.image_index = self.image_map.index(name)

        file_path = os.path.join(self.image_dir, name)
        show_image = self.get_image(file_path)
        self.show_image(show_image)

    def get_image(self, file_path):
        image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.image_area.file_path = file_path

        image_path = file_path
        xml_path = image_path.replace('JPEGImages', 'Annotations')
        xml_path = xml_path.replace('jpg', 'xml')

        in_file = open(xml_path)
        tree = ET.parse(in_file)
        root = tree.getroot()
        # 记录展示数据
        self.image_area.classes = []
        self.image_area.width_list = []
        self.image_area.height_list = []
        for obj in root.iter('object'):
            cls = obj.find('name').text
            self.image_area.classes.append(cls)
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text),
                 int(xmlbox.find('ymax').text))
            width = b[1] - b[0]
            height = b[3] - b[2]
            self.image_area.width_list.append(width)
            self.image_area.height_list.append(height)
            if (cls in self.classes_list) and (self.high >= width * height >= self.low):
                cv2.rectangle(image, (b[0], b[2]), (b[1], b[3]), COLORS[cls], 2)
                cv2.putText(image, cls, (b[0], b[2] - 3), cv2.FONT_HERSHEY_COMPLEX, 0.8, COLORS[cls], 2)
        # 产生html
        class_pie = Classes_Pie()
        class_pie.bin(self.image_area.classes).render("./html/class_pie.html")#类别饼图

        class_bar = Classes_Bar()
        class_bar.bar(self.image_area.classes).render("./html/class_bar.html")#类别柱状图

        print(self.image_area.width_list)
        print(self.image_area.height_list)

        size = (int(self.image_area.width()), int(self.image_area.height()))
        shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        print(shrink.shape)
        show_image = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  shrink.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        return show_image
    def show_image(self, image):

        self.image_area.load_image(image)

    def dirTreeClicked(self):
        print('dirTreeClicked')
        # 获取选择的路径
        pathSelected = self.dirModel.filePath(self.dirTreeView.selectedIndexes()[0])
        print('pathSelected   ', pathSelected)
        self.image_dir = pathSelected
        # 遍历路径下的媒体文件
        self.image_map.clear()
        self.image_index = 0
        for image_path in os.listdir(pathSelected):
            if os.path.isdir(os.path.join(pathSelected, image_path)):
                for item in os.listdir(os.path.join(pathSelected, image_path)):
                    if item.split('.')[-1] in FILE_TYPE:
                        item = image_path + '/' + item
                        self.image_map.append(item)
            else:
                item = image_path
                if item.split('.')[-1] in FILE_TYPE:
                    self.image_map.append(item)
        if len(self.image_map) > 0:
            self.image_map_list = self.image_map
            # print(self.image_dir, self.image_map)
            self.image_list.set_items(self.image_map)
            self.image_name = self.image_map[0]
            self.image_list.set_highlight(self.image_index)
            try:
                image_name = self.image_map[0]
                file_path = os.path.join(self.image_dir, image_name)
                show_image = self.get_image(file_path)
                self.show_image(show_image)
            except Exception as e:
                print(u'出错了', e)
                pass
        else:
            self.image_list.set_items(['空'])
            self.image_area.setStyleSheet("background-color: rgb(255,255, 255); border:1px solid black")

    def pre_photo(self):
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index += 1
        self.image_name = self.image_map[self.image_index]
        self.image_list.set_highlight(self.image_index)

        image_name = self.image_map[self.image_index]
        file_path = os.path.join(self.image_dir, image_name)
        show_image = self.get_image(file_path)
        self.show_image(show_image)

    def next_photo(self):
        self.image_index += 1
        if self.image_index == len(self.image_map):
            self.image_index -= 1
        self.image_name = self.image_map[self.image_index]
        self.image_list.set_highlight(self.image_index)

        image_name = self.image_map[self.image_index]
        file_path = os.path.join(self.image_dir, image_name)
        show_image = self.get_image(file_path)
        self.show_image(show_image)

    def confim_choice(self):
        classes_list = self.check_box.Selectlist()
        low, high = self.box_input.get_num()
        if classes_list:
            self.classes_list = classes_list
        if low and high:
            self.low = int(low)
            self.high = int(high)

        image_map_temp = []
        for image_name in self.image_map_list:
            image_path = os.path.join(self.image_dir, image_name)
            xml_path = image_path.replace('JPEGImages', 'Annotations')
            xml_path = xml_path.replace('jpg', 'xml')

            in_file = open(xml_path)
            tree = ET.parse(in_file)
            root = tree.getroot()
            for obj in root.iter('object'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                width = b[1] - b[0]
                height = b[3] - b[2]
                if (cls in self.classes_list) and (self.high > width > self.low or self.high > height > self.low):
                    image_map_temp.append(image_name)
                    break
        self.image_map = image_map_temp
        if self.image_map:
            try:
                self.image_index = self.image_map.index(self.image_name)
            except Exception as e:
                if len(self.image_map) > 0:
                    self.image_index = 0
        else:
            self.image_index = -1

        if not self.image_index == -1:
            self.image_list.set_items(self.image_map)
            self.image_list.set_highlight(self.image_index)
            image_name = self.image_map[self.image_index]
            file_path = os.path.join(self.image_dir, image_name)
            show_image = self.get_image(file_path)
            self.show_image(show_image)
        else:
            self.image_list.set_items(['空'])
            self.image_area.setStyleSheet("background-color: rgb(255,255, 255); border:1px solid black")
        # print(classes_list, low, high)
        # print(image_map_temp)
        # print(self.image_map, self.image_index, self.image_name)
        # print(self.classes_list, self.high, self.low)
class Visual_Menu(QtWidgets.QWidget,VisualMenu):
    def __init__(self, parent=None):
        super(Visual_Menu,self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(lambda: self.change_style(self.comboBox.currentIndex(),self.comboBox_2.currentIndex()))
        self.comboBox_2.currentIndexChanged.connect(lambda: self.change_style(self.comboBox.currentIndex(),self.comboBox_2.currentIndex()))
    # def change_type(self,box1,box2):
    #     if type == 0:
    #         self.myHtml.reload(QUrl("file:///D:/编程文件/python/图片分类查询系统/html/class_pie.html"))
    #     elif type ==1:
    #         self.myHtml.reload(QUrl("file:///D:/编程文件/python/图片分类查询系统/html/class_bar.html"))
    #     else:
    #         pass
    def change_style(self,box1,box2):
        if box1 == 0 and box2 == 0:
            self.myHtml.reload()
            self.myHtml.load(QUrl("file:///D:/编程文件/python/图片分类查询系统/html/class_pie.html"))
        elif box1 == 1 and box2 ==0:
            self.myHtml.reload()
            self.myHtml.load(QUrl("file:///D:/编程文件/python/图片分类查询系统/html/class_bar.html"))
        else:
            print("还未构建")
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
        self.mylogin = MyLogin()
        self.mylogin.show()
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
        self.pic_menu = Pic_Menu()
        self.actionopen.triggered.connect(self.open_pic_menu)
        self.actionviusal_menu.triggered.connect(self.open_visual_menu)
    def open_pic_menu(self):
        self.pic_menu.openfile()
        self.centralwidget.setLayout(self.pic_menu.mainLayout)
        self.actionviusal_menu.setEnabled(True)
    def open_visual_menu(self):
        self.visual_menu = Visual_Menu()
        self.visual_menu.show()



    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Main_Menu()
    demo.show()
    sys.exit(app.exec_())
