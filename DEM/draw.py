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
    A class to process and draw DEM features on canvas.
    ...

    Attributes
    ----------
    __points : QPoint3DF
        List of input point cloud.
    __dt : list
        List of created Delaunay triangulation.
    __contours : list
        List of created contour lines.
    __index_contours : list
        List of created index contour lines and their orientations.
    __triangles : list
        List of created triangles.
    __switch_mode : int
        Switch to determine features to draw on canvas.
    __draw_labels : bool
        Switch to show/hide contour labels.
    __zmin : int
        Minimum Z coordinate to draw contours from.
    __zmax : int
        Maximum Z coordinate to draw contours from.
    __dz : int
        Step of Z coordinates to draw contours.

    Methods
    -------
    setContourSettings():
        Sets input contour parameters.
    getContourSettings(self):
        Returns contour settings.
    contourInvalidInput(self):
        Opens a popup to inform of invalid input.
    paintEvent(e:QPaintEvent):
        Handles drawing of objects.
    getAspectColor(aspect):
        Returns aspect color. All colors are taken from ESRI aspect color pallette.
    setDT(dt : list[Edge]):
        Sets list of DT edges.
    setSlopeAspect(triangles: list[Triangle]):
        Sets list of triangles with attributes.
    getDT():
        Returns DT edges.
    getZMin():
        Returns minimum Z coordinate.
    getZMax():
        Returns maximum Z coordinate.
    getDZ():
        Returns step of contours.
    setContours(contours : list[Edge], index_contours : list[Edge]):
        Sets contours and index contours.
    getPoints():
        Returns point cloud.
    switchSlopeAspect(val):
        Switches between drawing slope or aspect.
    clearCanvas():
        Clears canvas.
    clearContourLines():
        Clears contour lines.
    clearSlopeAspect():
        Clears slope and aspect.
    showContourLinesLabels():
        Shows/hides contour labels.
    loadData(data):
        Loads input CSV file.
    findBoundingPoints(p:QPoint3DF, xmin, ymin, xmax, ymax):
        Returns minimum and maximum coordinates of bounding box around input points.
    resizeContent(xmin, ymin, xmax, ymax):
        Resizes input data to fit to display.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Constructs all the necessary attributes for Draw object."""
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
        """Sets input contour parameters."""
        a = Algorithms()
        # Execute contour dialog window
        dialog = InputDialog()
        # On signal accepted
        if dialog.exec():
            # Get input values
            zmin, zmax, dz = dialog.getInputs()
            # Convert input to int and set values
            try:
                zmin = int(zmin)
                zmax = int(zmax)
                dz = int(dz)
                self.__zmin = zmin
                self.__zmax = zmax
                self.__dz = dz
            # Input is string or invalid
            except ValueError:
                # Set default contour settings and alert the user
                zmin, zmax, dz = a.setContourDefaultSettings()
                self.contourInvalidInput()
                self.__zmin = zmin
                self.__zmax = zmax
                self.__dz = dz
        else:
            return

    def getContourSettings(self):
        """Returns contour settings."""
        zmin, zmax, dz = self.setContourSettings()
        return zmin, zmax, dz

    def contourInvalidInput(self):
        """Opens a popup to inform of invalid input."""
        dlg = QMessageBox()
        dlg.setWindowTitle("Invalid Input")
        dlg.setText("The input for contour settings is invalid. Default settings have been applied. (min = 0, max = 1650, step = 10)")
        dlg.exec()

    def paintEvent(self, e:QPaintEvent):
        """Handles drawing of objects."""
        # Create graphic objects
        qp = QPainter(self)
        pen = QPen()
        font = QFont('Arial', 7)
        font.setBold(True)
        qp.setFont(font)
        # Start draw
        qp.begin(self)
        # Process all triangles
        for t in self.__triangles:
            # Draw slope triangles
            if self.__switch_mode == 0:
                # Get triangle slope
                slope = t.getSlope()
                # Convert to RGB color
                col = int(slope*(510/pi))
                # Create color object
                color = QColor(col, col, col)
                qp.setBrush(color)
                # Create colored polygon
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])
                qp.drawPolygon(pol)
            # Draw aspect triangles
            if self.__switch_mode == 1:
                # Get triangle aspect
                aspect = t.getAspect()
                # Create colored polygon
                color = self.getAspectColor(aspect)
                qp.setBrush(color)
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])
                qp.drawPolygon(pol)
        # Set attributes for drawing edges
        pen.setColor(Qt.GlobalColor.green)
        qp.setPen(pen)
        for edge in self.__dt:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))
        # Set attributes for drawing normal contours
        pen.setWidth(1)
        pen.setColor(Qt.GlobalColor.darkRed)
        qp.setPen(pen)
        # Draw contour lines
        for edge in self.__contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))
        # Set attributes for drawing index contours
        pen.setWidth(2)
        pen.setColor(Qt.GlobalColor.darkRed)
        qp.setPen(pen)
        # Access contour segments
        index_contours = [contour[0] for contour in self.__index_contours]
        for edge in index_contours:
            qp.drawLine(int(edge.getStart().x()), int(edge.getStart().y()), int(edge.getEnd().x()), int(edge.getEnd().y()))
        # Set attributes for drawing vertices
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)
        # Draw vertices
        r = 3
        for point in self.__points:
            qp.drawEllipse(int(point.x()) - r, int(point.y()) - r, 2 * r, 2 * r)
        # If labels are switched on, draw them
        if self.__draw_labels:
            # Draw label on every 20th segment (customizable)
            index_contours_labels = self.__index_contours[::20]
            for edge in index_contours_labels:
                # Convert angle to degrees
                angle = edge[1] * 180/pi
                # Translate coordinate system
                qp.translate(edge[0].getEdgeCenterX(), edge[0].getEdgeCenterY())
                # Rotate painter
                qp.rotate(angle+180)
                # Draw bounding polygon
                qp.setBrush(Qt.GlobalColor.white)
                pen.setColor(Qt.GlobalColor.white)
                qp.setPen(pen)
                qp.drawRect(QRectF(QPointF(-5,-5), QSizeF(20,12)))
                # Draw label
                pen.setColor(Qt.GlobalColor.darkRed)
                qp.setPen(pen)
                qp.drawText(-5, 5, str(edge[0].getStart().getZ()))
                # Rotate painter back, return coordinate system to previous state
                qp.rotate(-(angle+180))
                qp.translate(-edge[0].getEdgeCenterX(), -edge[0].getEdgeCenterY())
        #End draw
        qp.end()
    
    def getAspectColor(self, aspect):
        """Returns aspect color. All colors are taken from ESRI aspect color pallette."""
        # East
        if (0 <= aspect <= pi/8) or (15*pi/8 <= aspect <= 2*pi):
            return QColor(0, 104, 192)
        # Northeast
        elif (pi/8 < aspect < 3*pi/8):
            return QColor(108, 0, 163)
        # South
        elif (3*pi/8 <= aspect <= 5*pi/8):
            return QColor(202, 0, 156)
        # Northwest
        elif (5*pi/8 < aspect < 7*pi/8):
            return QColor(255, 85, 104)
        # West
        elif (7*pi/8 <= aspect <= 9*pi/8):
            return QColor(255, 171, 71)
        # Southwest
        elif (9*pi/8 < aspect < 11*pi/8):
            return QColor(244, 250, 0)
        # North
        elif (11*pi/8 <= aspect <= 13*pi/8):
            return QColor(154, 251, 12)
        # Southeast
        elif (13*pi/8 < aspect < 15*pi/8):
            return QColor(0, 173, 67)

    def setDT(self, dt : list[Edge]):
        """Sets list of DT edges."""
        self.__dt = dt
    
    def setSlopeAspect(self, triangles: list[Triangle]):
        """Sets list of triangles with attributes."""
        self.__triangles = triangles
    
    def getDT(self):
        """Returns DT edges."""
        return self.__dt

    def getZMin(self):
        """Returns minimum Z coordinate."""
        return self.__zmin

    def getZMax(self):
        """Returns maximum Z coordinate."""
        return self.__zmax

    def getDZ(self):
        """Returns step of contours."""
        return self.__dz

    def setContours(self, contours : list[Edge], index_contours : list[Edge]):
        """Sets contours and index contours."""
        self.__contours = contours
        self.__index_contours = index_contours

    def getPoints(self):
        """Returns point cloud."""
        return self.__points
    
    def switchSlopeAspect(self, val):
        """
        Switches between drawing slope or aspect.
        -1 : draw nothing
        0 : draw slope
        1 : draw aspect
        """
        self.__switch_mode = val
    
    def clearCanvas(self):
        """Clears canvas."""
        self.__points = []
        self.__dt = []
        self.__contours = []
        self.__index_contours = []
        self.__triangles = []

    def clearContourLines(self):
        """Clears contour lines."""
        self.__contours = []
        self.__index_contours = []

    def clearSlopeAspect(self):
        """Clears slope and aspect."""
        self.__switch_mode = -1

    def showContourLinesLabels(self):
        """Shows/hides contour labels."""
        self.__draw_labels = not self.__draw_labels

    def loadData(self, data):
        """Loads input CSV file."""
        # Initialize min and max coordinates to compute bounding box
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        for row in data:
            # Convert rows
            xyz = [float(i) for i in row]
            x, y, z = xyz
            p = QPoint3DF(x,y,z)
            xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
            self.__points.append(p)
        # Adjust canvas according to Krovak
        xmin, xmax = xmax, xmin
        self.resizeContent(xmin, ymin, xmax, ymax)
        self.repaint()

    def findBoundingPoints(self, p:QPoint3DF, xmin, ymin, xmax, ymax):
        """Returns minimum and maximum coordinates of bounding box around input points."""
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