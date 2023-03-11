from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import acos, pi, sqrt
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

    def windingNumberAlgorithm(q:QPoint, pol:QPolygonF):
        #initialization of variables: lenght of one polygon, sum of angles, threshold value
        n = len(pol)
        total_angle = 0
        EPS = 1.0e-10

        #iterating trough all vertices 
        for i in range(n):
            #point is vertex => located on edge
            if (q == pol[i]) or (q == pol[(i+1)%n]):
                return -1
            
           #counting determinant to analyze position of the point 
            ux = pol[(i+1)%n].x() - pol[i].x()
            uy = pol[(i+1)%n].y() - pol[i].y()

            vx = q.x() - pol[i].x()
            vy = q.y() - pol[i].y()
            det = (ux*vy)-(vx*uy)

            #counting vector u (point q - vertex i)
            ux = pol[i].x() - q.x()
            uy = pol[i].y() - q.y()

            #counting vecotr v (point q - vertex i+1)
            vx = pol[(i+1)%n].x() - q.x()
            vy = pol[(i+1)%n].y() - q.y()

            #counting angle of u and v
            dot_product = ux*vx + uy*vy
            mod_of_vector = abs(sqrt(ux**2 + uy**2)*sqrt(vx**2 + vy**2))
            angle = dot_product/mod_of_vector
            if angle > 1:
                angle = 1
            angle = abs(acos(angle))
            #determinant determines the addition/subtraction of angle to the totalAngle
            if det > 0:
                total_angle += angle
            elif det < 0:
                total_angle -= angle

            #edge detection trapping: point q on edge
            if det == 0 and abs(angle-pi) < EPS:
                return -1
            
        # the point q belongs to the polygon
        if abs(abs(total_angle) - 2*pi) < EPS:
            return 1
        return 0

    # Set Ray Crossing as default algorithm upon starting the app
    default_alg = rayCrossingAlgorithm