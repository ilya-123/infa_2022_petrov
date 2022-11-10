import math
import numpy as np
from random import choice
from random import randint, random
import pygame
from pygame.draw import *

pygame.font.init()

FPS = 60

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

f = pygame.font.Font(None, 24)
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
gun_im = pygame.image.load("72k.png").convert_alpha()
gun_im = pygame.transform.scale(gun_im, (75, 50))
roze = pygame.image.load("roza.png").convert_alpha()
muxa = pygame.image.load("muxa.png").convert_alpha()
im = pygame.image.load("star.png").convert_alpha()
im = pygame.transform.scale(im, (30, 30))


class Ball:

    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball
            ball - мячики, которыми стреляет пчёлка
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        x, y берутся из положения пушки в момент отпускания кнопки мыши
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 7  # Время жизни каждого из шарика (в секундах)

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (self.x + self.vx + self.r >= 800) or (self.x + self.vx - self.r <= 0):
            self.vx = -self.vx / 2
        if self.y + self.r >= 550:
            self.vy = -self.vy / 2
            self.vx = self.vx / 2
            self.y = 530
        self.vy -= 20 / FPS
        self.vx = 0.997 * self.vx
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """Рисует шарик"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r, 5
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r - 5
        )
        # После каждой прорисовки уменьшает время жизни шарика:
        self.live -= 1 / FPS

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:

    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 70
        self.y = 500
        self.vx = 10
        self.vy = 10

    def move(self):
        """Функция движения пчелы"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.vx
        if keys[pygame.K_d]:
            self.x += self.vx

    def fire2_start(self):
        """Флажок, показывающий, зажата ли мышь"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        if target.live or fly.live:
            bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] == self.x:
            a = self.x + 0.01
        else:
            a = event.pos[0]
        if event:
            self.an = math.atan((event.pos[1] - self.y) / (a - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пчёлку и жало"""
        pos = pygame.mouse.get_pos()
        r = 3  # радиус жала
        L = 50  # начальная длина жала
        e = (pos[0] - self.x, pos[1] - self.y)
        mod = (e[0] ** 2 + e[1] ** 2) ** 0.5
        e = (e[0] / mod, e[1] / mod)  # Единичный направляющий ветор жала
        n = (-e[1], e[0])  # Вектор нормали к жалу

        polygon(screen, self.color,
                [(self.x + r * n[0], self.y + r * n[1]), (self.x - r * n[0], self.y - r * n[1]),
                 (self.x - r * n[0] + (L + self.f2_power) * e[0],
                  self.y - r * n[1] + (L + self.f2_power) * e[1]),
                 (self.x + r * n[0] + (L + self.f2_power) * e[0],
                  self.y + r * n[1] + (L + self.f2_power) * e[1])])

        screen.blit(gun_im, (self.x - 75, self.y - 30))

    def power_up(self):
        """функция, отвечающая за смену цвета и длины пушки"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:

    def __init__(self):
        self.points = 0
        self.new_target()
        self.live = 1

    def new_target(self):
        """ Инициализация цветочка"""
        self.x = randint(150, 730)
        self.y = randint(25, 300)
        self.r = randint(7, 25)
        self.color = RED
        self.v = randint(3, 10)
        self.live = 1

    def move(self):
        """Функция, отвечающая за движение цветочка по прямой и его отражение от стен"""
        self.x += self.v
        if (self.x + self.v + self.r >= 750) or (self.x + self.v - self.r <= 20):
            self.v *= -1

    def hit(self, points=1):
        """Попадание шарика в цветочек."""
        self.points += points

    def draw(self):
        """Рисует цветочек"""
        global roze
        roze1 = pygame.transform.scale(roze, (5 * self.r, 4 * self.r))
        screen.blit(roze1, (self.x - 2.5 * self.r, self.y - 2 * self.r))

    def count(self):
        """Выводит во время игры количество попаданий в цветочек"""
        counter = f.render(f'{target.points}', True, BLACK)
        screen.blit(counter, (30, 20))
        screen.blit(pygame.transform.scale(roze, (25, 25)), (5, 15))


class Fly:

    def __init__(self):
        self.points = 0
        self.new_target()
        self.live = 1

    def new_target(self):
        """ Инициализация мухи """
        self.x = randint(300, 600)
        self.y = randint(150, 350)
        self.r = randint(20, 25)
        self.R = randint(150, 250)  # Радиус кривизны траектории мухи
        self.color = BLUE
        self.v = randint(20, 25)
        self.alpha = random() * np.pi * 2
        self.live = 1

    def move(self):
        """Функция, отвечающая за движение по окружности и отражение от стен"""
        self.vx = self.v * math.cos(self.alpha)
        self.vy = self.v * math.sin(self.alpha)
        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.vx + self.r >= 800) or (self.x + self.vx - self.r <= 20):
            self.alpha = 3.14 - self.alpha
        if (self.y - self.vy + self.r >= 400) or (self.y - self.vy - self.r <= 10):
            self.alpha *= -1
        self.alpha += abs(self.v / self.R)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """Рисует цель"""
        global muxa
        muxa1 = pygame.transform.scale(muxa, (5 * self.r, 4 * self.r))
        screen.blit(muxa1, (self.x - 2.6 * self.r, self.y - 2 * self.r))

    def count(self):
        """Выводит во время игры количество попаданий в муху"""
        counter = f.render(f'{fly.points}', True, BLACK)
        screen.blit(counter, (60, 20))
        screen.blit(pygame.transform.scale(muxa, (25, 25)), (35, 15))


class Star:

    def __init__(self, obj):
        self.number = 100  # Количество звёздочек
        self.stars_vx = []
        self.stars_vy = []
        self.stars_x = []
        self.stars_y = []
        for i in range(self.number):
            self.stars_vx.append(randint(-50, 50) / 10)
            self.stars_vy.append(random() * 7)
            # задаются начальные координаты, чтобы звёздочки вылетали из цветочка.
            # obj - target, то есть цветочек.
            self.stars_x.append(obj.x)
            self.stars_y.append(obj.y)

    def move(self):
        for i in range(self.number):
            self.stars_vy[i] -= 3 / FPS
            self.stars_x[i] += self.stars_vx[i]
            self.stars_y[i] -= self.stars_vy[i]

    def draw(self):
        for i in range(self.number):
            screen.blit(im, (self.stars_x[i], self.stars_y[i]))


def new_game():
    """Обнуляет результаты после попадания во все цели"""
    global gun, target, fly, balls, bullet, timer, keys, star, flag_star
    gun = Gun(screen)
    target = Target()
    # star = Star(target)
    fly = Fly()
    target.new_target()
    fly.new_target()
    balls = []
    bullet = 0  # Счётчик выпущенных шариков
    timer = 0
    flag_star = 0  # Флаг для запуска анимации выпадения звёздочек. Опускается при новой игре


pygame.init()
clock = pygame.time.Clock()
finished = False
new_game()
# Начало основного цикла:
while not finished:
    screen.fill(WHITE)
    # Удерживает на экране надпись после каждой игры в течение 5-ти секунд:
    if not target.live and not fly.live and (timer <= 5):
        timer += 1 / FPS
        text = f.render('Вы попали в цели за ' + str(bullet) + ' выстрелов', True, BLACK)
        screen.blit(text, (250, 200))
    # Начинает новую игру:
    elif not target.live and not fly.live and (timer > 5):
        new_game()
    ''' Часть, связанная с анимацией и рисованием всех объектов '''
    gun.draw()
    gun.move()
    if flag_star:
        star.draw()
        star.move()
    for b in balls:
        b.draw()
        b.move()
    # Вывод счётчика попаданий:
    target.count()
    fly.count()
    if target.live:
        target.draw()
        target.move()
    if fly.live:
        fly.draw()
        fly.move()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        # Проверяет, не должен ли мяч исчезнуть:
        if b.live < 0:
            balls.remove(b)
        # Срабатывает при первом попадании в цель,
        # тут же её убирает и в случае с цветочком поднимает флаг для анимации звёздочек:
        if b.hittest(target) and target.live:
            star = Star(target)
            flag_star = 1
            target.live = 0
            target.hit()
        if b.hittest(fly) and fly.live:
            fly.live = 0
            fly.hit()

    gun.power_up()

pygame.quit()
