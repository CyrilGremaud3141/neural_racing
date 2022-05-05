from Track import Track
import random
import math
from render import Render
import alphashape


def ranTrack():
    width = 22
    num_points = 100
    x, y = 1000, 500

    points = []
    for i in range(num_points):
        points.append([int(random.random() * x), int(random.random() * y)])

    alpha = alphashape.optimizealpha(points)
    hull = alphashape.alphashape(points, alpha)
    hull_points = hull.exterior.coords.xy
    polygon = []
    for i in range(len(hull_points[0])):
        polygon.append([hull_points[0][i], hull_points[1][i]])
    # print(polygon)

    points = []
    for i in range(1, len(polygon)):
        p1 = polygon[(i + 1 + len(polygon)) % len(polygon)]
        p2 = polygon[(i - 1 + len(polygon)) % len(polygon)]
        points.append(p2)
        points.append([int((p1[0] - p2[0]) / 2), int((p1[1] - p2[1]) / 2)])
    


    for s in range(3):
        for i in range(len(points)):
            p = points[(i + len(points)) % len(points)]
            p1 = points[(i + 1 + len(points)) % len(points)]
            p2 = points[(i - 1 + len(points)) % len(points)]
            points[i] = [int((p[0] + p1[0] + p2[0]) / 3), int((p[1] + p1[1] + p2[1]) / 3)]


        # track = Track(points, width)
        # render = Render(track, 1000, 500)
        # render.render()
        # for i in range(200):
        #     render.show()
    

    for i in range(len(points)):
        points[i] = [int(points[i][0] * 2), int(points[i][1] * 2)]
    
    # r = random.random()
    # if r > 0.5:
    #     points.reverse()


    track = Track(points, width)
    return track


if __name__ == '__main__':
    for _ in range(100):
        track = ranTrack()
        render = Render(track, 1000, 500)
        render.render()
        for i in range(100):
            render.show()