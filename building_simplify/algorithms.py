from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import *

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
                    k+=1
        #point is inside
        if k % 2 == 1:
            return True
        return False
    
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
        ch = self.createChull(pol)

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

        #
    def wallAverage(self, pol: QPolygonF):
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
        pol_rot = self.rotate(pol, -sigma_aver)

        #find mmb and area over rotated pol
        mmb, area = self.minMaxBox(pol_rot)
        
        #rotate (back) min-max box
        er = self.rotate(mmb, sigma_aver)

        #resize building
        er_res = self.resizeRectangle(er, pol)
        #metoda hlavních komponent?: 

        """
        Metoda hlavních komponent
        matice A = [x1,y1...xn,y,]
        výsledekm budou vlastní čísla, vektory - v jakých směrech je budova určijící (v1 a v2 a jejich lambda1 a lambda2) - spačítám směrnici prvního hlavního vektrou - čtverec norem těch vlastních vektorů - importovat numpy
        metoda by měla být nejstabilnější známý maticový rozklad - zobecnění do 3D - výsledkem by pak byl kvádr
        """