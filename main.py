import pygame as pg
from moduls import *
import cfg

pg.init()

screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pg.display.set_caption("Brick Breaker")

clock = pg.time.Clock()

# Sprite Groups
brick_group = pg.sprite.Group()
ball_group = pg.sprite.Group()
powerup_group = pg.sprite.Group()

game = Game(screen, brick_group, ball_group, powerup_group)

game.new_level()
game.screen("Brick Breaker", "Press any button to start...")

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(cfg.BLACK)


    # Update and draw sprite groups
    ball_group.update()
    ball_group.draw(screen)

    brick_group.update()
    for brick in brick_group:
        brick.draw(screen)

    powerup_group.update()
    powerup_group.draw(screen)

    game.update()

    pg.display.update()
    clock.tick(cfg.FPS)

pg.quit()