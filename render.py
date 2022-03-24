import math
import pygame
pygame.init()

class Render:
    def __init__(self, track, res_x, res_y):
        self.points = track.points
        self.width = track.width
        self.resolution = res_x, res_y
        self.screen = pygame.display.set_mode(self.resolution)


    def render(self):
        self.screen.fill((0,0,0))

        pygame.draw.polygon(self.screen, (255, 0, 0), self.points, width=self.width)
        for point in self.points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, self.width/2 -2)

            

        pygame.display.update()

    def renderLine(self, x1, y1, x2, y2):
        pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2))
        pygame.display.update()













