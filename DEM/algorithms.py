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

    def getPointPolygonPositionR(self, q, pol):
        k = 0 #počet průsečíků
        n = len(pol) # délka polygonu

        #process all vertices
        for i in range (n):
            #reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()

            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            # z běžného seznamu tvoříme circular list - "kruhový seznam"

            #hledání vhodného segmentu - kt je prtnutý hor paprske, oba koncové body jsou v různých polorovinách
            if(yi1r > 0) and (yir <= 0) or (yir > 0) and (yi1r <= 0):
                #computing intersection
                xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)

                #increment amount of intersections
                if xm > 0:
                    k += 1
        #point is inside
        if k % 2 == 1:
            return 1
        return 0
    
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
    
    def createChull(self, pol:QPolygonF):
        #create convex hull using Jarvis scan
        ch = QPolygonF()

        #find pivot - min y coords - function min(pol, key=lambda:k.y)
        q = min(pol, key = lambda k : k.y())
        
        pj_1 = QPointF(q.x() - 1, q.y())
        pj = q

        #add q to chull
        ch.append(q)

        #Jarvis scan
        while True:
            #Initialize maximum
            phi_max = 0
            i_max = -1

            #Find suitable point maximizing angle
            for i in range(len(pol)):

                if pj != pol[i]:
                    #Measure angle
                    phi = self.get2LinesAngle(pj, pj_1, pj, pol[i])

                    #Actualize phi_max
                    if phi > phi_max:
                        phi_max = phi
                        i_max = i

            # Append point to CH
            ch.append(pol[i_max])

            #Actualize last two points
            pj_1 = pj
            pj = pol[i_max]

            #Stop condition
            if pj == q:
                break

        return ch

    def sortAngles(self, pol: QPolygonF, pivot):
        sorted_angles = []
        n = len(pol)
        for i in range(len(n)):
            if  pivot != i:
                dx = pol[(i+1)%n].x() - pol[i].x()
                dy = pol[(i+1)%n].y() - pol[i].y()
                sigma = atan2(dy,dx)

    def getPolarAngle(self, p1:QPointF, p2:QPointF):
        dx = p2.x() -p1.x()
        dy = p2.y() - p1.y()
        return atan2(dy, dx)

    def vectorOrientation(self, p1:QPointF, p2:QPointF, p3:QPointF):
        cross_prod = (p1.x() - p2.x()) * (p3.y() - p2.y()) - (p1.y() - p2.y()) * (p3.x() - p2.x())

        if cross_prod > 0:
            return 1 # ccw direction

        elif cross_prod < 0:
            return -1 # cw direction

        else:
            return 0 # collinear

    def findPivot(self, pol:QPolygonF):
        pivot = min(pol, key = lambda k : (k.y(), k.x()))
        return pivot

    def sortPoints(self, pol:QPolygonF, q:QPointF):
        sorted_points = []
        for point in pol:
            sorted_points.append(point)
        sorted_points.sort(key = lambda k: (self.getPolarAngle(q, k), self.euclidDistance(q, k)))
        return sorted_points

    def grahamScan(self, pol:QPolygonF):
        q = self.findPivot(pol)
        #pol.sort(key = lambda k: (self.getPolarAngle(q, k), self.euclidDistance(q, k)))
        sorted_points = self.sortPoints(pol, q)
        ch_list = []
        n = len(pol)
        for i in range(n):
            while len(ch_list) >= 2:
                if self.vectorOrientation(ch_list[-2], ch_list[-1], sorted_points[i]) == 1:
                    break

                else:
                    ch_list.pop()

            ch_list.append(sorted_points[i])
        ch = QPolygonF(ch_list)
        return ch

    def rotate(self, pol: QPolygonF, sig: float) -> QPolygonF:
        """Rotate polygon according to a given angle"""
        pol_rot = QPolygonF()

        #process all polygon vertices
        for i in range(len(pol)):
            # rotate point
            x_rot = pol[i].x()*cos(sig)-pol[i].y()*sin(sig)
            y_rot = pol[i].x()*sin(sig)+pol[i].y()*cos(sig)

            # create QPointF
            q_point = QPointF(x_rot,y_rot)
            # add point to polygon
            pol_rot.append(q_point)

        return pol_rot
    
    def minMaxBox(self, pol:QPolygonF):
        """create min max box"""
        # find extreme coordinates
        #x_min = min(pol, key = lambda k:k.x())# tenhle zápis vrátí bod s min xovou souřadnicí
        x_min = min(pol, key = lambda k:k.x()).x()
        x_max = max(pol, key = lambda k:k.x()).x()
        y_min = min(pol, key = lambda k:k.y()).y()
        y_max = max(pol, key = lambda k:k.y()).y()
        
        # create min max box vertices
        v1 = QPointF(x_min, y_min)
        v2 = QPointF(x_max, y_min)
        v3 = QPointF(x_max, y_max)
        v4 = QPointF(x_min, y_max)

        #append vertices into minmax box
        minmax_box = QPolygonF([v1,v2,v3,v4])

        # compute area
        a = x_max - x_min
        b = y_max - y_min
        area = a*b

        return minmax_box, area
    
    def minAreaEnclosingRectangle(self, pol: QPolygonF):
        """Create minimum area enclosing rectangle"""
        # create convex hull
        ch = self.grahamScan(pol)

        # get minmax box, area and sigma
        mmb_min, area_min = self.minMaxBox(ch)
        sigma_min = 0

        #process all segments of ch
        for i in range(len(ch)-1):
            # compute sigma
            dx = ch[i+1].x() - ch[i].x()
            dy = ch[i+1].y() - ch[i].y()

            sigma = atan2(dy,dx)

            # rotate
            ch_rot = self.rotate(ch, -sigma)

            #find mmb and area over rotated ch
            mmb, area = self.minMaxBox(ch_rot)

            if area < area_min:
                area_min = area
                mmb_min = mmb
                sigma_min = sigma

        # Rotate minmax box
        er = self.rotate(mmb_min, sigma_min)

        # Resize rectangle
        er_reduced = self.resizeRectangle(er, pol)

        return er_reduced
        
    def computeArea(self, pol: QPolygonF):
        n = len(pol)
        area = 0
        # process all vertices
        for i in range(n):
            # area increment
            area += pol[i].x() * (pol[(i+1) % n].y()-pol[(i-1+n) % n].y())
        
        return 0.5 * abs(area)
        # resize rectangle - přednáška 2 slide 38 - plocha obecného mnohoúhelníku
        # když je bod 2x, tak příspěvěk té plochy bude nulový

    def resizeRectangle(self, er: QPolygonF, pol:QPolygonF):
        # spočteme A z area(er) a Ab = area(pol)
        # poměr K
        # spočtemě těžiště
        # ui = vi-T
        # ui' = sqrt(k)*ui
        # vi' = T + ui'

        # Initialize building area and enclosing rectangle area
        ab = abs(self.computeArea(pol))
        a = abs(self.computeArea(er))

        k = ab/a

        #n_er = len(er) #tohle nevim jestli je z hodiny
        # Center of enclosing rectangle
        x_t = (er[0].x() + er[1].x() + er[2].x() + er[3].x())/4
        y_t = (er[0].y() + er[1].y() + er[2].y() + er[3].y())/4
        T = QPointF(x_t, y_t)
        # Vectors
        u1x = er[0].x() - x_t
        u1y = er[0].y() - y_t
        u2x = er[1].x() - x_t
        u2y = er[1].y() - y_t
        u3x = er[2].x() - x_t
        u3y = er[2].y() - y_t
        u4x = er[3].x() - x_t
        u4y = er[3].y() - y_t
        # Coordinates of new vertices
        v1x = x_t + sqrt(k) * u1x
        v1y = y_t + sqrt(k) * u1y
        v2x = x_t + sqrt(k) * u2x
        v2y = y_t + sqrt(k) * u2y
        v3x = x_t + sqrt(k) * u3x
        v3y = y_t + sqrt(k) * u3y
        v4x = x_t + sqrt(k) * u4x
        v4y = y_t + sqrt(k) * u4y
        # Create new vertices
        v1 = QPointF(v1x, v1y)
        v2 = QPointF(v2x, v2y)
        v3 = QPointF(v3x, v3y)
        v4 = QPointF(v4x, v4y)
        # New polygon
        er_reduced = QPolygonF([v1, v2, v3, v4])
        return er_reduced

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