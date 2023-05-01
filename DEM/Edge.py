from QPoint3DF import *
from math import *

class Edge:
    """
    A class used to represent edges of DT triangles.
    ...

    Attributes
    ----------
    __start : QPoint3DF
        Start point of edge.

    __end : QPoint3DF
        End point of edge.

    Methods
    ----------
    getStart():
       Returns start point.

    getEnd():
       Returns end point.

    switchOrientation():
       Creates new edge with an opposite orientation.

    getEdgeCenterX():
       Returns center X coordinate of an edge.

    getEdgeCenterY():
       Returns center Y coordinate of an edge.

    __eq__():
       Defines eq operation for an Edge object.
    """
    def __init__(self, start: QPoint3DF, end: QPoint3DF):
        """Constructs all the necessary attributes for Edge object."""
        self.__start = start
        self.__end = end

    def getStart(self):
       """Returns start point."""
       return self.__start
    
    def getEnd(self):
       """Returns end point."""
       return self.__end
    
    def switchOrientation(self):
       """Creates new edge with an opposite orientation."""
       return Edge(self.__end, self.__start)

    def getEdgeCenterX(self):
       """Returns center X coordinate of an edge."""
       return int((self.__start.x() + self.__end.x())/2)

    def getEdgeCenterY(self):
       """Returns center Y coordinate of an edge."""
       return int((self.__start.y() + self.__end.y())/2)

    def __eq__(self, other) -> bool:
       """Defines eq operation for an Edge object."""
       return (self.__start == other.__start) and (self.__end == other.__end)