from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import json
from math import sqrt, degrees, acos
# p = qpoint - bod má konstruktor QPoint(X,Y)
# p.x()
# p.y()
#dx = pol[i].x()
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
            if(yi1r>0) and (yir<=0) or (yir > 0) and (yi1r <= 0):
                #computing intersection
                xm = (xi1r*yir - xir*yi1r)/(yi1r-yir)

                #increment amount of intersections
                if xm > 0:
                    k+=1
        #point is inside
        if k % 2 == 1:
            return True
        return
    def windingNumber(self, q, pol):
        n = len(pol)

        for i in range(n):
            #analyze position of the point
            #můžu použít stejnou proměnnou? a to ux a uy?..
            #v momentě kdy se spočítá det...tak už můžu vektory u a v použít pro nový výpočet že?
            ux = pol[i+1%n].x() - pol[i].x()
            uy = pol[i+1%n].y() - pol[i].y()

            vx = q.x() - pol[i].x()
            vy = q.y() - pol[i].y()
            det = (ux*vy)-(vx*uy)
            
            totalAngle = 0
            #counting vector u (poit q - polygon vertex i)
            ux = pol[i].x() - q.x()
            uy = pol[i].y() - q.y()

            #counting vecotr v (poit q - polygon vertex i+1)
            vx = pol[i+1%n].x() - q.x()
            vy = pol[i+1%n].y() - q.y()

            
            #counting angle of u and v
            dotProduct = ux*vy + vx*uy
            modOfVector1 = sqrt( ux*ux + uy*uy)*sqrt(vx*vx + vy*vy) 
            angle = dotProduct/modOfVector1
            #print("Cosθ =",angle)
            angleInDegree = degrees(acos(angle))
            if det > 0:
                totalAngle += angleInDegree
            elif det < 0:
                totalAngle -= angleInDegree
            else:
                pass
                #ještě nevim
        if totalAngle == 360:
            return True
        return

