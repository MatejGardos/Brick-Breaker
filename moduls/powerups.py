import pygame as pg
import random
import cfg

class Powerup(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pg.transform.scale(pg.image.load("images/star.png"), (24, 24))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = random.randint(2, 5)

    def update(self):
        self.move()

    def move(self):
        self.rect.y += self.speed

        if self.rect.top > cfg.HEIGHT:
            self.kill()
