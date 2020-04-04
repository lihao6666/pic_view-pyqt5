import sys, cv2
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
import os, string
import math
from ComboCheckBox import ComboCheckBox
from BoxesInputDialog import BoxInput
from ImageList import ImageList
import xml.etree.ElementTree as ET

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


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        self.image_dir = ''
        self.image_map_list = []
        self.image_map = []
        self.image_index = 0
        self.image_name = ''
        self.classes_list = CLASSES
        self.low = 0
        self.high = 1024 * 1024

        app = QtWidgets.QApplication(sys.argv)
        super(MainWindow, self).__init__()

        self.setWindowTitle("数据集图像筛查系统")
        self.resize(1460, 1000)

        # 屏幕居中
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)

        self.show()

        mainSpliter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # 文件夹列表model
        self.dirModel = QtWidgets.QDirModel(self)
        # 只显示文件夹
        # self.dirModel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        # 文件夹列表view
        self.dirTreeView = QtWidgets.QTreeView()
        # 绑定model
        self.dirTreeView.setModel(self.dirModel)
        self.dirTreeView.hideColumn(1)
        self.dirTreeView.hideColumn(2)
        self.dirTreeView.hideColumn(3)
        # DirTree事件响应
        self.dirTreeView.selectionModel().selectionChanged.connect(self.dirTreeClicked)
        mainLayout = QtWidgets.QVBoxLayout()
        mainSpliter.addWidget(self.dirTreeView)

        self.imageContainer = QtWidgets.QFrame(mainSpliter)
        self.imageContainer.setMinimumWidth(self.geometry().width() * 0.6)

        containerLayout = QtWidgets.QVBoxLayout()
        # 类别筛选框
        filtrate_area = QtWidgets.QHBoxLayout()

        classLabel = QtWidgets.QLabel("类别选择")
        classLabel.setFixedWidth(60)
        filtrate_area.addWidget(classLabel)

        self.check_box = ComboCheckBox(CLASSES)
        self.check_box.setFixedWidth(350)
        filtrate_area.addWidget(self.check_box)

        # bounding-box筛选框
        self.box_input = BoxInput()
        self.box_input.setFixedWidth(200)
        filtrate_area.addWidget(self.box_input)

        self.confirm_button = QtWidgets.QPushButton('确定')
        self.confirm_button.setFixedWidth(150)
        self.confirm_button.clicked.connect(self.confim_choice)
        filtrate_area.addWidget(self.confirm_button)
        containerLayout.addLayout(filtrate_area)

        # 图片显示区域
        image_area_layout = QtWidgets.QHBoxLayout()

        self.image_list = ImageList()
        self.image_list.image_name.connect(self.get_name)
        # self.image_list.connect(self, QtCore.SIGNAL("transfer_child"), self.w2.receive)
        image_area_layout.addWidget(self.image_list)

        self.item_area = QtWidgets.QWidget()
        self.item_area.setFixedSize(800, 800)

        self.image_area = QtWidgets.QLabel(self.item_area)
        self.image_area.setFixedSize(800, 800)
        self.image_area.setStyleSheet("background-color: rgb(255, 255, 255); border:1px solid black")

        image_area_layout.addWidget(self.item_area)
        containerLayout.addLayout(image_area_layout)

        # 图片切换按钮
        photo_change_area = QtWidgets.QHBoxLayout()
        self.pre_photo_button = QtWidgets.QPushButton('上一张')
        self.next_photo_button = QtWidgets.QPushButton('下一张')
        self.pre_photo_button.setFixedWidth(150)
        self.next_photo_button.setFixedWidth(150)
        self.pre_photo_button.clicked.connect(self.pre_photo)
        self.next_photo_button.clicked.connect(self.next_photo)
        photo_change_area.addWidget(self.pre_photo_button)
        photo_change_area.addWidget(self.next_photo_button)
        containerLayout.addLayout(photo_change_area)

        self.imageContainer.setLayout(containerLayout)
        mainSpliter.addWidget(self.imageContainer)

        mainLayout.addWidget(mainSpliter)
        self.setLayout(mainLayout)
        sys.exit(app.exec_())

    def get_name(self, name):
        self.image_name = name
        self.image_index = self.image_map.index(name)

        file_path = os.path.join(self.image_dir, name)
        show_image = self.get_image(file_path)
        self.show_image(show_image)

    def get_image(self, file_path):
        image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image_path = file_path
        xml_path = image_path.replace('JPEGImages', 'Annotations')
        xml_path = xml_path.replace('jpg', 'xml')

        in_file = open(xml_path)
        tree = ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text),
                 int(xmlbox.find('ymax').text))
            width = b[1] - b[0]
            height = b[3] - b[2]
            if (cls in self.classes_list) and (self.high >= width * height >= self.low):
                cv2.rectangle(image, (b[0], b[2]), (b[1], b[3]), COLORS[cls], 2)
                cv2.putText(image, cls, (b[0], b[2] - 3), cv2.FONT_HERSHEY_COMPLEX, 0.8, COLORS[cls], 2)

        size = (int(self.image_area.width()), int(self.image_area.height()))
        shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        show_image = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  shrink.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        return show_image

    def show_image(self, image):
        self.image_area.setPixmap(QtGui.QPixmap.fromImage(image))

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
        print(image_map_temp)
        print(self.image_map, self.image_index, self.image_name)
        print(self.classes_list, self.high, self.low)


def main():
    MainWindow()


if __name__ == '__main__':
    main()
