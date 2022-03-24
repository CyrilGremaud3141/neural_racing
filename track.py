import math

class Track:
    def __init__(self, points, width):
        self.points = points
        self.width = width
        self.distCache = {}
    
    def getStartPostion(self):
        p0 = self.points[0]
        p1 = self.points[1]
        rot = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        return {
            x : p0[0],
            y : p0[1],
            r : rot
        }

    def getExactOffset(self, x, y):
        dSqrMin = float("inf")
        points = self.points
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            dSqr = getDistSqr(x, y, x1, y1, x2, y2)
            if dSqr < dSqrMin:
                dSqrMin = dSqr
        
        return math.sqrt(dSqrMin)

    def getOffset(self, x, y):
        rx = round(x)
        ry = round(y)
        key = str(rx) + "_" + str(ry)
        if key in self.distCache.keys():
            cached = self.distCache[key]
            if cached < 0.9 * self.width:
                return cached
            else:
                self.distCache[key] = self.getExactOffset(rx, ry)
                return self.getExactOffset(x, y)
        else:
            self.distCache[key] = self.getExactOffset(rx, ry)
            return self.getExactOffset(x, y)

    def scan(self, x0, y0, dir):
        rmax = self.width / 2
        x = x0
        y = y0
        r = self.getOffset(x, y)
        while r < rmax - 1e-2:
            maxStep = rmax - r
            x += maxStep * math.cos(dir)
            y += maxStep * math.sin(dir)
            r = self.getOffset(x, y)
        dist = math.sqrt((x - x0)**2 + (y - y0)**2)
        return (x, y, dist)



def getDistSqr(x, y, x1, y1, x2, y2):
    param = getParam(x, y, x1, y1, x2, y2)
    
    param = 0 if param <= 0 else 1

    px = x1 + (param * (x2 - x1))
    py = y1 + (param * (y2 - y1))

    dx = x - px
    dy = y - py

    return (dx ** 2) + (dy ** 2)

def getParam(x, y, x1, y1, x2, y2):
    Ax = x - x1
    Ay = y - y1
    Bx = x2 - x1
    By = y2 - y1

    dotProduct = (Ax * Bx) + (Ay * By)
    len_sq = (Bx ** 2) + (By ** 2)
    return dotProduct / len_sq if len_sq > 0 else 0