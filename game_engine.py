import numpy as np
from forimport import *

pg.init()
ships = pg.sprite.Group()
ship_map = np.array([[0] * 12 for _ in range(12)])
ship_quant = [4, 3, 2, 1]

X1, Y1 = 11, 2
X2, Y2 = 13, 6
X3, Y3 = 13, 2
X4, Y4 = 11, 4
XS = (X1, X2, X3, X4)
YS = (Y1, Y2, Y3, Y4)


def check_collisions(deck_num, orient, realx, realy):
    global ship_map, ship_quant
    if ship_quant[deck_num - 1] < 0:
        return False
    if orient == 'vertical':
        submat = ship_map[realy - 1:realy + deck_num + 1, realx - 1:realx + 2]
        if np.sum(submat) == 0:
            ship_map[realy:realy + deck_num, realx] = np.ones((deck_num, 1)).ravel()
            return True
        return False

def correct_field(x, y, deck_num, orientation):
    # add horizontal
    global ship_map
    print('========')
    realx = 1 + x // 75
    realy = 1 + y // 75
    if orientation == 'vertical':
        ship_map[realy:realy + deck_num, realx] = np.zeros((deck_num, 1)).ravel()



class Ship(pg.sprite.Sprite):
    def __init__(self, decknum, x, y, orientation):
        super().__init__(ships)
        self.decknum = decknum
        self.image = deckimages[decknum - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orientation = orientation

    def update(self, pos, relx, rely, scr):
        self.rect.x = pos[0] + relx
        self.rect.y = pos[1] + rely
        # self.draw(scr)


class GameField:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        pg.display.set_caption('Sea Battle')  # Название игры
        screen = pg.display.set_mode((self.w, self.h))  # Инициаллизация экрана
        self.screen = screen
        self.screen.fill((0, 60, 180))
        # pg.display.flip()


    def draw_static_ships(self):
        self.screen.blit(deckimages[0], (X1 * 75, Y1 * 75))
        self.screen.blit(deckimages[1], (X2 * 75, Y2 * 75))
        self.screen.blit(deckimages[2], (X3 * 75, Y3 * 75))
        self.screen.blit(deckimages[3], (X4 * 75, Y4 * 75))
        # pg.display.flip()


    def change_ships(self, pos):
        posx, posy = pos
        for i in range(4):
            if XS[i] * 75 <= posx <= (XS[i] + 1) * 75 and YS[i] * 75 <= posy <= (YS[i] + i + 1) * 75:
                ship_quant[i] -= 1
                Ship(i + 1, XS[i] * 75, YS[i] * 75, 'vertical')
                return True, XS[i] * 75 - posx, YS[i] * 75 - posy, -1
        # add horizontal
        for i, ship in enumerate(ships):
            if ship.rect.x <= posx <= ship.rect.x + 75 and ship.rect.y <= posy <= ship.rect.y + 75 * ship.decknum:
                correct_field(ship.rect.x, ship.rect.y, ship.decknum, ship.orientation)

                return True, ship.rect.x - posx, ship.rect.y - posy, i
        return False, -1, -1, -1

    def place_ship(self, ship_num):
        ship = list(ships)[ship_num]
        realx = round(ship.rect.x / 75)
        realy = round(ship.rect.y / 75)
        if realx < 0 or realx > 9 or realy < 0 or realy > 9:
            ship.kill()
            return True
        if check_collisions(ship.decknum, ship.orientation, realx + 1, realy + 1):
            ship.rect.x = 75 * realx
            ship.rect.y = 75 * realy
        else:
            ship.kill()
            return True
        return False





    def draw_net(self):
        tile_size = self.h // 10
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (i * tile_size + 1, 0), (i * tile_size + 1, self.h), 3)
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (0, i * tile_size + 1), (self.h, i * tile_size + 1), 3)
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (1125 + i * tile_size + 1, 0), (1125 + i * tile_size + 1, self.h), 3)
        for i in np.arange(11):
            pg.draw.line(self.screen, (0, 0, 0), (1125 + 0, i * tile_size + 1), (1125 + self.h, i * tile_size + 1), 3)
        # pg.display.flip()

    def draw_static(self):
        self.screen.fill((0, 60, 180))
        self.draw_net()
        self.draw_static_ships()







