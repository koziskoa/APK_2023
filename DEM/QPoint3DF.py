from PyQt6.QtCore import *
from PyQt6.QtGui import *

class QPoint3DF(QPointF):
    """
    A class used to represent 3D point.
    ...

    Attributes
    ----------
    x : float
        X coordinate of point.
    y : float
        Y coordinate of point.
    __z : float
        Z coordinate of point.

    Methods
    ----------
    getZ():
       Returns Z coordinate of QPoint3DF object..
    """
    def __init__(self, x:float, y:float, z: float):
        """Initialize x, y from parent QPointF class for QPoint3DF object."""
        super().__init__(x,y)
        self.__z = z

    def getZ(self):
        """Returns Z coordinate of QPoint3DF object."""
        return self.__z