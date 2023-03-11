import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import json
from math import *
class Draw(QWidget):
    """
    A class to process and draw points and polygons on canvas.

    ---

    Attributes
    ----------
    __polyg_list (list):
        List of input polygons
    polyg_status (list):
        List used to store the results of point in polygon analysis
    __q (QPointF):
        Movable point used in point in polygon analysis

    Methods
    -------
    mousePressEvent(e:QMouseEvent):
        Handles the change in point position

    paintEvent(e:QPaintEvent):
        Handles drawing of objects on canvas

    getPoint():
        Returns point.

    getPolygonList():
        Returns list of input polygons.

    clearEvent():
        Clears canvas.

    findBoundingPoints(p:QPointF, xmin, ymin, xmax, ymax):
        Finds minimum and maximum coordinates of bounding box around input polygons.

    resizePolygons(xmin, ymin, xmax, ymax):
        Resizes input data to fit to display.

    detectKrovak(ymin, ymax, epsg):
        Changes coordinates if input has Krovak's projection

    loadData(data):
        Loads input JSON file.
    """

    def __init__(self, *argsd, **kwargs):
        """
        Constructs all the necessary attributes for Draw object.

            Parameters:
                __polyg_list (list): List of input polygons.
                polyg_status (list): List used to store the results of point in polygon analysis
                __q (QPointF): Movable point used in point in polygon analysis
        """
        super().__init__(*argsd, **kwargs)
        self.__polyg_list = []
        self.polyg_status = []
        self.__q = QPointF(-50, -50)

    def mousePressEvent(self, e:QMouseEvent):
        """Handles the change in point position."""
        # Get coordinates of left mouse button click
        x = e.position().x()
        y = e.position().y()
        self.__q.setX(x)
        self.__q.setY(y)
        # Change statuses of all polygons to 0 (not highlighted)
        self.polyg_status = [0] * len(self.__polyg_list)
        # Repaint screen
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        """Handles drawing of objects on canvas."""
        qp = QPainter(self)
        # Start drawing
        qp.begin(self)
        # Set stroke color
        qp.setPen(Qt.GlobalColor.blue)

        # Repaint polygons based on their status
        for i in range(len(self.__polyg_list)):
            # Paint cyan if point is on an edge or inside a polygon
            if self.polyg_status[i] == 1 or self.polyg_status[i] == -1:
                qp.setBrush(Qt.GlobalColor.cyan)

            # Paint yellow if point is outside a polygon or no analysis has been done
            else:
                qp.setBrush(Qt.GlobalColor.yellow)

            qp.drawPolygon(self.__polyg_list[i])

        # Set point attributes
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.red)
        d = 4
        qp.drawEllipse(int(self.__q.x() - d / 2), int(self.__q.y() - d / 2), d, d)

        # Stop drawing
        qp.end()

    def getPoint(self):
        """Returns point."""
        return  self.__q

    def getPolygonList(self):
        """Returns list of input polygons."""
        return  self.__polyg_list

    def clearEvent(self):
        """Clears canvas."""
        self.__polyg_list = []
        self.repaint()

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

    def detectKrovak(self, ymin, ymax, epsg):
        """Changes coordinates if input has Krovak's projection."""
        if epsg == "EPSG:5514":
            # Swap necessary coordinates
            krovak_ymin = ymax
            krovak_ymax = ymin
            return krovak_ymin, krovak_ymax
            # Return input coordinates if any other projection
        else:
            return ymin, ymax

    def loadData(self, data):
        """Loads input JSON file."""
        # Initialize min and max coordinates to compute bounding box
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        # Get coordinate system of input
        epsg = data["crs"]["properties"]["name"]

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
                        xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
                    # Append created polygon to polygon list, set its status to 0 (not highlighted)
                    self.__polyg_list.append(pol)
                    self.polyg_status.append(0)
            # Swap y coordinates if input has Krovak's projection
            ymin, ymax = self.detectKrovak(ymin, ymax, epsg)
            # Resize polygons to fit to display
            self.resizePolygons(xmin, ymin, xmax, ymax)
            self.repaint()
        # Alert if no coordinates have been found
        else:
            dlg = QMessageBox()
            dlg.setWindowTitle("Error Message")
            dlg.setText("Invalid JSON file")
            dlg.exec()
            return None
