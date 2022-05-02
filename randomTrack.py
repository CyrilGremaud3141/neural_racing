from Track import Track
import random
import math
from render import Render


def ranTrack():
    width = 5
    num_points = 100
    x, y = 1000, 500

    points = []
    for i in range(num_points):
        points.append([int(random.random() * x), int(random.random() * y)])


    for s in range(1000):
        for i in range(num_points):
            p = points[(i + len(points)) % len(points)]
            p1 = points[(i + 1 + len(points)) % len(points)]
            p2 = points[(i - 1 + len(points)) % len(points)]
            points[i] = [int((p[0] + p1[0] + p2[0]) / 3), int((p[1] + p1[1] + p2[1]) / 3)]


        track = Track(points, width)
        render = Render(track, 1000, 500)
        render.render()
        for i in range(10):
            render.show()
    








    



    track = Track(points, width)
    return track


if __name__ == '__main__':
    track = ranTrack()
    render = Render(track, 1000, 500)
    render.render()
    for i in range(1000):
        render.show()