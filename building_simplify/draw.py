from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Building, convex hull and enclosing rectangle
        self.__pol = QPolygonF()
        self.__ch = QPolygonF()
        self.__er = QPolygonF()

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()

        #Add point to polygon
        p = QPointF(x,y)

        #Append p to polygon
        self.__pol.append(p)

        #Repaint screen
        self.repaint()

    def paintEvent(self, e:QPaintEvent):
        #Draw polygon

        #Create graphic object
        qp = QPainter(self)

        #Start draw
        qp.begin(self)

        #Set attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        #Draw building
        qp.drawPolygon(self.__pol)

        #Set attributes convex hull
        qp.setPen(Qt.GlobalColor.blue)
        #qp.setBrush(Qt.GlobalColor.yellow)

        #Draw ch
        qp.drawPolygon(self.__ch)

        #Set attributes enclosing rectangle
        qp.setPen(Qt.GlobalColor.red)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # draw enclosing rectangle
        qp.drawPolygon(self.__er)
        #End draw
        qp.end()

    def getPolygon(self):
        #Get polygon
        return self.__pol
    
    def setConvexHull(self, pol):
        #set chull
        self.__ch = pol

    def setEnclosingRectangle(self, pol: QPolygonF):
        self.__er = pol

    def clearCanvas(self):
        self.__pol = []
        self.__ch = []
        self.__er = []
        