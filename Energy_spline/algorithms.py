from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *
from settings import *

class Algorithms:
    """
    A class to store algorithms for creating minimum energy spline.
    """

    def __init__(self):
        pass
    
    def getEuclidDistance(self, x1,y1,x2,y2):
        """Gets distance between two points"""
        a = x2 - x1
        b = y2 - y1
        dist = sqrt(a**2 + b**2)
        return dist
    
    def getPointLineDistance(self, xa, ya, x1, y1, x2, y2):
        """Returns distance between a point and a line."""
        # Numerator
        dn = xa * (y1 - y2) + x1*(y2 - ya) + x2*(ya - y1)
        # Denominator
        dd = self.getEuclidDistance(x1, y1, x2, y2)
        # Compute distance
        distance = dn/dd
        d1 = self.getEuclidDistance(x1, y1, xa, ya)
        k = sqrt(d1**2 - distance**2)
        xq = x1 + k*(x2-x1)/dd
        yq = y1 + k*(y2-y1)/dd

        return distance, xq, yq

    def getEuclidDistance(self, x1, y1, x2, y2):
        """Computes Euclidean distance."""
        dx = x2 - x1
        dy = y2 - y1
        return sqrt(dx ** 2 + dy ** 2)

    def getPointLineSegmentDistance(self, xa, ya, x1, y1, x2, y2):
        """Returns distance between a point A=[xa, ya] and line segment (p1, p2)."""
        # Direction vector
        ux = x2 - x1
        uy = y2 - y1
        # Normal vector
        nx = -uy
        ny = ux
        # Point P3
        x3 = x1 + nx
        y3 = y1 + ny
        # Point P4
        x4 = x2 + nx
        y4 = y2 + ny
        # Position of A according to (p1, p3) and (p2, p4)
        d13, xq3, yq3 = self.getPointLineDistance(xa, ya, x1, y1, x3, y3)
        d24, xq4, yq4 = self.getPointLineDistance(xa, ya, x2, y2, x4, y4)
        # Testing criterion
        t = d13 * d24
        # Point between two normals
        if t < 0:
            d, xq, yq = self.getPointLineDistance(xa, ya, x1, y1, x2, y2)
            return abs(d), xq, yq
        # Point in the left half plane
        if d13 > 0:
            return self.getEuclidDistance(xa, ya, x1, y1), x1, y1
        # Point in the right half plane
        return self.getEuclidDistance(xa, ya, x2, y2), x2, y2

    def getNearestLineSegmentPoint(self, xa: float, ya: float, X: matrix, Y: matrix):
        """Returns point on the barrier nearest to p."""
        # Initialize minimum point index and distance
        imin = -1
        dmin = inf
        # Size of the matrix
        m, n = X.shape
        # Browse all line segments
        for i in range(m - 1):
            # Distance between point A=[xa, ya] and line segment (p[i], p[i+1])
            di, xi, yi = self.getPointLineSegmentDistance(xa, ya, X[i, 0], Y[i, 0], X[i + 1, 0], Y[i + 1, 0])
            # Update minimum
            if di < dmin:
                dmin = di
                imin = i
                xmin = xi
                ymin = yi

        return dmin, imin, xmin, ymin

    def createA(self, alpha, beta, gamma, h, m):
        """Creates matrix used to calculate line displacement."""
        # Coefficients a, b, c
        a = alpha + (2 * beta) / h ** 2 + (6 * gamma) / h ** 4
        b = -beta / h ** 2 - (4 * gamma) / h ** 4
        c = gamma / h ** 4
        # Fill matrix with zeros
        A = zeros((m, m))
        # Process each element
        for i in range(m):
            # Main diagonal element
            A[i, i] = a
            # Non-diagonal elements, test
            if i < (m - 1):
                A[i, i + 1] = b
                A[i + 1, i] = b
            # Non-diagonal elements, test
            if i < (m - 2):
                A[i, i + 2] = c
                A[i + 2, i] = c

        return A

    def getEx(self, xi, yi, xn, yn, d, dmin):
        """Returns partial derivative of the outer energy according to x."""
        # Partial derivative of the outer energy according to x
        c = 20 * dmin
        # Vertex is closer than minimum distance
        if d < dmin:
            return -c * (xi - xn) / (dmin * d)

        return 0

    def getEy(self, xi, yi, xn, yn, d, dmin):
        """Returns partial derivative of the outer energy according to y."""
        # Partial derivative of the outer energy according to y
        c = 20 * dmin
        # Vertex is closer than minimum distance
        if d < dmin:
            return -c * (yi - yn) / (dmin * d)

        return 0

    def minEnergySpline(self, L: list[QPointF], B: list[QPointF], alpha: list[QPointF], beta: float, gamma: float,
                        lam: float, dmin: float, iters):
        """Creates displaced line."""
        ml = len(L)
        mb = len(B)
        # Create empty matrices
        XL = zeros((ml, 1))
        YL = zeros((ml, 1))
        XB = zeros((mb, 1))
        YB = zeros((mb, 1))
        # Convert polyline to matrix representation
        for i in range(ml):
            XL[i, 0] = L[i].x()
            YL[i, 0] = L[i].y()
        # Convert barrier to matrix representation
        for i in range(mb):
            XB[i, 0] = B[i].x()
            YB[i, 0] = B[i].y()
        # Compute step h
        dx = transpose(diff(transpose(XL)))
        dy = transpose(diff(transpose(YL)))
        H = sqrt(multiply(dx, dx) + multiply(dy, dy))
        h = H.mean()
        # Create A
        A = self.createA(alpha, beta, gamma, h, ml)
        # Compute inverse matrix
        I = identity(ml)
        AI = linalg.inv(A + lam * I)
        # Create difference matrices
        DX = zeros((ml, 1))
        DY = zeros((ml, 1))
        # Displaced vertices
        XLi = XL
        YLi = YL

        # Main iteration process
        for i in range(iters):
            # Partial derivatives of potentials according to dx, dy
            Ex = zeros((ml, 1))
            Ey = zeros((ml, 1))
            # Compute Ex, Ey
            for j in range(0, ml):
                # Find nearest point
                dn, idxn, xn, yn = self.getNearestLineSegmentPoint(XLi[j, 0], YLi[j, 0], XB, YB)
                # Compute Ex, Ey
                Ex[j, 0] = self.getEx(XLi[j, 0], YLi[j, 0], xn, yn, dn, dmin)
                Ey[j, 0] = self.getEy(XLi[j, 0], YLi[j, 0], xn, yn, dn, dmin)
            # Compute shifts
            DX = AI @ (lam * DX - Ex)
            DY = AI @ (lam * DY - Ey)
            XLi = XL + DX
            YLi = YL + DY
        # Convert matrix representation to polyline
        LD = []
        for j in range(ml):
            v = QPointF(XLi[j, 0], YLi[j, 0])
            LD.append(v)

        return LD