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

    computeVector(p1, p2):
        Returns vector between two points.
    
    computeAngle(ax,ay,bx,by):
        Returns angle of two vecotrs.
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
            xir, yir = Algorithms.computeVector(pol[i], q)

            # Check if point is located on a vertex
            if xir == 0 and yir == 0:
                return -1

            # Reduce coordinates of the next vertex
            xi1r, yi1r = Algorithms.computeVector(pol[(i+1)%n], q)

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
        """
        Winding Number Algorithm.

            Parameters:
                q (QPoint): Point represented by x, y coordinates.
                pol(QPolygonF): Polygon formed by vertices with x, y coordinates.
            Returns:
               -1 (int): Point is located on the edge of the polygon.
                1 (int): Point is located inside the polygon.
                0 (int): Point is located outside the polygon
        """
        # initialization of variables: lenght of one polygon, sum of angles, threshold value
        n = len(pol)
        total_angle = 0
        EPS = 1.0e-10

        #iterate through all vertices 
        for i in range(n):
            #point is vertex => located on edge
            if (q == pol[i]) or (q == pol[(i+1)%n]):
                return -1
            
            # compute determinant to analyze position of the point 
            # vertex i+1 - vertex i
            ux, uy = Algorithms.computeVector(pol[(i+1)%n], pol[i])

            # point q - vertex i
            vx, vy = Algorithms.computeVector(q, pol[i])
            det = (ux*vy)-(vx*uy)

            # compute vector u (point q - vertex i)
            ux, uy = Algorithms.computeVector(pol[i], q)

            # compute vecotr v (point q - vertex i+1)
            vx, vy = Algorithms.computeVector(pol[(i+1)%n], q)

            # compute angle of vectors u and v
            angle = Algorithms.computeAngle(ux,uy,vx,vy)

            # determinant determines the addition/subtraction of angle to the totalAngle
            if det > 0:
                total_angle += angle
            elif det < 0:
                total_angle -= angle

            #edge detection: point q on edge
            if det == 0 and abs(angle-pi) < EPS:
                return -1
            
        # point q is inside the polygon
        if abs(abs(total_angle) - 2*pi) < EPS:
            return 1
        # point q is outside of the polygon
        return 0
    
    def computeVector(p1,p2):
        """ Returns vector between two points. """
        x = p1.x() - p2.x()
        y = p1.y() - p2.y()
        return x,y

    def computeAngle(ax,ay,bx,by):
        """ Returns angle of two vecotrs. """
        dot_product = ax*bx + ay*by
        mod_of_vector = abs(sqrt(ax**2 + ay**2)*sqrt(bx**2 + by**2))
        omega = dot_product/mod_of_vector
        if omega > 1:
            omega = 1
        return abs(acos(omega))
    
    # Set Ray Crossing as default algorithm upon starting the app
    default_alg = rayCrossingAlgorithm