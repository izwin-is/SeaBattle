from game_engine import *
import socket_communication as sc
import pygame as pg
SCREEN_HEIGHT, SCREEN_WIDTH = 900, 1260

def main():
    field = GameField(SCREEN_HEIGHT, SCREEN_WIDTH)
    field.draw_net()
    field.draw_ships()

    stage = 0

    while stage == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    field.change_ships(event.pos)
                    print(event.pos)



if __name__ == '__main__':
    main()