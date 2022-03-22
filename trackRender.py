import pygame
pygame.init()

class Renderer:
    def __init__(self, track, background):
        self.background = background


size = width, height = 320*2, 240*2

speed = [2, 2]

black = 0, 0, 0


screen = pygame.display.set_mode(size)


car = pygame.image.load("car.png")

car_size = car.get_rect()

while 1:

    for event in pygame.event.get():

        if event.type == pygame.QUIT: sys.exit()


    screen.fill(black)

    screen.blit(car, car_size)

    pygame.display.flip()