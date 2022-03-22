import math
class Track:
    def __init__(self, points, widht):
        self.points = points
        self.widht = widht
    
    def getStartPostion(self):
        p0 = self.points[0]
        p1 = self.points[1]
        rot = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        return {
            x : p0[0],
            y : p0[1],
            r : rot
        }

    