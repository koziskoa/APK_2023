from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from math import *
from Edge import *
from triangle import *

class Algorithms:
    def __init__(self):
        pass
    
    def get2LinesAngle(self,p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
        ux = p2.x()-p1.x()
        uy = p2.y()-p1.y()

        vx = p4.x()-p3.x()
        vy = p4.y()-p3.y()

        #dot porduct
        dp = ux*vx + uy*vy

        #norms of vecotrs u and v
        nu = sqrt(ux**2 + uy**2)
        nv = sqrt(vx**2 + vy**2)

        cos_angle = dp / (nu * nv)
        cos_angle = max(min(cos_angle,1), -1)

        return acos(cos_angle)
    

    def euclidDistance(self, p1:QPointF, p2: QPointF):
        a = p2.x() - p1.x()
        b = p2.y() - p1.y()
        dist = sqrt(a**2 + b**2)
        return dist

    def getPointAndLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
        ux = p2.x()-p1.x()
        uy = p2.y()-p1.y()

        vx = p.x()-p1.x()
        vy = p.y()-p1.y()

        t = ux * vy - uy * vx

        # point is in the left halfplane
        if t > 0:
            return 1
        
        # point is in the right halfplane
        if t < 0:
            return 0
        
        # colinear point
        return -1
        
        # funkce v podstatě na hledání maxima
    def getDelaunayPoint(self, p1: QPoint3DF, p2: QPoint3DF, points:list[QPoint3DF]):
        '''Fid optimal Delaunay point'''
        idx_max = -1
        om_max = 0

        #process all points
        for i in range(len(points)):
            #exlude identical points
            if points[i] != p1 and points[i] != p2:
                # Point in the left halfplane
                if self.getPointAndLinePosition(points[i],p1,p2) == 1:
                    # compute angle
                    omega = self.get2LinesAngle(points[i], p1, points[i], p2)
                    # actualize angle
                    if omega > om_max:
                        om_max = omega
                        idx_max = i
        return idx_max
    # update active edges list
    def updateAEL(self, edge: Edge, ael: list[Edge]):
        """ update of AEL"""
       #change oreientation
        e_o = edge.SwitchOrientation()
        # opposite edge in AEL
        if e_o in ael:
            ael.remove(e_o)
        # opposite edge is not in edge 
        else:
            ael.append(edge)
    """
    samotná triangulace
    na vstupu - množinu bodů (list_of_points)
    triangulaci ukládáme po hranách
    vrcí list DT
    """    
    def getNearestPoint(self, p: QPoint3DF, points: list[QPoint3DF]):
        # find the nearest point
        idx_min = -1
        d_min = inf

        #process all poitns
        for i in range(len(points)):
            # p is different from points
            if p != points[i]:
                # cimpute distace
                d_x = points[i].x() - p.x()
                d_y = points[i].y() - p.y()

                d = sqrt(d_x**2 + d_y**2)

                #update minimum
                if d < d_min:
                    d_min = d
                    idx_min = i

        return idx_min            

    
    def createDT(self, points: list[QPoint3DF]):
        """Create Delaunay triangulation"""
        dt:list[Edge] = []
        ael:list[Edge] = []

        # find a point with the min x coordinate
        point_1 = min(points, key= lambda k: k.x())
        # find nearest point
        point_2 = points[self.getNearestPoint(point_1, points)]

        # create edge and opposite edge
        edge = Edge(point_1, point_2)
        edge_o = Edge(point_2, point_1)

        # add two edges to AEL
        ael.append(edge)
        ael.append(edge_o)

        # process AEL until it is empty
        while ael:
            # take the first edge
            e_1  = ael.pop()
            # switch orientation
            e_1o = e_1.SwitchOrientation()

            # find index of the optimal Delaunay point
            idx = self.getDelaunayPoint(e_1o.getStart(),e_1o.getEnd(), points)

            # is the point in the AEL
            if idx != -1:
                e2 = Edge(e_1o.getEnd(),  points[idx])
                e3 = Edge(points[idx], e_1o.getStart())
                
                # add edges to dt
                dt.append(e_1o)
                dt.append(e2)
                dt.append(e3)

                # 
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)
        return dt



        """
        hledáme takový bod, který bude ležet od našeho nalezeného bodu vlavo

        buď náhodný bod, nebo s nejmenší xovou souřad - vytvoříme 2 hrany
        dokud ael není prázdný - vezmeme z něj nějakou htanu, změníme její orientaci - a následně hledáme optimální delaunyovský bod . pokud takový bod existuje?
        
        pokud existuje - do del triangulace - přidáváme hrany: e1, e2, e3 (ccw orientace) - přidáme jenom 2 hrany (do AEL)
        je to trochu složitější: viz slide 36 3. situace - do AEL nemůžeme přidat 2 hrany (byl by to nekonečný cyklus), ale jednu
        musíme se tedy zeptat, jestli tam není hrana s opačnou orientaci:
            je tam: tuto hranu s opačnou orientací smažeme - už k ní nebude existuovat žádný kandidátní trojúhelník
            není tam: vše vpořádku 

        na vstupu má hranu e a AEL
        hraně e změníme orientaci
        pokud e existuje v ALE - TAK JÍ ODSTRANÍM, pokud ne, tak v pohodě

        """

    def getContourLinePoint(self, p1: QPoint3DF, p2: QPoint3DF, z: float):
        # Intersection of line and horizontal plane
        xb = (p2.x() - p1.x())*(z - p1.getZ())/(p2.getZ() - p1.getZ()) + p1.x()
        yb = (p2.y() - p1.y()) * (z - p1.getZ()) / (p2.getZ() - p1.getZ()) + p1.y()

        return QPoint3DF(xb, yb, z)
    
    def createContourLines(self, dt: list[Edge], zmin:float, zmax:float, dz:float ):
        # Create contour lines inside the given interval and step
        contours: list[Edge] = []

        #Process all triangles
        for i in range(0,len(dt),3):
            #Get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()

            # Get elevations of points
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()

            # test intersections of all planes
            for z in range(zmin, zmax, dz):
                #Get heigh differencies
                dz1 = z - z1
                dz2 = z - z2
                dz3 = z - z3

                #Triangle is coplanar
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue

                #Edges (p1,p2) and (p2,p3) are intersected by plane
                if dz1*dz2 <= 0 and dz2*dz3 <= 0:
                    #Compute intersections
                    a = self.getContourLinePoint(p1, p2, z)
                    b = self.getContourLinePoint(p2, p3, z)

                    #Create edge
                    e = Edge(a, b)

                    #Add contour to list of contours
                    contours.append(e)

                # Edges (p2,p3) and (p3,p1) are intersected by plane
                elif dz2 * dz3 <= 0 and dz3 * dz1 <= 0:
                    # Compute intersections
                    a = self.getContourLinePoint(p2, p3, z)
                    b = self.getContourLinePoint(p3, p1, z)

                    # Create edge
                    e = Edge(a, b)

                    # Add contour to list of contours
                    contours.append(e)

                # Edges (p3,p1) and (p1,p          2) are intersected by plane
                elif dz3 * dz1 <= 0 and dz1 * dz2 <= 0:
                    # Compute intersections
                    a = self.getContourLinePoint(p3, p1, z)
                    b = self.getContourLinePoint(p1, p2, z)

                    # Create edge
                    e = Edge(a, b)

                    # Add contour to list of contours
                    contours.append(e)

        return contours
    
    """Analýza sklonu
    vstup: trojúhelník - 3 vrcholy (p1, p2, p3)
    spočítáme normálový vektor - jako vektorový součin nt(u x v) = nx, ny, nz
    spočteme úhel k vodorovné rovině - normálový vektor vodorovné roviny n(0,0,1 - z praktických důvodů, ale může být cokoliv R+)
        cos phi = (nt*n)/(|n|*|nt|) ==  nz/|nt|
    trojúhelník: p1, p2, p3
        slope
        Azimut = expozice 
        
        budeme procházet DMT
        vezmeme trojúhelník a spočítáme pro něj slope"""

    def getNormalVector(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        uz = p2.getZ() - p1.getZ()

        # second vector
        vx = p3.x() - p1.x()
        vy = p3.y() - p1.y()
        vz = p3.getZ() - p1.getZ()

        # normal vector, components
        nx = uy * vz - vy * uz
        ny = -(ux * vz - vx * uz)
        nz = ux * vy - vx * uy

        return nx, ny, nz

    def createSlope(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        nx, ny, nz = self.getNormalVector(p1, p2, p3)

        # norm 
        n = sqrt(nx*nx + ny*ny + nz*nz)

        # compute slope
        slope = acos(nz/n)

        return slope

    def createAspect(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        nx, ny, nz = self.getNormalVector(p1, p2, p3)
        aspect = atan2(ny, nx)
        if aspect < 0 :
            aspect += 2*pi

        return aspect

    def analyzeDTMSlope(self, dt:list[Edge]):
        """returns list of triangles"""

        dtm: list[Triangle] = []

        #process all triangles
        for i in range(0,len(dt),3):
            # get triangles edges
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()

            # compute slope
            slope = self.createSlope(p1, p2, p3)
            
            # create triangle
            triangle = Triangle(p1, p2, p3, slope, 0)
            
            # Add triangle to the list
            dtm.append(triangle)

        return dtm

    def analyzeDTMAspect(self, dt:list[Edge]):
        dtm: list[Triangle] = []

        # process all triangles
        for i in range(0, len(dt), 3):
            # get triangles edges
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i + 1].getEnd()

            # compute slope
            aspect = self.createAspect(p1, p2, p3)

            # create triangle
            triangle = Triangle(p1, p2, p3, 0, aspect)

            # Add triangle to the list
            dtm.append(triangle)

        return dtm

    """
    expozici si uděláme sami - jeeeee - bezesné noci
    """