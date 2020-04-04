from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QWidget, QMenu, QAction, QGraphicsItem
from PyQt5 import QtGui
import cv2
from numpy import fromfile,uint8



class ImageArea(QGraphicsView):
    def __init__(self):
        super(ImageArea, self).__init__()
        self.setFixedSize(800,600)
        self.setStyleSheet("background-color: rgb(255, 255, 255); border:1px solid black")
        self.zoomscale = 1
        self.file_path = ""
        self.pic = None
    def load_image(self,image):
        self.pic = QtGui.QPixmap.fromImage(image)
        self.item = QGraphicsPixmapItem(self.pic)
        self.item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.setScene(self.scene)
        self.item.setScale(self.zoomscale)
    def wheelEvent(self, event):
        if self.pic :
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleX = angle.x()  # 水平滚过的距离(此处用不上)
            angleY = angle.y()  # 竖直滚过的距离
            if angleY < 0:
                self.zoomscale = self.zoomscale - angleY/360
                if self.zoomscale <= 0:
                    self.zoomscale = 0.2
                self.item.setScale(self.zoomscale)
                # print("滚轮上滚")
            else:  # 滚轮下滚
                self.zoomscale = self.zoomscale - angleY / 360
                if self.zoomscale >= 1.8:
                    self.zoomscale = 1.8
                self.item.setScale(self.zoomscale)
            
                # print("鼠标滚轮下滚")  # 响应测试语句
    def contextMenuEvent(self, event):
        if self.pic:
            self.menu = QMenu(self)
            Qaction = self.menu.addAction("查看原图")
            action = self.menu.exec_(self.mapToGlobal(event.pos()))
            if action == Qaction:
                self.show_old_pic()
    def show_old_pic(self):
        image = cv2.imdecode(fromfile(self.file_path, dtype=uint8), -1)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # size = (self.width(),self.height())
        # shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        shrink = image
        show_image = QtGui.QImage(shrink.data,
                                  shrink.shape[1],
                                  shrink.shape[0],
                                  shrink.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        self.load_image(show_image)




