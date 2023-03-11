from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class Algorithms:
    """
    A class to store algorithms for point in polygon analysis.

    Methods
    -------
    rayCrossingAlgorithm(q, pol):
        Determines the point location by using Ray Crossing Algorithm.

    windingNumberAlgorithm(q, pol):
        Determines the point location by using Winding Number Algorithm.
    """
    def __init__(self):
        pass

    def rayCrossingAlgorithm(q:QPoint, pol:QPolygonF):
        """
        Ray Crossing Algorithm.

            Parameters:
                q (QPoint): Point represented by x, y coordinates.
                pol(QPolygonF): Polygon formed by vertices with x, y coordinates.

            Returns:
                -1 (int): Point is located on the edge of the polygon.
                1 (int): Point is located inside the polygon.
                0 (int): Point is located outside the polygon.
        """
        # Initialize the number of left and right intersections and the number of vertices in the polygon
        kr = 0
        kl = 0
        n = len(pol)

        # Process all vertices
        for i in range (n):
            # Reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()

            # Check if point is located on a vertex
            if xir == 0 and yir == 0:
                return -1

            # Reduce coordinates of the next vertex
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()

            # Check for horizontal edge
            if (yi1r - yir) == 0:
                continue

            #Compute the intersection of ray and edge
            xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)

            # Process lower segment
            if (yi1r < 0) != (yir < 0):
                # Increment the number of left intersections if xm is on the left
                if xm < 0:
                    kl += 1

            # Process upper segment
            if (yi1r > 0) != (yir > 0):
                # Increment the number of right intersections if xm is on the right
                if xm > 0:
                    kr += 1

        # Point is on an edge if the number of left and right intersections is diferent
        if (kl % 2) != (kr % 2):
            return -1

        # Point is inside the polygon if there's odd number of intersections
        elif (kr % 2 == 1):
            return 1

        # Point is outside the polygon if otherwise
        else:
            return 0

    # Set Ray Crossing as default algorithm upon starting the app
    default_alg = rayCrossingAlgorithm