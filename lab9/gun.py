import math
from random import choice
from random import randint, random
import pygame
from pygame.draw import *

pygame.font.init()

FPS = 30

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


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 7

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
        self.live -= 1 / FPS

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            # obj.live = 0
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

    def fire2_start(self, event):
        """Флажок, показывающий, зажата ли мышь"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        if target.live or t.live:
            bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] == 20:
            a = 20.01
        else:
            a = event.pos[0]
        if event:
            self.an = math.atan((event.pos[1] - 450) / (a - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку"""
        pygame.draw.polygon(screen, self.color, [(40, 450),
                                                 (40 - 15 * math.sin(self.an), 450 + 15 * math.cos(self.an)),
                                                 (
                                                 40 - 15 * math.sin(self.an) + (self.f2_power + 50) * math.cos(self.an),
                                                 450 + 15 * math.cos(self.an) + (self.f2_power + 50) * math.sin(
                                                     self.an)),
                                                 (40 + (self.f2_power + 50) * math.cos(self.an),
                                                  450 + (self.f2_power + 50) * math.sin(self.an))])

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
        """ Инициализация новой цели. Красный шарик - двигается по прямой """
        self.x = randint(150, 730)
        self.y = randint(150, 430)
        self.r = randint(7, 25)
        self.color = RED
        self.v = randint(3, 15)
        self.alpha = random() * 6.28
        self.live = 1

    def move(self):
        """Функция, отвечающая за движение по прямой и отражение от стен"""
        self.vx = self.v * math.cos(self.alpha)
        self.vy = self.v * math.sin(self.alpha)
        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.vx + self.r >= 750) or (self.x + self.vx - self.r <= 20):
            self.alpha = 3.14 + self.alpha
        if (self.y + self.r >= 450) or (self.y - self.r <= 30):
            self.alpha = 3.14 + self.alpha

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        print(self.points)

    def draw(self):
        """Рисует цель"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def count(self):
        """Выводит во время игры количество попаданий в шарик в левом верхнем углу"""
        counter = f.render(f'{target.points}', True, BLACK)
        screen.blit(counter, (30, 20))
        pygame.draw.circle(screen, RED, (20, 20), 5)


class Target_:

    def __init__(self):
        self.points = 0
        self.new_target()
        self.live = 1

    def new_target(self):
        """ Инициализация новой цели. Синий шарик, двигается по окружности. """
        self.x = randint(300, 600)
        self.y = randint(150, 350)
        self.r = randint(7, 25)
        self.R = randint(20, 150)
        self.color = BLUE
        self.v = randint(3, 25)
        self.alpha = random() * 6.28
        self.live = 1

    def move(self):
        """Функция, отвечающая за движение по окружности и отражение от стен"""
        self.vx = self.v * math.cos(self.alpha)
        self.vy = self.v * math.sin(self.alpha)
        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.vx + self.r >= 800) or (self.x + self.vx - self.r <= 20):
            self.alpha = 3.14 - self.alpha
        if (self.y + self.r >= 500) or (self.y - self.r <= 10):
            self.alpha = -self.alpha
        self.alpha += abs(self.v / self.R)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """Рисует цель"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def count(self):
        """Выводит во время игры количество попаданий в шарик в левом верхнем углу"""
        counter = f.render(f'{t.points}', True, BLACK)
        screen.blit(counter, (60, 20))
        pygame.draw.circle(screen, BLUE, (50, 20), 5)


def new_game():
    """Обнуляет результаты после попадания во все шарики"""
    global gun, target, t, balls, bullet, s
    gun = Gun(screen)
    target = Target()
    t = Target_()
    target.new_target()
    t.new_target()
    balls = []
    bullet = 0
    s = 0


pygame.init()
clock = pygame.time.Clock()
finished = False
new_game()
while not finished:
    screen.fill(WHITE)
    if not target.live and not t.live and (s <= 5):
        s += 1 / FPS
        text = f.render('Вы попали в цели за ' + str(bullet) + ' выстрелов', True, BLACK)
        screen.blit(text, (250, 200)) # Удерживает на экране надпись после каждой игры в течение 5-ти секунд
    elif not target.live and not t.live and (s > 5):
        new_game() # Начинает новую игру
    gun.draw()
    for b in balls:
        b.draw()
    target.count()
    t.count()
    if target.live:
        target.draw()
        target.move()
    if t.live:
        t.draw()
        t.move()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.live < 0:
            balls.remove(b)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
        if b.hittest(t) and t.live:
            t.live = 0
            t.hit()
    gun.power_up()

pygame.quit()
