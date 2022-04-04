import math
import pygame
import cv2 as cv
import numpy as np
pygame.init()

class Render:
    def __init__(self, track, res_x, res_y):
        self.points = track.points
        self.width = track.width
        self.resolution = res_y, res_x, 3
        self.img = np.zeros(self.resolution, np.uint8)


    def render(self):
        self.img = np.zeros(self.resolution, np.uint8)
        pts = np.array(self.points, np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(self.img,[pts],True,(0,255,255), self.width)
        

    def renderCar(self, x, y):
        cv.circle(self.img, (x, y), 1, (0,0,255), 2)

    def renderLine(self, x1, y1, x2, y2):
        cv.line(self.img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 1)

    def show(self):
        cv.imshow("image", self.img)
        cv.waitKey(1)













