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
import csv

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
        self.__index_contours = []
        self.__triangles: list[Triangle] = []
        self.__switch_mode = -1
        self.__draw_labels = True
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
        pen = QPen()
        font = QFont('Arial', 7)
        font.setBold(True)
        qp.setFont(font)
        #Start draw
        qp.begin(self)
        #k = (510/(2*pi))
 
        # process triangles one by one        
        for t in self.__triangles:
            # condition of settings for drawing DEM slope
            if self.__switch_mode == 0:
                # get triangles slope
                slope = t.getSlope()

                # convert to color
                col = int(slope*(510/pi))
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
        pen.setColor(Qt.GlobalColor.green)
        qp.setPen(pen)

        #Draw triangles
        for edge in self.__dt:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))

        #Set attributes
        pen.setWidth(1)
        pen.setColor(Qt.GlobalColor.darkRed)
        qp.setPen(pen)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # Draw contour lines
        for edge in self.__contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))

        pen.setWidth(2)
        pen.setColor(Qt.GlobalColor.darkRed)
        qp.setPen(pen)

        index_contours = [contour[0] for contour in self.__index_contours]
        for edge in index_contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))

        # Set attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # Draw points
        r = 3  # jako 10 pixelů
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2 * r, 2 * r)  # x- r a y - r
            #qp.drawText(int(point.x())-5,int(point.y())+5, str(int(point.getZ())))

        if self.__draw_labels:
            index_contours_labels = self.__index_contours[::20]
            for edge in index_contours_labels:
                angle = edge[1] * 180/pi
                qp.translate(edge[0].getEdgeCenterX(), edge[0].getEdgeCenterY())
                qp.rotate(angle+180)
                qp.setBrush(Qt.GlobalColor.white)
                pen.setColor(Qt.GlobalColor.white)
                qp.setPen(pen)
                qp.drawRect(QRectF(QPointF(-5,-5), QSizeF(20,12)))
                pen.setColor(Qt.GlobalColor.darkRed)
                qp.setPen(pen)
                qp.drawText(-5, 5, str(edge[0].getStart().getZ()))
                qp.rotate(-(angle+180))
                qp.translate(-edge[0].getEdgeCenterX(), -edge[0].getEdgeCenterY())

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

    def setContours(self, contours : list[Edge], index_contours : list[Edge]):
        self.__contours = contours
        self.__index_contours = index_contours

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
        self.__index_contours = []
        self.__triangles = []

    def clearContourLines(self):
        self.__contours = []
        self.__index_contours = []

    def clearSlopeAspect(self):
        self.__switch_mode = -1

    def showContourLinesLabels(self):
        self.__draw_labels = not self.__draw_labels

    def loadData(self, data):
        """Loads input JSON or GeoJSON file."""
        # Initialize min and max coordinates to compute bounding box
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf

        for row in data:
            xyz = [float(i) for i in row]
            x, y, z = xyz
            p = QPoint3DF(x,y,z)
            xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
            self.__points.append(p)
        xmin, xmax = xmax, xmin
        self.resizeContent(xmin, ymin, xmax, ymax)
        self.repaint()
        """
        # Check first feature for key coordinates
        if "coordinates" in data["features"][0]["geometry"]:
            # Iterate over each feature (polygon)
            for feature in data["features"]:
                # Prepare empty QPolygonF object
                pol = QPolygonF()
                if isinstance(feature["geometry"]["coordinates"], list):
                    # Convert each coordinate to QPointF object
                    for coords in feature["geometry"]["coordinates"][0]:
                        p=QPointF(int(coords[0]),int(coords[1]))
                        # Append to polygon
                        pol.append(p)
                        # Process min and max coordinates to find bounding box
                        
                    # Append created polygon to polygon list, set its status to 0 (not highlighted)
                    self.__polyg_list.append(pol)
                    self.polyg_status.append(0)
            # Swap y coordinates according to Krovak's projection
            ymin, ymax = ymax, ymin
            # Resize polygons to fit to display
            self.resizePolygons(xmin, ymin, xmax, ymax)
            self.repaint()
        # Alert if no coordinates have been found
        else:
            return False
        """
    def findBoundingPoints(self, p:QPoint3DF, xmin, ymin, xmax, ymax):
        """Returns minimum and maximum coordinates of bounding box around input polygons."""
        if p.x() < xmin:
            xmin = p.x()
        if p.y() < ymin:
            ymin = p.y()
        if p.x() > xmax:
            xmax = p.x()
        if p.y() > ymax:
            ymax = p.y()
        return xmin, ymin, xmax, ymax

    def resizeContent(self, xmin, ymin, xmax, ymax):
        """Resizes input data to fit to display."""
        canvas_height = self.frameGeometry().height()
        canvas_width = self.frameGeometry().width()
        # Iterate over each coordinate for repositioning
        for point in self.__points:
            new_x = int((point.x() - xmin) * canvas_width/(xmax - xmin))
            new_y = int((point.y() - ymin) * canvas_height/(ymax - ymin))
            # Reposition coordinates accordingly
            point.setX(new_x)
            point.setY(new_y)