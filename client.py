from game_engine import *
import socket_communication as sc
import pygame as pg
SCREEN_HEIGHT, SCREEN_WIDTH = 750, 1875

def main():
    field = GameField(SCREEN_HEIGHT, SCREEN_WIDTH)
    field.draw_static()

    stage = 0
    clock = pg.time.Clock()

    isshipmoving = False
    while stage == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                isshipmoving, relx, rely, ship_num = field.change_ships(event.pos, event.button)
            if event.type == pg.MOUSEBUTTONUP and (event.button == 1 or event.button == 3) and isshipmoving:
                isshipmoving = False
                isdead = field.place_ship(ship_num)
                if isdead:
                    ship_quant[ship.decknum - 1] += 1
        if isshipmoving:
            ship = list(ships)[ship_num]
            ship.update(pg.mouse.get_pos(), relx, rely, field.screen)

        field.draw_static()
        ships.draw(field.screen)
        try:
            if not isdead:
                field.screen.blit(ship.image, (ship.rect.x, ship.rect.y))
        except: pass
        clock.tick(30)
        pg.display.flip()



if __name__ == '__main__':
    main()