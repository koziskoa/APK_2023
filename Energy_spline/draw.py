from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from settings import *

class Draw(QWidget):
    """
    A class to process and draw lines on canvas.

    ---

    Attributes
    ----------
    __add_L (bool):
        Input switch for line/barrier
    __L (QPolygonF):
        List of created enclosing rectangles
    __B (QPolygonF):
        List of created convex hulls
    __LD (QPolygonF):
        List of created convex hulls
    xmin, ymin, xmax, ymax (float):
        Bounding points for objects on canvas
    L_is_normalized (bool):
        Flag for line adjustment
    B_is_normalized (bool):
        Flag for barrier adjustment
    """

    def __init__(self, *args, **kwargs):
        """Constructs all the necessary attributes for Draw object."""
        super().__init__(*args, **kwargs)
        self.__add_L = True
        self.__L = QPolygonF()
        self.__B = QPolygonF()
        self.__LD = QPolygonF()
        self.xmin = inf
        self.xmax = -inf
        self.ymin = inf
        self.ymax = -inf
        self.L_is_normalized = True
        self.B_is_normalized = True

    def paintEvent(self, e:QPaintEvent):
        """Handles drawing of objects on canvas."""
        #Create graphic object
        qp = QPainter(self)
        #Start draw
        qp.begin(self)
        #Set attributes for line
        qp.setPen(Qt.GlobalColor.black)
        #Draw line
        qp.drawPolyline(self.__L)
        # Set attributes for barrier
        qp.setPen(Qt.GlobalColor.blue)
        # Draw barrier
        qp.drawPolyline(self.__B)
        # Set attributes for displaced line
        qp.setPen(Qt.GlobalColor.red)
        # Draw displaced line
        qp.drawPolyline(self.__LD)
        #End draw
        qp.end()

    def getL(self):
        """Returns line."""
        return self.__L

    def getB(self):
        """Returns barrier."""
        return self.__B

    def setLD(self, LD_):
        """Sets displaced line."""
        self.__LD = LD_

    def setSource(self, status):
        """Switches between inputting line or barrier."""
        self.__add_L = status

    def clearAll(self):
        """Clears canvas."""
        self.__L.clear()
        self.__B.clear()
        self.__LD.clear()
        self.xmin = inf
        self.xmax = -inf
        self.ymin = inf
        self.ymax = -inf

    def loadData(self, data):
        """Loads input CSV file."""
        # Load line
        if self.__add_L:
            for row in data:
                # Convert rows
                xy = [float(i) for i in row]
                x, y = xy
                p = QPointF(x, y)
                self.findBoundingPoints(p)
                self.__L.append(p)
            # Set flag resize
            self.L_is_normalized = False
        # Load barrier
        else:
            for row in data:
                # Convert rows
                xy = [float(i) for i in row]
                x, y = xy
                p = QPointF(x, y)
                self.findBoundingPoints(p)
                self.__B.append(p)
            # Set flag to resize
            self.B_is_normalized = False
        # Adjust canvas according to Krovak
        self.resizeContent()
        self.repaint()

    def findBoundingPoints(self, p: QPointF):
        """Adjusts minimum and maximum coordinates of bounding box around input lines."""
        if p.x() < self.xmin:
            self.xmin = p.x()
        if p.y() < self.ymin:
            self.ymin = p.y()
        if p.x() > self.xmax:
            self.xmax = p.x()
        if p.y() > self.ymax:
            self.ymax = p.y()

    def resizeContent(self):
        """Resizes and centers input data to fit to display."""
        # Constant for window padding
        C = 100
        canvas_height = self.frameGeometry().height() - C
        canvas_width = self.frameGeometry().width() - C
        # Swap xmin and xmax according to Krovak
        xmin = self.xmax
        xmax = self.xmin
        # Iterate over each coordinate for repositioning if it hasn't been done before
        # For line:
        if not self.L_is_normalized:
            if (self.ymax-self.ymin)/canvas_height > (self.xmax-self.xmin)/canvas_width:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + C
                    new_y = int((point.y() - self.ymin) * canvas_height / (self.ymax - self.ymin)) + C/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.L_is_normalized = True
            else:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_width / (xmax - xmin)) + C
                    new_y = int((point.y() - self.ymin) * canvas_width / (self.ymax - self.ymin)) + C/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.L_is_normalized = True
        # For barrier:
        if not self.B_is_normalized:
            if (self.ymax - self.ymin) / canvas_height > (self.xmax - self.xmin) / canvas_width:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + C
                    new_y = int((point.y() - self.ymin) * canvas_height / (self.ymax - self.ymin)) + C/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.B_is_normalized = True
            else:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_width / (xmax - xmin)) + C
                    new_y = int((point.y() - self.ymin) * canvas_width / (self.ymax - self.ymin)) + C/2
                    # Reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.B_is_normalized = True