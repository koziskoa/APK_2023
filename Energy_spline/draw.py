from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from settings import *

class Draw(QWidget):
    """
    A class to process and draw polygons on canvas.

    ---

    Attributes
    ----------
    __polyg_list (list):
        List of input polygons
    __er_list (list):
        List of created enclosing rectangles
    __ch_list (list):
        List of created convex hulls

    Methods
    -------
    paintEvent(e:QPaintEvent):
        Handles drawing of objects on canvas

    clearCanvas():
        Clears canvas.

    clearERs():
        Clears enclosing rectangles.

    clearCHs():
        Clears convex hulls.

    getPolygonList():
        Returns list of input polygons.

    getEnclosingRectangles():
        Returns list of enclosing rectangles.

    getConvexHulls():
        Returns list of convex hulls.

    setEnclosingRectangles():
        Sets enclosing rectangles.

    setConvexHulls():
        Sets convex hulls.

    resizePolygons(xmin, ymin, xmax, ymax):
        Resizes input data to fit to display.

    findBoundingPoints(p:QPointF, xmin, ymin, xmax, ymax):
        Finds minimum and maximum coordinates of bounding box around input polygons.

    loadData(data):
        Loads input JSON file.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructs all the necessary attributes for Draw object.

            Parameters:
                __polyg_list (list): List of input polygons.
                __er_list (list): List of created enclosing rectangles.
                __ch_list (list): List of created convex hulls.
        """
        super().__init__(*args, **kwargs)
        self.__add_L = True
        self.__L = QPolygonF()
        self.__B = QPolygonF()
        self.__LD = QPolygonF()
        self.__add_vertex = True
        self.xmin = inf
        self.xmax = -inf
        self.ymin = inf
        self.ymax = -inf
        self.L_is_normalized = True
        self.B_is_normalized = True

    def paintEvent(self, e:QPaintEvent):
        #Draw polygon

        #Create graphic object
        qp = QPainter(self)

        #Start draw
        qp.begin(self)

        #Set attributes
        qp.setPen(Qt.GlobalColor.black)

        #Draw L
        qp.drawPolyline(self.__L)

        # Set attributes
        qp.setPen(Qt.GlobalColor.blue)

        # Draw B
        qp.drawPolyline(self.__B)

        # Set attributes
        qp.setPen(Qt.GlobalColor.red)

        # Draw LD
        qp.drawPolyline(self.__LD)

        #End draw
        qp.end()

    def switchSource(self):
        #Move point or add vertex
        self.__add_vertex = not(self.__add_vertex)

    def getL(self):
        return self.__L

    def getB(self):
        return self.__B

    def setLD(self, LD_):
        self.__LD = LD_

    def setSource(self, status):
        self.__add_L = status

    def clearAll(self):
        self.__L.clear()
        self.__B.clear()
        self.__LD.clear()
        self.xmin = inf
        self.xmax = -inf
        self.ymin = inf
        self.ymax = -inf

    def loadData(self, data):
        """Loads input CSV file."""
        # Initialize min and max coordinates to compute bounding box
        """xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf"""
        if self.__add_L:
            for row in data:
                # Convert rows
                xy = [float(i) for i in row]
                x, y = xy
                p = QPointF(x, y)
                self.findBoundingPoints(p)
                self.__L.append(p)
            self.L_is_normalized = False
        else:
            for row in data:
                # Convert rows
                xy = [float(i) for i in row]
                x, y = xy
                p = QPointF(x, y)
                self.findBoundingPoints(p)
                self.__B.append(p)
            self.B_is_normalized = False
        # Adjust canvas according to Krovak
        self.resizeContent()
        self.repaint()

    def findBoundingPoints(self, p: QPointF):
        """Returns minimum and maximum coordinates of bounding box around input points."""
        if p.x() < self.xmin:
            self.xmin = p.x()
        if p.y() < self.ymin:
            self.ymin = p.y()
        if p.x() > self.xmax:
            self.xmax = p.x()
        if p.y() > self.ymax:
            self.ymax = p.y()

    def resizeContent(self):
        """Resizes input data to fit to display."""
        c = 100
        canvas_height = self.frameGeometry().height() - c
        canvas_width = self.frameGeometry().width() - c
        xmin = self.xmax
        xmax = self.xmin
        # Iterate over each coordinate for repositioning
        if not self.L_is_normalized:
            if (self.ymax-self.ymin)/canvas_height > (self.xmax-self.xmin)/canvas_width:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + c
                    new_y = int((point.y() - self.ymin) * canvas_height / (self.ymax - self.ymin)) + c/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.L_is_normalized = True
            else:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_width / (xmax - xmin)) + c
                    new_y = int((point.y() - self.ymin) * canvas_width / (self.ymax - self.ymin)) + c/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.L_is_normalized = True
        if not self.B_is_normalized:
            if (self.ymax - self.ymin) / canvas_height > (self.xmax - self.xmin) / canvas_width:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + c
                    new_y = int((point.y() - self.ymin) * canvas_height / (self.ymax - self.ymin)) + c/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.B_is_normalized = True
            else:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_width / (xmax - xmin)) + c
                    new_y = int((point.y() - self.ymin) * canvas_width / (self.ymax - self.ymin)) + c/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.B_is_normalized = True
