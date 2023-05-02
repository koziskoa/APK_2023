from QPoint3DF import *

class Triangle:
    """
    A class used to represent triangles created by Delaunay triangulation.
    ...

    Attributes
    ----------
    __p1 : QPoint3DF
        First point of triangle.

    __p2 : QPoint3DF
        Second point of triangle.

    __p3 : QPoint3DF
        Third point of triangle.

    __slope : float
        Slope of triangle.

    __aspect : QPoint3DF
        Aspect of triangle.

    Methods
    ----------
    getP1():
       Returns first point of triangle.

    getP2():
       Returns second point of triangle.

    getP3():
       Returns third point of triangle.

    getSlope():
       Returns slope of triangle.

    getAspect():
       Returns aspect of triangle.
    """
    def __init__(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF, slope: float, aspect:float):
        """Constructs all the necessary attributes for Triangle object."""
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        self.__slope = slope
        self.__aspect = aspect

    def getP1(self):
        """Returns first point of triangle."""
        return self.__p1

    def getP2(self):
        """Returns second point of triangle."""
        return self.__p2

    def getP3(self):
        """Returns third point of triangle."""
        return self.__p3

    def getSlope(self):
        """Returns slope of triangle."""
        return self.__slope

    def getAspect(self):
        """Returns aspect of triangle."""
        return self.__aspect