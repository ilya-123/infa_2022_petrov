import pygame
from pygame.draw import *

pygame.init()
FPS = 30
sc = pygame.display.set_mode((400, 400), pygame.RESIZABLE)
GREY = (120, 120, 120)
sc.fill(GREY)
pygame.display.flip()



YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

circle(sc, YELLOW, (200, 200), 150)
circle(sc, WHITE, (200, 200), 152, 2)

circle(sc, RED, (150, 150), 25)
circle(sc, RED, (250, 150), 25)
circle(sc, BLACK, (150, 150), 10)
circle(sc, BLACK, (250, 150), 10)

polygon(sc, BLACK, [(50, 50), (185, 130), (175, 145), (50, 70)])
polygon(sc, BLACK, [(350, 50), (215, 130), (225, 145), (350, 70)])
polygon(sc, BLACK, [(125, 250), (275, 250), (275, 275), (125, 275)])






pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()