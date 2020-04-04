# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\编程文件\python\图片分类查询系统\ui\Remote.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from RemoteArea import RemoteArea
import cv2
import os
from MakeHtml import Pixel_Bar_Pie
from numpy import fromfile,uint8

DI = {
        "苗木": [0, 229, 254],
        "果园,柑橘": [0, 254, 162],
        "休闲农业": [254, 212, 0],
        "粮田,水稻": [0, 5, 255],
        "其它": [255, 101, 0],
        "经作": [0, 255, 50],
        "Background": [0, 0, 0],
        "菜田,蔬菜": [0, 117, 255],
        "林地,廊道,生态林": [178, 254, 0],
        "水产": [67, 255, 0],
        "未确定用途": [255, 0, 16]
}

class Pic_Menu2(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Pic_Menu2, self).__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pic_area1 = RemoteArea()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic_area1.sizePolicy().hasHeightForWidth())
        self.pic_area1.setSizePolicy(sizePolicy)
        self.pic_area1.setObjectName("pic_area1")
        self.horizontalLayout.addWidget(self.pic_area1)
        self.pic_area2 = RemoteArea()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic_area2.sizePolicy().hasHeightForWidth())
        self.pic_area2.setSizePolicy(sizePolicy)
        self.pic_area2.setObjectName("pic_area2")
        self.horizontalLayout.addWidget(self.pic_area2)

    def open_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, "选取图片", "./", "Image Files(*.png *.jpg *.tif)")
        pic1_name = name[0]
        pic2_name = pic1_name.replace('.tif', '-res.png')

        if pic1_name:

            image = cv2.imdecode(fromfile(pic1_name, dtype=uint8), -1)

            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            shrink = image
            show_image = QtGui.QImage(shrink.data,
                                    shrink.shape[1],
                                    shrink.shape[0],
                                    shrink.shape[1] * 3,
                                    QtGui.QImage.Format_RGB888)
            self.pic_area1.load_image(show_image)
            self.pic_area1.file_path = pic1_name

            image2 = cv2.imdecode(fromfile(pic2_name, dtype=uint8), -1)
            # image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
            shrink = image2
            show_image2 = QtGui.QImage(shrink.data,
                                    shrink.shape[1],
                                    shrink.shape[0],
                                    shrink.shape[1] * 3,
                                    QtGui.QImage.Format_RGB888)
            self.pic_area2.load_image(show_image2)
            self.pic_area2.file_path = pic2_name

            self.pic_area1.other_pic = self.pic_area2
            self.pic_area1.mask_pic = image2
            self.pic_area2.other_pic = self.pic_area1
            self.pic_area2.mask_pic = image2
    def make_html(self):
        infoX = [ "苗木",
        "果园",
        "农业",
        "粮田",
        "其它",
        "经作",
        "背景",
        "菜田",
        "林地",
        "水产",
        "未确定"]
        infoY = [0,0,0,0,0,0,0,0,0,0,0]
        for i in range(self.pic_area2.mask_pic.shape[0]):
            for j in range(self.pic_area2.mask_pic.shape[1]):
                    pixel = list(self.pic_area2.mask_pic[i][j])
                    index = list(DI.values()).index(pixel) # 获取下标
                    infoY[index] += 1
        print(infoY)
        info = []
        info.append(infoX)
        info.append(infoY)

        self.pixel_bar_pie = Pixel_Bar_Pie()
        self.pixel_bar_pie.make_bar_pie(infoX,infoY).render("./html/pixel_bar_pie.html")



    def get_res_pic(self, image):
        pass
