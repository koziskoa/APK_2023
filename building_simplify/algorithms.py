from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import *

class Algorithms:
    def __init__(self):
        pass

    def get2LinesAngle(p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
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
    
    def jarvisScan(pol:QPolygonF):
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
                    phi = Algorithms.get2LinesAngle(pj, pj_1, pj, pol[i])

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

    def grahamScan(pol:QPolygonF):
        '''
        - odůvodnění ve zprávě proč jsme použily překlikávátka na konvexní obálky
        '''
        q = Algorithms.findPivot(pol)
        #pol.sort(key = lambda k: (self.getPolarAngle(q, k), self.euclidDistance(q, k)))
        ch = QPolygonF()
        sorted_points = Algorithms.sortPoints(pol, q)
        ch_list = []
        n = len(pol)
        for i in range(n):
            while len(ch_list) >= 2:
                # Check for CW direction instead of CCW as the y axis is flipped
                if Algorithms.vectorOrientation(ch_list[-2], ch_list[-1], sorted_points[i]) == -1:
                    break

                else:
                    ch_list.pop()

            ch_list.append(sorted_points[i])

        ch = QPolygonF(ch_list)
        return ch

    def sortAngles(self, pol: QPolygonF, pivot):
        sorted_angles = []
        n = len(pol)
        for i in range(len(n)):
            if  pivot != i:
                dx = pol[(i+1)%n].x() - pol[i].x()
                dy = pol[(i+1)%n].y() - pol[i].y()
                sigma = atan2(dy,dx)

    def getPolarAngle(p1:QPointF, p2:QPointF):
        dx = p2.x() -p1.x()
        dy = p2.y() - p1.y()
        return atan2(dy, dx)

    def vectorOrientation(p1:QPointF, p2:QPointF, p3:QPointF):
        cross_prod = (p1.x() - p2.x()) * (p3.y() - p2.y()) - (p1.y() - p2.y()) * (p3.x() - p2.x())

        if cross_prod > 0:
            return 1 # ccw direction

        elif cross_prod < 0:
            return -1 # cw direction

        else:
            return 0 # collinear

    def findPivot(pol:QPolygonF):
        pivot = min(pol, key = lambda k : (k.y(), k.x()))
        return pivot

    def sortPoints(pol:QPolygonF, q:QPointF):
        sorted_points = []
        for point in pol:
            sorted_points.append(point)
        sorted_points.sort(key = lambda k: (Algorithms.getPolarAngle(q, k), Algorithms.euclidDistance(q, k)))
        return sorted_points



    def rotate(pol: QPolygonF, sig: float) -> QPolygonF:
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
    
    def minMaxBox(pol:QPolygonF):
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
    
    def minAreaEnclosingRectangle(pol: QPolygonF):
        """Create minimum area enclosing rectangle"""
        # create convex hull
        ch = Algorithms.ch_alg(pol)

        # get minmax box, area and sigma
        mmb_min, area_min = Algorithms.minMaxBox(ch)
        sigma_min = 0

        #process all segments of ch
        for i in range(len(ch)-1):
            # compute sigma
            dx = ch[i+1].x() - ch[i].x()
            dy = ch[i+1].y() - ch[i].y()

            sigma = atan2(dy,dx)

            # rotate
            ch_rot = Algorithms.rotate(ch, -sigma)

            #find mmb and area over rotated ch
            mmb, area = Algorithms.minMaxBox(ch_rot)

            if area < area_min:
                area_min = area
                mmb_min = mmb
                sigma_min = sigma

        # Rotate minmax box
        er = Algorithms.rotate(mmb_min, sigma_min)

        # Resize rectangle
        er_reduced = Algorithms.resizeRectangle(er, pol)

        return er_reduced
        
    def computeArea(pol: QPolygonF):
        n = len(pol)
        area = 0
        # process all vertices
        for i in range(n):
            # area increment
            area += pol[i].x() * (pol[(i+1) % n].y()-pol[(i-1+n) % n].y())
        
        return 0.5 * abs(area)
        # resize rectangle - přednáška 2 slide 38 - plocha obecného mnohoúhelníku
        # když je bod 2x, tak příspěvěk té plochy bude nulový

    def resizeRectangle(er: QPolygonF, pol:QPolygonF):
        # spočteme A z area(er) a Ab = area(pol)
        # poměr K
        # spočtemě těžiště
        # ui = vi-T
        # ui' = sqrt(k)*ui
        # vi' = T + ui'

        # Initialize building area and enclosing rectangle area
        ab = abs(Algorithms.computeArea(pol))
        a = abs(Algorithms.computeArea(er))

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

        #
    def wallAverage(pol: QPolygonF):
        # compute sigma
        dx = pol[1].x() - pol[0].x()
        dy = pol[1].y() - pol[0].y()

        sigma = atan2(dy,dx)

        n = len(pol)
        r_aver = 0
        #process all edges
        for i in range(1,n):
            dx_i = pol[(i+1)%n].x() - pol[i].x()
            dy_i = pol[(i+1)%n].y() - pol[i].y()

            sigma_i = atan2(dy_i, dx_i)

            #direction differences
            delta_sigma_i = sigma_i-sigma

            if delta_sigma_i < 0:
                delta_sigma_i += 2*pi

            #fraction by pi/2
            k_i = round(2*delta_sigma_i/pi)

            #remainder
            r_i = delta_sigma_i - (k_i * (pi/2))

            #kámo, co to je? - average reminder
            r_aver += r_aver + r_i #počítám čitatel....tohle nebo vážit hranami: X = sum w_i(s_i)*x_i(r_i) - čím větší strana tím větší vliv úhlu
        
        #average remainder
        r_aver = r_aver/n

        #average_rotation
        sigma_aver = sigma + r_aver

        # vzali jsme 1. stranu: modulo pi/2,2. strana: modulo pi/2,... - dohromady jsme z toho spočetli průměrný zbytek
        # otočíme o sigma aver
        # rotate
        pol_rot = Algorithms.rotate(pol, -sigma_aver)

        #find mmb and area over rotated pol
        mmb, area = Algorithms.minMaxBox(pol_rot)
        
        #rotate (back) min-max box
        er = Algorithms.rotate(mmb, sigma_aver)

        #resize building
        er_res = Algorithms.resizeRectangle(er, pol)
        return er_res
        #metoda hlavních komponent?: 

    def euclidDistance(p1:QPointF, p2: QPointF):
        return sqrt((p2.x() - p1.x())**2 + (p2.y() - p1.y())**2)

    def longestEdge(pol:QPolygonF):
        '''NĚCO'''
        n = len(pol)
        longest_edge = -1
        #q = QPointF()
        ch = Algorithms.ch_alg(pol)

        for i in range(n):
            actual_edge = Algorithms.euclidDistance(pol[i],pol[(i+1)%n])
            if actual_edge > longest_edge:
                longest_edge = actual_edge
                dx = pol[(i+1)%n].x() - pol[i].x()
                dy = pol[(i+1)%n].y() - pol[i].y()

        sigma_l = atan2(dy,dx)

        building_rot = Algorithms.rotate(pol,-sigma_l)

        mmb_l, area_l = Algorithms.minMaxBox(building_rot)
        er = Algorithms.rotate(mmb_l, sigma_l)
        
        res = Algorithms.resizeRectangle(er, pol)

        return res

    def findDiagonals(ch:QPolygonF):
        diagonals = []
        n = len(ch)-1
        for i in range(n):
            for j in range(i+1, n):
                if (j != (i-1+n)%n) and (j != (i+1)%n):
                    diagonals.append([ch[i], ch[j], Algorithms.euclidDistance(ch[i], ch[j])])
        return diagonals

    def intersectionTest(p1:QPointF, p2:QPointF, pol:QPolygonF):
        n = len(pol)
        for i in range(n):

            point = pol[i]
            point_after = pol[(i+1)%n]

            if (p1 == point or p1 == point_after) or (p2 == point or p2 == point_after):
                continue

            t1 = ((p2.x()-p1.x())*(point_after.y()-p1.y())-((point_after.x()-p1.x())*(p2.y()-p1.y())))
            t2 = ((p2.x()-p1.x())*(point.y()-p1.y())-((point.x()-p1.x())*(p2.y()-p1.y())))
            t3 = ((point_after.x()-point.x())*(p1.y()-point.y())-((p1.x()-point.x())*(point_after.y()-point.y())))
            t4 = ((point_after.x()-point.x())*(p2.y()-point.y())-((p2.x()-point.x())*(point_after.y()-point.y())))

            if t1*t2 >= 0 or t3*t4 >=0:
                continue
            else:
                return True
        return False

    def setDiagonals(diagonals, pol):
        # dve premenne na Null
        # vyplnia sa
        sigma1 = None
        dist1 = None
        sigma2 = None
        dist2 = None

        for i in range(len(diagonals)):
            p1, p2 = diagonals[i][0], diagonals[i][1]
            res = Algorithms.intersectionTest(p1, p2, pol)
            if res == True:
                continue

            else:
                if dist1 is None:
                    dx = diagonals[i][0].x() - diagonals[i][1].x()
                    dy = diagonals[i][0].y() - diagonals[i][1].y()
                    sigma1 = atan2(dy, dx)
                    dist1 = diagonals[i][2]

                else:
                    dx = diagonals[i][0].x() - diagonals[i][1].x()
                    dy = diagonals[i][0].y() - diagonals[i][1].y()
                    sigma2 = atan2(dy, dx)
                    dist2 = diagonals[i][2]
                    break

        if sigma1 is None:
            dx = diagonals[0][0].x() - diagonals[0][1].x()
            dy = diagonals[0][0].y() - diagonals[0][1].y()
            sigma1 = atan2(dy, dx)
            dist1 = diagonals[0][2]

        if sigma2 is None:
            dx = diagonals[1][0].x() - diagonals[1][1].x()
            dy = diagonals[1][0].y() - diagonals[1][1].y()
            sigma2 = atan2(dy, dx)
            dist2 = diagonals[1][2]

        return sigma1, dist1, sigma2, dist2

    def weightedBisector(pol:QPolygonF):
        ch = Algorithms.ch_alg(pol)
        if len(ch) <= 4:
            return ch
        start = 0
        diagonals = Algorithms.findDiagonals(ch)
        diagonals.sort(key=lambda k: k[2], reverse=True)
        sigma1, dist1, sigma2, dist2 = Algorithms.setDiagonals(diagonals, pol)

        sigma = (dist1*sigma1 + dist2*sigma2)/(dist1+dist2)
        building_rot = Algorithms.rotate(pol, -sigma)

        mmb, area = Algorithms.minMaxBox(building_rot)
        er = Algorithms.rotate(mmb, sigma)

        res = Algorithms.resizeRectangle(er, pol)

        return res

        # metoda TEST
        # weightedBisector

        """
                for i in range(len(pol)):
            for j in range(len(pol)):
                if pol[i] != pol[j]:
                    if pol[(i+1)/len(pol)] or pol[(i-1)/len(pol)]: # řekněme, že jsem se touhle podmínkou zbavila p+1 a p-1
                        continue # doufám, že to je jdi na další index
                    diagonals.append([pol[i], pol[j]])
        """



        """
        Metoda hlavních komponent
        matice A = [x1,y1...xn,y,]
        výsledekm budou vlastní čísla, vektory - v jakých směrech je budova určijící (v1 a v2 a jejich lambda1 a lambda2) - spačítám směrnici prvního hlavního vektrou - čtverec norem těch vlastních vektorů - importovat numpy
        metoda by měla být nejstabilnější známý maticový rozklad - zobecnění do 3D - výsledkem by pak byl kvádr

def longestEdge(self, pol:QPolygonF):
        '''NĚCO'''
        n = len(pol)
        longest_edge = -1
        #q = QPointF()
        #ch = self.createChull(pol)

        for i in range(n):
            actual_edge = self.euclidDistance(pol[i],pol[(i+1)%n])
            if actual_edge > longest_edge:
                longest_edge = actual_edge

                dx = pol[(i+1)%n].x() - pol[i].x()
                dy = pol[(i+1)%n].y() - pol[i].y()

                sigma_l = atan2(dy,dx)
                building_rot = self.rotate(pol,-sigma_l)

        mmb_rot, area = self.minMaxBox(building_rot)
        er = self.rotate(mmb_rot, sigma_l)

        #mmb_lrot = self.rotate(mmb_l, sigma_l)
        res = self.resizeRectangle(er, pol)

        return res

        """
    ch_alg = jarvisScan