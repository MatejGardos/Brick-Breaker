import pygame as pg
import random
import cfg

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y


        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.speed = 3

        self.image = pg.image.load("images/golf_ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.dx*self.speed
        self.rect.y += self.dy*self.speed

        if self.rect.top < 0:
            self.dy = -1 * self.dy
            self.rect.top = 1 
        if self.rect.left < 0:
            self.dx = -1 * self.dx
            self.rect.left = 1
        if self.rect.right > cfg.WIDTH:
            self.dx = -1 * self.dx
            self.rect.right = cfg.WIDTH - 1

        if self.rect.top > cfg.HEIGHT:
            self.kill()