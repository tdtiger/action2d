import pygame as pg
from pygame.locals import *

import time

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption('action2d')
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.velocity = 5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.velocity
        if keys[K_RIGHT]:
            self.rect.x += self.velocity
        if keys[K_SPACE]:
            self.rect.y -= self.velocity

player = Player()
all_sprites = pg.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()
