import pygame as pg
import random, sys
import cfg
from .bricks import Brick
from .ball import Ball
from . powerups import Powerup

class Game:
    def __init__(self, surface, brick_group, ball_group, powerup_group):
        self.surface = surface
        self.brick_group = brick_group
        self.ball_group = ball_group
        self.powerup_group = powerup_group
        self.font = pg.font.Font("simkai.ttf", 32)

        self.level = 1

        self.player_x = cfg.WIDTH//2
        self.player_y = cfg.HEIGHT - 30
        self.player_width = 100
        self.player_rect = pg.rect.Rect(self.player_x-50, self.player_y, self.player_width, 10)
        self.player_speed = 5
        self.double_width = False
        self.powerup_time = pg.time.get_ticks()

    def update(self):
        self.player()
        self.check_collisions()
        self.level_completed()
        self.game_over()

    def player(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.player_rect.left = max(self.player_rect.left - self.player_speed, 0) 
        if keys[pg.K_RIGHT]:
            self.player_rect.right = min(self.player_rect.right + self.player_speed, cfg.WIDTH) 

        if self.double_width:
            if pg.time.get_ticks() - self.powerup_time > 10000:
                self.player_rect = pg.rect.Rect(self.player_rect.centerx-50, self.player_rect.y, self.player_width, 10)
                self.double_width = False

        pg.draw.rect(self.surface, cfg.WHITE, self.player_rect)

    def check_collisions(self):
        # player and ball
        for ball in self.ball_group:
            if self.player_rect.colliderect(ball):
                ball.dy = -1 * ball.dy
                ball.dx += random.randint(-10, 10)/100
                ball.rect.bottom = self.player_rect.top

        # ball and brick
        collision_dict = pg.sprite.groupcollide(self.ball_group, self.brick_group, False, False)
        if collision_dict:
            for bricks in collision_dict.values():
                for brick in bricks:                       
                    if brick.health == 1:
                        brick.kill()
                        if random.randint(1,10) > 7:
                            powerup = Powerup(brick.rect.centerx, brick.rect.centery)
                            self.powerup_group.add(powerup)
                    else:
                        brick.health -= 1
                        if random.randint(1,10) > 9:
                            powerup = Powerup(brick.rect.centerx, brick.rect.centery)
                            self.powerup_group.add(powerup)

            for ball in collision_dict:
                ball.dy = -1 * ball.dy
                
        # powerup and player
        for powerup in self.powerup_group:
            if self.player_rect.colliderect(powerup):
                powerup.kill()
                if random.randint(0,1) == 0:
                    for ball in self.ball_group:
                        new_ball = Ball(ball.rect.centerx, ball.rect.centery)
                        self.ball_group.add(new_ball)
                else:
                    self.player_rect = pg.rect.Rect(self.player_rect.centerx-100, self.player_rect.y, self.player_width*2, 10)
                    self.powerup_time = pg.time.get_ticks()
                    self.double_width = True


    def new_level(self):
        self.brick_group.empty()
        self.ball_group.empty()
        self.powerup_group.empty()
        self.player_rect = pg.rect.Rect(self.player_x-50, self.player_y, self.player_width, 10)

        for y in range(4):
            self.health = max(1, self.level-y)
            for x in range(6):
                Brick(5+x*99, 5+y*50, self.health, self.brick_group)

        ball = Ball(self.player_rect.centerx, self.player_rect.top)
        self.ball_group.add(ball)

    def game_over(self):
        if len(self.ball_group) == 0:
            self.level = 1
            self.screen("Game Over", "Press any button to play again...")
            self.new_level()

    def level_completed(self):
        if len(self.brick_group) == 0:
            self.level += 1
            self.screen(f"You have passed level {self.level}", "Press any button to continue...")
            self.new_level()

    def screen(self, main_txt, sub_txt):
        paused = True
        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    paused = False

            self.surface.fill(cfg.BLACK)

            main_text = self.font.render(main_txt, True, cfg.WHITE)
            main_rect = main_text.get_rect()
            main_rect.center = (cfg.WIDTH//2, cfg.HEIGHT//2 - 20)

            sub_text = self.font.render(sub_txt, True, cfg.WHITE)
            sub_rect = sub_text.get_rect()
            sub_rect.center = (cfg.WIDTH//2, cfg.HEIGHT//2 + 20)

            self.surface.blit(main_text, main_rect)
            self.surface.blit(sub_text, sub_rect)

            pg.display.update()