from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import * 
from Edge import * 
from random import *
from triangle import * 
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Building, convex hull and enclosing rectangle
        self.__points: list[QPoint3DF] = []
        self.__dt : list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []

    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()
        z = random()*100

        #create point
        p = QPoint3DF(x,y,z)

        #Append p to point cloud
        self.__points.append(p)

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

        #Draw points
        r = 10 # jako 10 pixelů
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2*r, 2*r)# x- r a y - r

        k = (510/(pi/2))

        
        # process triangles one by one
        for t in self.__triangles:

            # get triangles slope
            aspect = t.getAspect()
            
            # convert to color
            col = 255 - int(abs(aspect) * k)

            #create color
            color = QColor(col, col, col)
            qp.setBrush(color)
            
            #create colorful polygon
            pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            qp.drawPolygon(pol)

        
        # Set attributes
        qp.setPen(Qt.GlobalColor.green)

        #Draw triangles
        for edge in self.__dt:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))

        #Set attributes
        qp.setPen(Qt.GlobalColor.darkRed)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # Draw contour lines
        for edge in self.__contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))
        
        # Set attributes
        # qp.setPen(Qt.GlobalColor.blue)
        # qp.setBrush(Qt.GlobalColor.yellow)

        #End draw
        qp.end()

    def setDT(self, dt : list[Edge]):
        self.__dt = dt
    
    def setSlope(self, triangles: list[Triangle]):
        self.__triangles = triangles

    def setAspect(self, triangles: list[Triangle]):
        self.__triangles = triangles
    
    def getDT(self):
        return self.__dt

    def setContours(self, contours : list[Edge]):
        self.__contours = contours

    def getPoints(self):
        return self.__points
    
    def clearCanvas(self):
        """Clears canvas."""
        self.__points = []
        self.__dt = []
        self.__contours = []
        self.__triangles = []
        
        