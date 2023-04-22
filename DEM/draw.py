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
        self.__switch_mode = -1

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

        k = (510/(pi/2))

        
        # process triangles one by one
        """for t in self.__triangles:

            # get triangles slope
            slope = t.getSlope()
            
            # convert to color
            col = 255 - int(abs(slope) * k)

            #create color
            color = QColor(col, col, col)
            qp.setBrush(color)
            
            #create colorful polygon
            pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            qp.drawPolygon(pol)"""
        
        for t in self.__triangles:
            if self.__switch_mode == 0:
                # get triangles slope
                slope = t.getSlope()


                # convert to color
                col = 255 - int(slope * k)

                #create color
                color = QColor(col, col, col)
                qp.setBrush(color)

                #create colorful polygon
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

                qp.drawPolygon(pol)

            if self.__switch_mode == 1:
                aspect = t.getAspect()
                color = self.getAspectColor(aspect)
                qp.setBrush(color)
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
        
        #Set attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        #Draw points
        r = 10 # jako 10 pixelů
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2*r, 2*r)# x- r a y - r
            qp.drawText(point,str(int(point.getZ())))
        
        
        # Set attributes
        # qp.setPen(Qt.GlobalColor.blue)
        # qp.setBrush(Qt.GlobalColor.yellow)

        #End draw
        qp.end()
    
    def getAspectColor(self, aspect):
        """ gets color for aspect """
        if (0 <= aspect <= pi/8) or (15*pi/8 <= aspect <= 2*pi): #east
            return QColor(0, 104, 192)
        
        if pi/8 < aspect < 3*pi/8 : #northeast
            return QColor(0, 173, 67)
        
        if 3*pi/8 <= aspect <= 5*pi/8 : #north
            return QColor(154, 251, 12)
        
        if 5*pi/8 < aspect < 7*pi/8 : #northwest
            return QColor(244, 250, 0)
        
        if 7*pi/8 <= aspect <= 9*pi/8 : #west
            return QColor(255, 171, 71)
        
        if 9*pi/8 < aspect < 11*pi/8 : #southwest
            return QColor(255, 85, 104)
        
        if 11*pi/8 <= aspect <= 13*pi/8 : #south
            return QColor(202, 0, 156)
        
        if 13*pi/8 < aspect < 15*pi/8 : #southeast
            return QColor(108, 0, 163)

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
    
    def switchSlopeAspect(self, val):
        # Move point or add vertex
        self.__switch_mode = val
    
    def clearCanvas(self):
        """Clears canvas."""
        self.__points = []
        self.__dt = []
        self.__contours = []
        self.__triangles = []

        