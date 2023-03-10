from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
# sample comment
class Draw(QWidget):
    def __init__(self, *argsd, **kwargs):
        super().__init__(*argsd, **kwargs)
        self.polyg_list = []
        self.point_list = []
        #bude vykreslovat bod a polygon
        # query point a polygon
        self.__q = QPointF()
        #self.__pol = QPolygonF()
        #self.__add_vertex = True #primárně zadává vrchol
        self.is_highlighted = []
        pass

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

        self.is_highlighted = [False] * len(self.polyg_list)
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

        for i in range(len(self.polyg_list)):
            if self.is_highlighted[i]:
                qp.setBrush(Qt.GlobalColor.cyan)

            else:
                qp.setBrush(Qt.GlobalColor.yellow)

            qp.drawPolygon(self.polyg_list[i])

        #draw point
        d = 10
        qp.drawEllipse(int(self.__q.x()-d/2), int(self.__q.y()-d/2), d, d)
        qp.end()

    # def switchSource(self):
    #     move point or add vertex
    #     self.__add_vertex = not(self.__add_vertex)

    def getPoint(self):
        #get point
        return  self.__q
    def getPolygonList(self):
        #get polygon
        return  self.polyg_list
    
    def iterate_coords(self, data):
        for feature in data["features"]:
            pol = QPolygonF()
            if isinstance(feature["geometry"]["coordinates"],list):
                for coords in feature["geometry"]["coordinates"][0]:
                    p=QPointF(coords[0],coords[1])

                    pol.append(p)
                self.polyg_list.append(pol)
                self.is_highlighted.append(False)
        self.repaint()

