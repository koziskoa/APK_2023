from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from math import *
from Edge import *
from triangle import *

class Algorithms:
    """
    A class to store algorithms for creating DEM, analysing DEM and other auxiliary methods.

    Methods for DEM generation & analysis
    ----------
        createDT(self, points: list[QPoint3DF]):
            Performs Delaunay triangulation.

        createContourLines(self, dt: list[Edge], zmin:float, zmax:float, dz:float):
            Generates contour lines and index contour lines.

        analyzeDTMSlope(self, dt:list[Edge]):
            Returns list of DT triangles with computed slope.

        analyzeDTMAspect(self, dt:list[Edge]):
            Returns list of DT triangles with computed aspect.

    Auxiliary methods
    ----------
        get2LinesAngle(p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
            Computes angle between two given lines.

        euclidDistance(p1:QPoint3DF, p2:QPoint3DF):
            Computes Euclidean distance.

        getPointAndLinePosition(p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
            Returns information about point position relative to line.

        getDelaunayPoint(p1: QPoint3DF, p2: QPoint3DF, points:list[QPoint3DF]):
            Finds optimal Delaunay point.

        updateAEL(self, edge: Edge, ael: list[Edge]):
            Updates active edges list.

        getNearestPoint(p: QPoint3DF, points: list[QPoint3DF]):
            Finds nearest point from point cloud to a given point.

        getContourLinePoint(p1: QPoint3DF, p2: QPoint3DF, z: float):
            Returns contour line point.

        setContourDefaultSettings():
            Sets default contour parameters (minimum, maximum, step).

        getNormalVector(p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
            Returns normal vector of the plane of triangle.

        createSlope(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
            Computes slope of a triangle.

        createAspect(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
            Computes aspect of a triangle.
    """
    def __init__(self):
        pass

    def get2LinesAngle(self, p1: QPointF, p2: QPointF, p3: QPointF, p4: QPointF):
        """
        Computes angle between two given lines.

            Parameters:
                p1, p2, p3, p4 (QPoint): Vertices of two lines.

            Returns:
               (float) Angle between input lines.
        """
        # Get vector components of the first line
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        # Get vector components of the second line
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()
        # Calculate dot product
        dp = ux * vx + uy * vy
        # Calculate norms for both vectors
        nu = sqrt(ux ** 2 + uy ** 2)
        nv = sqrt(vx ** 2 + vy ** 2)
        # Compute angle
        cos_angle = dp / (nu * nv)
        # Validate angle
        cos_angle = max(min(cos_angle, 1), -1)
        return acos(cos_angle)

    def getPointAndLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
        """
        Returns information about point position relative to line.

            Parameters:
                p (QPoint3DF): Point to be analysed.
                p1, p2 (QPoint3DF): Start and end points of a line.

            Returns:
                1: point is located in the left halfplane
                0: point is located in the right halfplane
               -1: point is collinear with the line
        """
        # Compute vector components
        ux = p2.x()-p1.x()
        uy = p2.y()-p1.y()
        vx = p.x()-p1.x()
        vy = p.y()-p1.y()
        # Calculate cross product
        t = ux * vy - uy * vx
        # Point is in the left halfplane
        if t > 0:
            return 1
        # Point is in the right halfplane
        if t < 0:
            return 0
        # Point is colinear
        return -1

    def getDelaunayPoint(self, p1: QPoint3DF, p2: QPoint3DF, points:list[QPoint3DF]):
        """
        Finds optimal Delaunay point.

            Parameters:
                p1, p2 (QPoint3DF): Start and end points of a line.
                points (list): List of input points.

            Returns:
                idx_max (int): Index of optimal Delaunay point.
        """
        # Initialize index and angle
        idx_max = -1
        om_max = 0
        # Process all points
        for i in range(len(points)):
            # Exclude identical points
            if points[i] != p1 and points[i] != p2:
                # Point in the left halfplane
                if self.getPointAndLinePosition(points[i],p1,p2) == 1:
                    # Compute angle
                    omega = self.get2LinesAngle(points[i], p1, points[i], p2)
                    # Update angle and index
                    if omega > om_max:
                        om_max = omega
                        idx_max = i
        # Return -1 if no optimal Delaunay point is found
        return idx_max
    
    def updateAEL(self, edge: Edge, ael: list[Edge]):
        """
        Updates active edges list.

            Parameters:
                edge (Edge object): Input edge.
                ael (list): List of active edges.
        """
        # Switch edge orientation
        e_o = edge.switchOrientation()
        # Remove edge if opposite orientation edge is in AEL
        if e_o in ael:
            ael.remove(e_o)
        # Opposite edge is not in AEL
        else:
            ael.append(edge)

    def euclidDistance(self, p1:QPoint3DF, p2: QPoint3DF):
        """Computes Euclidean distance."""
        return sqrt((p2.x() - p1.x())**2 + (p2.y() - p1.y())**2)

    def getNearestPoint(self, p: QPoint3DF, points: list[QPoint3DF]):
        """
        Finds nearest point from point cloud to a given point.

            Parameters:
                p (QPoint3DF): Input point.
                points (list): List of points in point cloud.

            Returns:
                idx_min (int): Index of the nearest point.
        """
        # Initialize index and angle
        idx_min = -1
        d_min = inf
        # Process all points
        for i in range(len(points)):
            # Point is not identical to any other point
            if p != points[i]:
                # Compute distance
                d = self.euclidDistance(p, points[i])
                # Update nearest point index and minimum distance
                if d < d_min:
                    d_min = d
                    idx_min = i
        return idx_min            

    def createDT(self, points: list[QPoint3DF]):
        """
        Performs Delaunay triangulation.

            Parameters:
                points (list): List of input points.

            Returns:
                dt (list): List of edges of generated triangles.
        """
        # Initialize list of edges and active edges list
        dt:list[Edge] = []
        ael:list[Edge] = []
        # Get point with the min x coordinate
        point_1 = min(points, key= lambda k: k.x())
        # Find nearest point
        point_2 = points[self.getNearestPoint(point_1, points)]
        # Create edge and opposite orientation edge
        edge = Edge(point_1, point_2)
        edge_o = Edge(point_2, point_1)
        # Add both edges to AEL
        ael.append(edge)
        ael.append(edge_o)
        # Process AEL until it is empty
        while ael:
            # Take the first edge
            e_1  = ael.pop()
            # Switch its orientation
            e_1o = e_1.switchOrientation()
            # Find index of the optimal Delaunay point
            idx = self.getDelaunayPoint(e_1o.getStart(),e_1o.getEnd(), points)
            # If optimal Delaunay point exists
            if idx != -1:
                # Create new edges
                e2 = Edge(e_1o.getEnd(),  points[idx])
                e3 = Edge(points[idx], e_1o.getStart())
                # Add edges to edges list
                dt.append(e_1o)
                dt.append(e2)
                dt.append(e3)
                # Update AEL
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)
        return dt

    def getContourLinePoint(self, p1: QPoint3DF, p2: QPoint3DF, z: float):
        """
        Returns contour line point.

            Parameters:
                p1, p2 (QPoint3DF): Start and end points of a given line.
                z (float): Z coordinate of contour line point.

            Returns:
                Intersection QPoint3DF point.
        """
        # Intersection of line and horizontal plane
        xb = (p2.x() - p1.x())*(z - p1.getZ())/(p2.getZ() - p1.getZ()) + p1.x()
        yb = (p2.y() - p1.y()) * (z - p1.getZ()) / (p2.getZ() - p1.getZ()) + p1.y()

        return QPoint3DF(xb, yb, z)

    def setContourDefaultSettings(self):
        """Sets default contour parameters (minimum, maximum, step)."""
        return 0, 1650, 10

    def createContourLines(self, dt: list[Edge], zmin:float, zmax:float, dz:float):
        """
        Generates contour lines and index contour lines.

            Parameters:
                dt (list): List of DT edges.
                zmin (float): Minimum Z coordinate.
                zmax (float): Maximum Z coordinate.
                dz (float): Step to generate contour.

            Returns:
                contours (list): List of normal contour lines.
                index_contour (list): List of index contours and their orientations.
        """
        # Return if step set to 0
        if dz == 0:
            return
        # Create contour lines inside the given interval and step
        contours: list[Edge] = []
        index_contours = []
        # Process all triangles
        for i in range(0,len(dt),3):
            # Get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            # Get normal vector of triangle
            nx, ny, nz = self.getNormalVector(p1, p2, p3)
            # Find orientation of triangle for contour labels
            label_orientation = atan2(ny, nx)
            # Adjust label angle
            label_orientation += pi/2
            # Get elevations of points
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()
            # Set contour counter
            contour_counter = -1
            # Test intersections of all planes
            for z in range(zmin, zmax, dz):
                # Get height differences
                dz1 = z - z1
                dz2 = z - z2
                dz3 = z - z3
                # Increment contour counter
                contour_counter += 1
                # Triangle is coplanar
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue
                # Edges (p1, p2) and (p2, p3) are intersected by plane
                if dz1*dz2 <= 0 and dz2*dz3 <= 0:
                    # Compute intersections
                    a = self.getContourLinePoint(p1, p2, z)
                    b = self.getContourLinePoint(p2, p3, z)
                    # Create edge
                    e = Edge(a, b)
                    # Add contour and its orientation to list of index contours
                    if contour_counter % 5 == 0:
                        index_contours.append([e, label_orientation])
                    # Add contour to list of contours
                    else:
                        contours.append(e)
                # Edges (p2, p3) and (p3, p1) are intersected by plane
                elif dz2 * dz3 <= 0 and dz3 * dz1 <= 0:
                    # Compute intersections
                    a = self.getContourLinePoint(p2, p3, z)
                    b = self.getContourLinePoint(p3, p1, z)
                    # Create edge
                    e = Edge(a, b)
                    # Add contour and its orientation to list of index contours
                    if contour_counter % 5 == 0:
                        index_contours.append([e, label_orientation])
                    # Add contour to list of contours
                    else:
                        contours.append(e)

                # Edges (p3, p1) and (p1, p2) are intersected by plane
                elif dz3 * dz1 <= 0 and dz1 * dz2 <= 0:
                    # Compute intersections
                    a = self.getContourLinePoint(p3, p1, z)
                    b = self.getContourLinePoint(p1, p2, z)
                    # Create edge
                    e = Edge(a, b)
                    # Add contour and its orientation to list of index contours
                    if contour_counter % 5 == 0:
                        index_contours.append([e, label_orientation])
                    # Add contour to list of contours
                    else:
                        contours.append(e)

        return contours, index_contours

    def getNormalVector(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        """
        Returns normal vector of the plane of triangle.

            Parameters:
                p1, p2, p3 (QPoint3DF): Points forming a triangle.

            Returns:
                nx, ny, nz (float): Normal vector components.
        """
        # First vector
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        uz = p2.getZ() - p1.getZ()
        # Second vector
        vx = p3.x() - p1.x()
        vy = p3.y() - p1.y()
        vz = p3.getZ() - p1.getZ()
        # Normal vector, components
        nx = uy * vz - vy * uz
        ny = -(ux * vz - vx * uz)
        nz = ux * vy - vx * uy

        return nx, ny, nz

    def createSlope(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        """
        Computes slope of a triangle.

            Parameters:
                p1, p2, p3 (QPoint3DF): Points forming a triangle.

            Returns:
                slope (float): Slope of the triangle.
        """
        # Get normal vector components
        nx, ny, nz = self.getNormalVector(p1, p2, p3)
        # Compute norm of normal vector
        n = sqrt(nx*nx + ny*ny + nz*nz)
        # Compute slope
        slope = acos(nz/n)

        return slope

    def createAspect(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        """
        Computes aspect of a triangle.

            Parameters:
                p1, p2, p3 (QPoint3DF): Points forming a triangle.

            Returns:
                aspect (float): Aspect of the triangle.
        """
        # Get normal vector components
        nx, ny, nz = self.getNormalVector(p1, p2, p3)
        # Calculate angle in 2D
        aspect = atan2(ny, nx)
        # Adjust angle if negative for further computation
        if aspect < 0 :
            aspect += 2*pi

        return aspect

    def analyzeDTMSlope(self, dt:list[Edge]):
        """
        Returns list of DT triangles with computed slope.

            Parameters:
                dt (list): List of edges of DT.

            Returns:
                dtm (list): List of triangles with computed slope.
        """
        # Initialize list of triangles
        dtm: list[Triangle] = []
        # Process all triangles
        for i in range(0,len(dt),3):
            # Get triangle edges
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            # Compute slope
            slope = self.createSlope(p1, p2, p3)
            # Create triangle
            triangle = Triangle(p1, p2, p3, slope, 0)
            # Add triangle to list
            dtm.append(triangle)

        return dtm

    def analyzeDTMAspect(self, dt:list[Edge]):
        """
        Returns list of DT triangles with computed aspect.

            Parameters:
                dt (list): List of edges of DT.

            Returns:
                dtm (list): List of triangles with computed aspect.
        """
        # Initialize list of triangles
        dtm: list[Triangle] = []
        # Process all triangles
        for i in range(0, len(dt), 3):
            # Get triangle edges
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()
            # Compute slope
            aspect = self.createAspect(p1, p2, p3)
            # Create triangle
            triangle = Triangle(p1, p2, p3, 0, aspect)
            # Add triangle to list
            dtm.append(triangle)

        return dtm