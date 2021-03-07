import numpy as np
from forimport import *

pg.init()
ships = pg.sprite.Group()

class Ship(pg.sprite.Sprite):
    def __init__(self, decknum, x, y, image):
        super().__init__(ships)
        self.decknum = decknum
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GameField:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        pg.display.set_caption('Sea Battle')  # Название игры
        screen = pg.display.set_mode((self.w, self.h))  # Инициаллизация экрана
        self.screen = screen
        self.screen.fill((0, 60, 180))
        pg.display.flip()

    def draw_ships(self):
        self.screen.blit(deck2, (13 * 90, 4 * 90))
        pg.display.flip()


    def change_ships(self, pos):
        pass


    def draw_net(self):
        tile_size = self.h // 10
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (i * tile_size + 1, 0), (i * tile_size + 1, self.h), 3)
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (0, i * tile_size + 1), (self.h, i * tile_size + 1), 3)
        pg.display.flip()











# def create_ships():
#     for i in range(1, 2):
