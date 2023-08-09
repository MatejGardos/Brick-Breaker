import pygame as pg
import cfg

class Brick(pg.sprite.Sprite):
    def __init__(self, x, y, health, brick_group):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.brick_group = brick_group

        if self.health == 1: self.color = cfg.GREEN
        elif self.health == 2: self.color = cfg.YELLOW
        elif self.health == 3: self.color = cfg.RED
        else: self.color = cfg.PURPLE

        self.width = 95
        self.height = 45

        self.rect = pg.rect.Rect(self.x, self.y, self.width, self.height)

        self.brick_group.add(self)

    def update(self):
        if self.health == 1: self.color = cfg.GREEN
        elif self.health == 2: self.color = cfg.YELLOW
        elif self.health == 3: self.color = cfg.RED
        else: self.color = cfg.PURPLE

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)