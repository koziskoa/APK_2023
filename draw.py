import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
from math import *
# sample comment
class Draw(QWidget):
    def __init__(self, *argsd, **kwargs):
        super().__init__(*argsd, **kwargs)
        self.__polyg_list = []
        #self.point_list = []
        self.__q = QPointF()
        self.is_highlighted = []
        self.__q = QPointF(-50, -50)

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click and its coords
        x = e.position().x()
        y = e.position().y()

        #add point to polygon
        #if self.__add_vertex:
           #create point P se souřadnicemi X a Y
            #p = QPointF(x,y)
        #append p to polygon (list)
            #self.__pol.append(p)
        self.__q.setX(x)
        self.__q.setY(y)

        self.is_highlighted = [0] * len(self.__polyg_list)
        #repaint screen
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        #draw polygon
        #create graphic object - vytvoříme nový objekt qpainter
        qp = QPainter(self)

        #start draw
        qp.begin(self)

        #set attributes - barva čáry
        qp.setPen(Qt.GlobalColor.blue)
        #qp.setBrush(Qt.GlobalColor.yellow)

        for i in range(len(self.__polyg_list)):
            if self.is_highlighted[i] == 1 or self.is_highlighted[i] == -1:
                qp.setBrush(Qt.GlobalColor.cyan)

            else:
                qp.setBrush(Qt.GlobalColor.yellow)

            qp.drawPolygon(self.__polyg_list[i])

        d = 4
        qp.drawEllipse(int(self.__q.x() - d / 2), int(self.__q.y() - d / 2), d, d)

        qp.end()

    # def switchSource(self):
    #     move point or add vertex
    #     self.__add_vertex = not(self.__add_vertex)

    def getPoint(self):
        #get point
        return  self.__q
    def getPolygonList(self):
        #get polygon
        return  self.__polyg_list

    #def resizeWindowEvent(self, ):

    def findBoundingPoints(self, p:QPointF, xmin, ymin, xmax, ymax):
        if p.x() < xmin:
            xmin = p.x()
        if p.y() < ymin:
            ymin = p.y()
        if p.x() > xmax:
            xmax = p.x()
        if p.y() > ymax:
            ymax = p.y()
        return xmin, ymin, xmax, ymax

    def resizePolygons(self, xmin, ymin, xmax, ymax):
        canvas_height = self.frameGeometry().height()
        canvas_width = self.frameGeometry().width()
        for polygon in self.__polyg_list:
            for point in polygon:
                new_x = int((point.x() - xmin) * canvas_width/(xmax - xmin))
                new_y = int((point.y() - ymin) * canvas_height/(ymax - ymin))
                point.setX(new_x)
                point.setY(new_y)

    def detectKrovak(self, ymin, ymax, epsg):
        if epsg == "EPSG:5514":
            krovak_ymin = ymax
            krovak_ymax = ymin
            return krovak_ymin, krovak_ymax
        else:
            return ymin, ymax

    def iterate_coords(self, data):
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        epsg = data["crs"]["properties"]["name"]

        # Check first feature for coordinates
        if "coordinates" in data["features"][0]["geometry"]:
            for feature in data["features"]:
                pol = QPolygonF()
                if isinstance(feature["geometry"]["coordinates"], list):
                    for coords in feature["geometry"]["coordinates"][0]:
                        p=QPointF(int(coords[0]),int(coords[1]))
                        pol.append(p)
                        xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
                    self.__polyg_list.append(pol)
                    self.is_highlighted.append(0)
            ymin, ymax = self.detectKrovak(ymin, ymax, epsg)

            self.resizePolygons(xmin, ymin, xmax, ymax)
            self.repaint()
        else:
            sys.exit()

