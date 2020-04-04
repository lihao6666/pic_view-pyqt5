from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsItem, QGraphicsScene, QWidget, QMenu, QAction
from PyQt5 import QtGui
import cv2


class RemoteArea(QGraphicsView):
    def __init__(self):
        super(RemoteArea, self).__init__()
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: rgb(255, 255, 255); border:1px solid black")
        self.zoomscale = 1
        self.file_path = ""
        self.pic = None
        self.pixel = None
        self.di = {
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

    def load_image(self, image):
        self.pic = QtGui.QPixmap.fromImage(image)
        # self.pic2 = QtGui.QPixmap.fromImage(image)

        self.item = QGraphicsPixmapItem(self.pic)
        self.item.setFlag(QGraphicsItem.ItemIsMovable)
        # self.item2 = QGraphicsPixmapItem(self.pic2)

        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        # self.scene.addItem(self.item2)
        self.setScene(self.scene)
        self.item.setScale(self.zoomscale)

    # def mousePressEvent(self, event):
    #     if self.pic:
    #         if event.button() == Qt.LeftButton:
    #             self.mousePressPos = event.pos()
    #             self.mouseIsPress = True
    #             print(self.mousePressPos)
    #
    # def mouseReleaseEvent(self, event):
    #     if self.pic:
    #         if event.buttons() == Qt.LeftButton:
    #             self.mouseIsPress = False
    #
    # def mouseMoveEvent(self, event):
    #     if self.pic:
    #         if self.mouseIsPress:
    #             moveDistance = event.pos() - self.mousePressPos
    #             print(moveDistance.x())
    #             print(moveDistance.y())
    #             # self.scene.setSceneRect(self.item.x()+moveDistance.x(),self.item.y()+moveDistance.y(),self.item.)
    #             self.item.moveBy(self.item.x() + moveDistance.x(), self.item.y() + moveDistance.y())

    def wheelEvent(self, event):
        if self.pic:
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleX = angle.x()  # 水平滚过的距离(此处用不上)
            angleY = angle.y()  # 竖直滚过的距离
            if angleY < 0:
                self.zoomscale = self.zoomscale - angleY / 360
                if self.zoomscale <= 0:
                    self.zoomscale = 0.2
                self.item.setScale(self.zoomscale)
                self.other_pic.item.setScale(self.zoomscale)
                # print("滚轮上滚")
            else:  # 滚轮下滚
                self.zoomscale = self.zoomscale - angleY / 360
                if self.zoomscale >= 1.8:
                    self.zoomscale = 1.8
                self.item.setScale(self.zoomscale)
                self.other_pic.item.setScale(self.zoomscale)

                # print("鼠标滚轮下滚")  # 响应测试语句

    def contextMenuEvent(self, event):
        if self.pic:
            self.pixel = self.item.mapFromScene(self.mapToScene(event.pos())) #转换为相对像素位置，也就是点击图片像素点位置
            x = int(self.pixel.x())
            y = int(self.pixel.y())
            print("x:"+str(x),"y:"+str(y))
            mask_pic_pixel =  list(self.mask_pic[y][x])
            type_name = list(self.di.keys())[list(self.di.values()).index(mask_pic_pixel)]
            print(type_name)
            self.menu = QMenu(self)
            Qaction = self.menu.addAction(type_name)
            action = self.menu.exec_(self.mapToGlobal(event.pos()))
            if action == Qaction:
                pass

    # def show_old_pic(self):
    #     image = cv2.imdecode(np.fromfile(self.file_path, dtype=np.uint8), -1)
    #     # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #     # size = (self.width(),self.height())
    #     # shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    #     shrink = image
    #     show_image = QtGui.QImage(shrink.data,
    #                               shrink.shape[1],
    #                               shrink.shape[0],
    #                               shrink.shape[1] * 3,
    #                               QtGui.QImage.Format_RGB888)
    #     self.load_image(show_image)
