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
        pygame.display.update()












