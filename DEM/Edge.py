from QPoint3DF import *

class Edge:
    def __init__(self, start: QPoint3DF, end: QPoint3DF):
        self.__start = start
        self.__end = end

    def getStart(self):
        '''Return start point'''
        return self.__start
    
    def getEnd(self): #např když se budeme dotazovat na počáteční nebo koncový bod
        '''Return end point'''
        return self.__end
    
    def SwitchOrientation(self):
        '''Create new edge with an opposite orientatioin'''
        return Edge(self.__end, self.__start)
    
    def __eq__(self, other) -> bool:
        '''compare two edges'''
        return (self.__start == other.__start) and (self.__end == other.__end)
    
    '''můžeme získat startovní, konvový bod a můžeme změnit její orientaci ale musíme si nadefinovati porovnávací operace
    __Lt__
    __Gt__
    __eq__ - budou se rovnat jejich počáteční a koncové body: se - overloading operátorů - přetěžování operátorů
    
    u jakéhokoliv uživatelského typu musíme nadefinovat svoje porovnávací metody'''