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
        # self.screen = pygame.display.set_mode(self.resolution)


    def render(self):
        # self.screen.fill((0,0,0))

        # pygame.draw.polygon(self.screen, (255, 0, 0), self.points, width=self.width)
        # for point in self.points:
        #     pygame.draw.circle(self.screen, (255, 0, 0), point, self.width/2 -2)

            

        # pygame.display.update()


        img = np.zeros(self.resolution, np.uint8)
        pts = np.array(self.points, np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(img,[pts],True,(0,255,255), self.width)

        cv.imshow("image", img)
        cv.waitKey(0)

    def renderLine(self, x1, y1, x2, y2):
        pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2))
        pygame.display.update()













