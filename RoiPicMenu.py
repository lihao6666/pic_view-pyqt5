import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt, QDir, QModelIndex, QUrl
from ComboCheckBox import ComboCheckBox
from BoxesInputDialog import BoxInput
from ImageList import ImageList
from ImageArea import ImageArea
from MakeHtml import Classes_Bar_Line,Classes_Bar_Pie,WH_AREA_Compose
import xml.etree.ElementTree as ET
import os
import cv2
from numpy import fromfile,uint8

THUMB_WIDTH = 128
THUMB_HEIGHT = 128
THUMB_MIN = 64
THUMB_MAX = 256
FILE_TYPE = ['png', 'jpg', 'jpeg', 'tif', 'bmp', 'gif']
CLASSES = ['101', '102', '103', '104', '105', '106', '107', '112', '119', '120','001','002','003','004']
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
    '120': (75, 46, 72),
    '001':(0,0,255),
    '002':(0,255,0),
    '003':(255,0,0),
    '004':(0,255,255)
}

class ROI():
    def __init__(self, type, width, height, xmin, ymin, location):
        self.type = type
        self.width = width
        self.height = height
        self.xmin = xmin
        self.ymin = ymin
        self.location = location

class Pic_Menu(QtWidgets.QWidget):
    def __init__(self,parent = None):
        self.image_dir = ''
        self.image_map_list = []
        self.image_map = []
        self.image_index = 0
        self.image_name = ''
        self.classes_list = CLASSES
        self.roi_list_one = [] # 保存一张图片的roi
        self.roi_list_many = [] # 保存多张图片的roi


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
        if dir:
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
        image = cv2.imdecode(fromfile(file_path, dtype=uint8), -1)
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
            # if (cls in self.classes_list) and (self.high >= width * height >= self.low):
            if cls in self.classes_list:
                cv2.rectangle(image, (b[0], b[2]), (b[1], b[3]), COLORS[cls], 2)
                cv2.putText(image, cls, (b[0], b[2] - 3), cv2.FONT_HERSHEY_COMPLEX, 0.8, COLORS[cls], 2)

            roi = ROI(type=cls, width=width, height=height, xmin=b[0], ymin=b[2], location=file_path)
            self.roi_list_one.append(roi)
        # 产生html
        # class_pie = Classes_Pie()
        # class_pie.bin(self.image_area.classes).render("./html/class_pie.html")#类别饼图

        # class_bar = Classes_Bar()
        # class_bar.bar(self.image_area.classes).render("./html/class_bar.html")#类别柱状图
        class_bar_line = Classes_Bar_Line()
        class_bar_line.make_bar_line(self.image_area.classes).render("./html/class_bar_line.html")

        class_bar_pie = Classes_Bar_Pie()
        class_bar_pie.make_bar_pie(self.image_area.classes).render("./html/class_bar_pie.html")

        wh_area_compose = WH_AREA_Compose()
        wh_area_compose.make_compose(self.image_area.width_list,self.image_area.height_list).render("./html/wh_area_compose.html")

        size = (int(self.image_area.width()), int(self.image_area.height()))
        # shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        shrink = image
        print(shrink.shape)
        show_image = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  shrink.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        return show_image
    def show_image(self, image):

        self.image_area.load_image(image)
    #这个是最左边文文件夹改变时的变化
    def search_file(self, dirpath, folder):
        for image_path in os.listdir(dirpath):
            if os.path.isdir(os.path.join(dirpath, image_path)):
                if folder == '':
                    next_folder = image_path
                else:
                    next_folder = folder + '/' + image_path
                self.search_file(os.path.join(dirpath, image_path), next_folder)
            else:
                item = image_path
                if item.split('.')[-1] in FILE_TYPE:
                    if folder == '':
                        item = image_path
                    else:
                        item = folder + '/' + image_path
                    self.image_map.append(item)
    def get_rois(self):
        self.roi_list_many.clear()
        for image in self.image_map:
            image_path = os.path.join(self.image_dir, image)
            # 获取文件名，除掉前缀
            file_name = os.path.splitext(image_path)[0]
            xml_path = file_name + ".xml"

            in_file = open(xml_path)
            tree = ET.parse(in_file)
            root = tree.getroot()
            # 记录展示数据
            for obj in root.iter('object'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text),
                     int(xmlbox.find('ymax').text))
                width = b[1] - b[0]
                height = b[3] - b[2]
                roi = ROI(type=cls, width=width, height=height, xmin=b[0], ymin=b[2], location=image)
                self.roi_list_many.append(roi)
                
    def dirTreeClicked(self):
        print('dirTreeClicked')
        # 获取选择的路径
        pathSelected = self.dirModel.filePath(self.dirTreeView.selectedIndexes()[0])
        print('pathSelected   ', pathSelected)
        self.image_dir = pathSelected
        # 遍历路径下的媒体文件
        self.image_map.clear()
        self.image_index = 0
        # 检索多层数据
        self.search_file(pathSelected, '')
        # 显示文件夹第一张图片
        if len(self.image_map) > 0:
            self.image_map_list = self.image_map
            # print(self.image_dir, self.image_map)
            self.image_list.set_items(self.image_map)
            self.image_name = self.image_map[0]
            self.image_list.set_highlight(self.image_index)
            try:
                image_name = self.image_map[0]
                file_path = os.path.join(self.image_dir, image_name)
                print("image_dir:", self.image_dir)
                print("image_name:", image_name)
                print("filepath:", file_path)
                show_image = self.get_image(file_path)
                self.show_image(show_image)
            except Exception as e:
                print(u'出错了', e)
        else:
            self.image_list.set_items(['空'])
            self.image_area.setStyleSheet("background-color: rgb(255,255, 255); border:1px solid black")
        # 统计所有ROI
        self.get_rois()
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