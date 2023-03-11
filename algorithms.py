from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import sqrt, pi, acos
# p = qpoint - bod má konstruktor QPoint(X,Y)
# p.x()
# p.y()
#dx = pol[i].x()
class Algorithms:

    def __init__(self):
        pass

    def rayCrossingAlgorithm(self, q, pol):
        kr = 0 #počet průsečíků
        kl = 0
        n = len(pol) # délka polygonu

        #process all vertices
        for i in range (n):
            #reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()

            if xir == 0 and yir == 0:
                return -1

            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            # z běžného seznamu tvoříme circular list - "kruhový seznam"

            #if (yi1r > 0) and (yir <= 0) or (yir > 0) and (yi1r <= 0):
            if (yi1r - yir) == 0:
                continue

            xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)
            #hledání vhodného segmentu - kt je prtnutý hor paprske, oba koncové body jsou v různých polorovinách
            if (yi1r < 0) != (yir < 0):
                if xm < 0:
                    kl += 1

            if (yi1r > 0) != (yir > 0):
                #computing intersection
                if xm > 0:
                    kr += 1

        if (kr % 2 == 1):
            return 1

        elif (kl % 2) != (kr % 2):
            return -1
        return 0
    def windingNumber(self, q, pol):
        n = len(pol)
        totalAngle = 0
        eps = 1.0e-10
        for i in range(n):
            #analyze position of the point
            #můžu použít stejnou proměnnou? a to ux a uy?..
            #v momentě kdy se spočítá det...tak už můžu vektory u a v použít pro nový výpočet že?
            ux = pol[(i+1)%n].x() - pol[i].x()
            uy = pol[(i+1)%n].y() - pol[i].y()

            vx = q.x() - pol[i].x()
            vy = q.y() - pol[i].y()
            det = (ux*vy)-(vx*uy)
            #if det == 0:
                #return -1

            #counting vector u (poit q - polygon vertex i)
            ux = pol[i].x() - q.x()
            uy = pol[i].y() - q.y()

            #counting vecotr v (poit q - polygon vertex i+1)
            vx = pol[(i+1)%n].x() - q.x()
            vy = pol[(i+1)%n].y() - q.y()

            #counting angle of u and v
            dotProduct = ux*vx + uy*vy
            modOfVector1 = abs(sqrt(ux**2 + uy**2)*sqrt(vx**2 + vy**2))
            angle = dotProduct/modOfVector1
            if angle > 1:
                angle = 1
            #print("Cosθ =",angle)
            angle = abs(acos(angle))
            if det > 0:
                totalAngle += angle
            elif det < 0:
                totalAngle -= angle
            if det == 0 and abs(angle-pi)< eps:
                print("probiha iterace")
                return -1
                #hranice polygonu ještě nevim
            #print(angle, det)
            #print(totalAngle)
        if abs(abs(totalAngle) - 2*pi) < eps:
            return 1
        return 0

