from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
# sample comment
class Draw(QWidget):
    def __init__(self, *argsd, **kwargs):
        super().__init__(*argsd, **kwargs)

        #bude vykreslovat bod a polygon
        # query point a polygon
        self.__q = QPointF(0,0)
        self.__pol = QPolygonF()
        self.__add_vertex = True #primárně zadává vrchol
        pass

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click and its coords
        x = e.position().x()
        y = e.position().y()

        #add point to polygon
        if self.__add_vertex:
           #create point P se souřadnicemi X a Y
            p = QPointF(x,y)
        #append p to polygon (list)
            self.__pol.append(p)
        else:
            self.__q.setX(x)
            self.__q.setY(y)
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
        qp.setBrush(Qt.GlobalColor.yellow)
        qp.drawPolygon(self.__pol)
        #draw point
        d = 10
        qp.drawEllipse(int(self.__q.x()-d/2), int(self.__q.y()-d/2), d, d)
        qp.end()

    def switchSource(self):
        #move point or add vertex
        self.__add_vertex = not(self.__add_vertex)

    def getPoint(self):
        #get point
        return  self.__q
    def getPolygon(self):
        #get polygon
        return  self.__pol
    
    def read_data(self, e:QFileOpenEvent, name):
        with open(name, encoding="utf-8") as geojsonfile:
            reader = json.load(geojsonfile)
            polygons = iterate_coords(reader)
        return polygons
    
    def iterate_coords(self, data):
        pol=self.__pol
        for feature in data["features"]:
            if isinstance(feature["geometry"]["coordinates"],list):
                for coords in feature["geometry"]["coordinates"][0]:
                    p=QPointF(coords[0],coords[1])
                    pol.append(p)
            return pol
