from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

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
        self.__polyg_list = []
        self.__element = []
        self.__barrier = []

    def paintEvent(self, e:QPaintEvent):
        """Handles drawing of objects on canvas."""
        qp = QPainter(self)
        # Start drawing
        qp.begin(self)

        #Set attributes of buildings
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)
        # Draw buildings
        for i in range(len(self.__polyg_list)):
            qp.drawPolygon(self.__polyg_list[i])

        # Set attributes of convex hulls
        qp.setPen(Qt.GlobalColor.blue)
        #Draw convex hulls
        for i in range(len(self.__ch_list)):
            qp.drawPolygon(self.__ch_list[i])

        # Set attributes of enclosing rectangles
        qp.setPen(Qt.GlobalColor.red)
        # Draw enclosing rectangles
        for i in range(len(self.__er_list)):
            qp.drawPolygon(self.__er_list[i])

        # Stop drawing
        qp.end()

    def clearCanvas(self):
        """Clears canvas."""
        self.__polyg_list = []
        self.__er_list = []
        self.__ch_list = []

    def clearERs(self):
        """Clears enclosing rectangles."""
        self.__er_list = []

    def clearCHs(self):
        """Clears convex hulls."""
        self.__ch_list = []

    def getPolygonList(self):
        """Returns list of input polygons."""
        return  self.__polyg_list

    def getConvexHulls(self, pols):
        """Returns list of convex hulls."""
        self.__ch_list = pols

    def setEnclosingRectangles(self, pols: list):
        """Sets enclosing rectangles."""
        self.__er_list = pols

    def setConvexHulls(self, pols: list):
        """Sets convex hulls."""
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