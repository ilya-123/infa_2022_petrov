import pygame
import numpy as np
from pygame.draw import *
from random import randint, random

name = str()
pygame.init()
screen_x = 1400
screen_y = 800
text_x = 50
text_y = 40
wall = 100
balls = list()
number_of_balls = 5
max_speed = 15
restart_screen_x = 110
restart_screen_y = 70
time = 0
time_x = 650
time_y = 40
flag = False

FPS = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
# table = pd.read_csv("tabular.csv")
f = pygame.font.Font('minecraft.ttf', 24)
restart_im = pygame.image.load("restart.png").convert_alpha()
restart_im = pygame.transform.scale(restart_im, (restart_screen_x, restart_screen_y))


class Ball:

    def __init__(self):
        self.r = randint(20, 30)
        self.x = randint(wall + self.r, screen_x - wall - self.r)
        self.y = randint(wall + self.r, screen_y - wall - self.r)
        self.v_x = random() * max_speed * (-1) ** randint(-5, 5)
        self.v_y = random() * max_speed * (-1) ** randint(-5, 5)
        self.color = COLORS[randint(0, 5)]

    def draw_ball(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def need_for_speed(self):
        self.x += self.v_x
        self.y += self.v_y

    def wall_check(self):
        if (self.x + self.v_x + self.r > screen_x - wall) or (self.x + self.v_x - self.r < wall):
            self.v_x = -random() * max_speed * np.sign(self.v_x)
            self.v_y = random() * max_speed * ((-1) ** randint(-5, 5))
        elif (self.y + self.v_y + self.r > screen_y - wall) or (self.y + self.v_y - self.r < wall):
            self.v_y = -random() * max_speed * np.sign(self.v_y)
            self.v_x = random() * max_speed * ((-1) ** randint(-5, 5))

    def click(self):
        global balls
        if (event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2 <= self.r ** 2:
            del balls[i]


def restart_check():
    global flag
    if (screen_x - restart_screen_x < event.pos[0] < screen_x) \
            and (0 < event.pos[1] < restart_screen_y):
        flag = True


pygame.display.update()
clock = pygame.time.Clock()
finished = False

for i in range(number_of_balls):
    balls.append(Ball())
while not finished:
    if len(balls) == 0:
        finished = True
    if flag:
        balls.clear()
        time = 0
        flag = False
        for i in range(number_of_balls):
            balls.append(Ball())
    polygon(screen, WHITE,
            [(wall, wall), (screen_x - wall, wall), (screen_x - wall, screen_y - wall), (wall, screen_y - wall)], 3)
    polygon(screen, WHITE,
            [(screen_x, 0), (screen_x, restart_screen_y), (screen_x - restart_screen_x, restart_screen_y),
             (screen_x - restart_screen_x, 0)])
    for i in range(len(balls)):
        balls[i].draw_ball()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            restart_check()
            for i in range(len(balls) - 1, -1, -1):
                balls[i].click()

    for i in range(len(balls)):
        balls[i].wall_check()
        balls[i].need_for_speed()
    sc_text = f.render(f'Ваш счёт: {number_of_balls - len(balls)}', True, WHITE)
    screen.blit(sc_text, (text_x, text_y))
    screen.blit(restart_im, (screen_x - restart_screen_x, 0))
    counter = f.render(f'Время: {int(time)}', True, WHITE)
    screen.blit(counter, (time_x, time_y))
    pygame.display.update()
    time += 1 / FPS
    screen.fill(BLACK)
    clock.tick(FPS)

screen.fill(BLACK)
screen.blit(f.render("Введите своё имя: ", True, RED), (screen_x / 3, screen_y / 3))
pygame.display.update()
finished = False
name = ""
dict_records = {}
while not finished:

    screen.fill(BLACK)
    screen.blit(f.render("Введите своё имя:", True, RED), (screen_x / 3, screen_y / 3))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                finished = True
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            else:
                name += event.unicode
        screen.blit(f.render(name, True, RED), (screen_x / 2, screen_y / 2))
        pygame.display.update()
dict_records[name] = time
print(dict_records)
with open('records.txt', 'a') as file:
    for key, value in dict_records.items():
        file.write(f'{key}, {value}\n')
pygame.quit()
