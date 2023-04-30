from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import * 
from Edge import * 
from random import *
from triangle import * 
from math import *
from algorithms import *
from dialog import *

class Draw(QWidget):
    """
    A class to process and draw polygons on canvas.

    ---

    Attributes
    ----------
    __points (list[QPoint3DF]):
        List of input point cloud
    __dt (list[Edge]):
        List of created Delaunay triangulation
    __contours (list[Edge]):
        List of created contour lines
    __triangles (list[Triangle])
        List of created ractangles
    __switch_mode
        default value:-1

    __polyg_list (list):
        List of input polygons
    __er_list (list):
        List of created enclosing rectangles
    __ch_list (list):
        List of created convex hulls

    Methods
    -------
    mousePressEvent(self, e: QMouseEvent
        assigns coordinates after the mouse is pressed
    
    paintEvent(e:QPaintEvent):
        Handles drawing of objects on canvas

    clearCanvas():
        Clears canvas.

    resizePolygons(xmin, ymin, xmax, ymax):
        Resizes input data to fit to display.

    findBoundingPoints(p:QPointF, xmin, ymin, xmax, ymax):
        Finds minimum and maximum coordinates of bounding box around input polygons.

    loadData(data):
        Loads input JSON file.
    
    setDT(self, dt : list[Edge]):

    setSlope(self, triangles: list[Triangle]):

    setAspect(self, triangles: list[Triangle]):

    setContours(self, contours : list[Edge]):

    getPoints(self):
    
    getDT(self):

    getAspectColor(self, aspect):

    switchSlopeAspect(self, val):
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Building, convex hull and enclosing rectangle
        self.__points: list[QPoint3DF] = []
        self.__dt : list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []
        self.__switch_mode = -1
        self.__zmin = 0
        self.__zmax = 1650
        self.__dz = 10

    def setContourSettings(self):
        a = Algorithms()
        dialog = InputDialog()
        if dialog.exec():
            zmin, zmax, dz = dialog.getInputs()
            try:
                zmin = int(zmin)
                zmax = int(zmax)
                dz = int(dz)
                self.__zmin = zmin
                self.__zmax = zmax
                self.__dz = dz

            except ValueError:
                zmin, zmax, dz = a.setContourDefaultSettings()
                self.contourInvalidInput()
                self.__zmin = zmin
                self.__zmax = zmax
                self.__dz = dz
        else:
            return

    def getContourSettings(self):
        zmin, zmax, dz = self.setContourSettings()
        return zmin, zmax, dz

    def contourInvalidInput(self):
        """"""
        dlg = QMessageBox()
        dlg.setWindowTitle("Invalid Input")
        dlg.setText("The input for contour settings is invalid. Default settings have been applied. (min = 0, max = 1650, step = 10)")
        dlg.exec()

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
        """Handles drawing of objects"""

        #Create graphic object
        qp = QPainter(self)

        #Start draw
        qp.begin(self)

        k = (510/(pi/2))
 
        # process triangles one by one        
        for t in self.__triangles:
            # condition of settings for drawing DEM slope
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

            # condition of settings for drawing DEM aspect
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
        if (0 <= aspect <= pi/8) or (15*pi/8 <= aspect <= 2*pi) : #east - drawn correctly
            return QColor(0, 104, 192)
        
        elif (pi/8 < aspect < 3*pi/8) : #northeast
            return QColor(108, 0, 163)
                        
        elif (3*pi/8 <= aspect <= 5*pi/8) : #north = south
            return QColor(202, 0, 156)
        
        elif (5*pi/8 < aspect < 7*pi/8) : #northwest
            return QColor(255, 85, 104)
        
        elif (7*pi/8 <= aspect <= 9*pi/8) : #west - drawn correctly
            return QColor(255, 171, 71)
        
        elif (9*pi/8 < aspect < 11*pi/8) : #southwest
            return QColor(244, 250, 0)
        
        elif (11*pi/8 <= aspect <= 13*pi/8) : #south = north
            return QColor(154, 251, 12)
        
        elif (13*pi/8 < aspect < 15*pi/8) : #southeast
            return QColor(0, 173, 67)
        

    def setDT(self, dt : list[Edge]):
        self.__dt = dt
    
    def setSlope(self, triangles: list[Triangle]):
        self.__triangles = triangles

    def setAspect(self, triangles: list[Triangle]):
        self.__triangles = triangles
    
    def getDT(self):
        return self.__dt

    def getZMin(self):
        return self.__zmin

    def getZMax(self):
        return self.__zmax

    def getDZ(self):
        return self.__dz

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

        