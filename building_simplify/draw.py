from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__polyg_list = []
        self.__er_list = []
        self.__ch_list = []

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
        for i in range(len(self.__polyg_list)):
            qp.drawPolygon(self.__polyg_list[i])

        #Set attributes convex hull
        qp.setPen(Qt.GlobalColor.blue)
        #qp.setBrush(Qt.GlobalColor.yellow)

        #Draw ch
        for i in range(len(self.__ch_list)):
            qp.drawPolygon(self.__ch_list[i])
        #End draw

        #Set attributes enclosing rectangle
        qp.setPen(Qt.GlobalColor.red)
        #qp.setBrush(Qt.GlobalColor.yellow)

        # draw enclosing rectangle
        for i in range(len(self.__er_list)):
            qp.drawPolygon(self.__er_list[i])
        #End draw
        qp.end()

    def clearCanvas(self):
        self.__polyg_list = []
        self.__er_list = []
        self.__ch_list = []

    def getPolygonList(self):
        """Returns list of input polygons."""
        return  self.__polyg_list

    def getConvexHulls(self, pols):
        self.__ch_list = pols
    def setEnclosingRectangles(self, pols: list):
        self.__er_list = pols

    def setConvexHulls(self, pols: list):
        self.__ch_list = pols

    def resizePolygons(self, xmin, ymin, xmax, ymax):
        """Resizes input data to fit to display."""
        canvas_height = self.frameGeometry().height()
        canvas_width = self.frameGeometry().width()
        # Iterate over each coordinate for repositioning
        for polygon in self.__polyg_list:
            for point in polygon:
                new_x = int((point.x() - xmin) * canvas_width/(xmax - xmin))
                new_y = int((point.y() - ymin) * canvas_height/(ymax - ymin))
                # Reposition coordinates accordingly
                point.setX(new_x)
                point.setY(new_y)

    def findBoundingPoints(self, p:QPointF, xmin, ymin, xmax, ymax):
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

    def loadData(self, data):
        """Loads input JSON or GeoJSON file."""
        # Initialize min and max coordinates to compute bounding box
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf

        # Check first feature for key coordinates
        if "coordinates" in data["features"][0]["geometry"]:
            # Iterate over each feature (polygon)
            for feature in data["features"]:
                # Prepare empty QPolygonF object
                pol = QPolygonF()
                if isinstance(feature["geometry"]["coordinates"], list):
                    # Convert each coordinate to QPointF object
                    for coords in feature["geometry"]["coordinates"][0]:
                        p = QPointF(int(coords[0]), int(coords[1]))
                        # Append to polygon
                        pol.append(p)
                        # Process min and max coordinates to find bounding box
                        xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
                    # Append created polygon to polygon list, set its status to 0 (not highlighted)
                    self.__polyg_list.append(pol)
            # Swap y coordinates according to Krovak's projection
            ymin, ymax = ymax, ymin
            # Resize polygons to fit to display
            self.resizePolygons(xmin, ymin, xmax, ymax)
            self.repaint()
        # Alert if no coordinates have been found
        else:
            return False