from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import json
# p = qpoint - bod má konstruktor QPoint(X,Y)
# p.x()
# p.y()
#dx = pol[i].x()
class Algorithms:

    def __init__(self):
        pass

    def getPointPolygonPositionR(self, q, pol):
        kr = 0 #počet průsečíků
        kl = 0
        n = len(pol) # délka polygonu

        #process all vertices
        for i in range (n):
            #reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()

            if xir == 0 and yir == 0:
                return True

            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            # z běžného seznamu tvoříme circular list - "kruhový seznam"

            #if (yi1r > 0) and (yir <= 0) or (yir > 0) and (yi1r <= 0):
            if yi1r - yir == 0:
                continue

            xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)
            #hledání vhodného segmentu - kt je prtnutý hor paprske, oba koncové body jsou v různých polorovinách
            if (yi1r < 0) != (yir < 0):
                if xm < 0:
                    kl += 1

            elif (yi1r > 0) != (yir > 0):
                #computing intersection
                if xm > 0:
                    kr += 1

        if (kr % 2 == 1) or ((kl % 2) != (kr%2)):
            return True
        return