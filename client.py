from game_engine import *
import socket_communication as sc
import pygame as pg
import pg_textinput as pt


def main():
    field = GameField(SCREEN_HEIGHT, SCREEN_WIDTH)


    # Создание кнопок
    approve_button = Button(field.screen, 'approve', 2, 0, 40, 65, (0, 0, 0), 0, 0)
    start_game_button = Button(field.screen, 'start the game', 1, 0, 70)
    enter_ip_button = Button(field.screen, 'connect by id', 1, 0, 170)
    take_file_button = Button(field.screen, 'Take id from the file', 3, 490, 420)


    stage = 0
    clock = pg.time.Clock()
    tinput = pt.TextInput(font_size=75, font_family='Other\\Unicephalon.ttf', max_string_length=15)

    isshipmoving = False
    # Меню
    field.screen.fill((255, 249, 70))
    while stage == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                stage = start_game_button.check(event.button, stage)
                stage = enter_ip_button.check(event.button, stage)

        start_game_button.update_draw()
        enter_ip_button.update_draw()

        clock.tick(30)
        pg.display.flip()



    # Ввод хоста
    enterinput = False
    fromfile = False
    while stage == 1:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                enterinput = True
            if event.type == pg.MOUSEBUTTONDOWN:
                stage = take_file_button.check(event.button, stage)

        tinput.update(events)
        field.screen.fill((150, 0, 100))
        print_text(field.screen, "please enter server's host", 0, 100, font_size=65)
        pg.draw.rect(field.screen, (0, 0, 0), (463, 269, 914, 89))
        pg.draw.rect(field.screen, (255, 255, 255), (469, 275, 900, 75))
        field.screen.blit(tinput.get_surface(), (469, 280))
        if enterinput:
            host = tinput.get_text()
            print_text(field.screen, "Waiting for the opponent...", 0, 600, font_size=65)
            fromfile = False
            name = 'art'
            sc.match(host, name)
            stage = 6

        take_file_button.update_draw()
        if fromfile:
            if isempty:
                print_text(field.screen, "file is empty", 0, 600, font_size=65)

        pg.display.flip()
        clock.tick(30)

        if stage == 3:
            stage = 1
            fromfile = True
            with open('Other\\host.txt', 'r') as file:
                host = file.readline()
            if host == '':
                isempty = True
            else:
                isempty = False
                tinput.input_string = host
                tinput.cursor_position = len(host)







    # place ships
    if stage == 6: field.draw_static()
    while stage == 6:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                isshipmoving, relx, rely, ship_num = field.change_ships(event.pos, event.button)
                stage = approve_button.check(event.button, stage)

            if event.type == pg.MOUSEBUTTONUP and (event.button == 1 or event.button == 3) and isshipmoving:
                isshipmoving = False
                isdead = field.place_ship(ship_num)
                if isdead:
                    ship_quant[ship.decknum - 1] += 1

        # Обновления объектов
        if isshipmoving:
            ship = list(ships)[ship_num]
            ship.update(pg.mouse.get_pos(), relx, rely, field.screen)

        field.draw_static()
        ships.draw(field.screen)

        approve_button.update_draw()

        try:
            if not isdead:
                field.screen.blit(ship.image, (ship.rect.x, ship.rect.y))
        except: pass
        pg.display.flip()
        clock.tick(30)





if __name__ == '__main__':
    main()