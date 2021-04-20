from game_engine import *
import socket_communication as sc
import pygame as pg
import pg_textinput as pt
from threading import Thread, Event


def main():
    field = GameField(SCREEN_HEIGHT, SCREEN_WIDTH)


    # Создание кнопок
    approve_button = Button(field.screen, 'approve', 5, 0, 40, 65, (0, 0, 0), 0, 0)
    start_game_button = Button(field.screen, 'start the game', 6, 0, 70)
    enter_ip_button = Button(field.screen, 'connect by id', 1, 0, 170)
    take_file_button = Button(field.screen, 'Take it from the file', 3, 0, 420)
    menu_button = Button(field.screen, 'menu', 0, 30, 30, font_size=35)
    reenter_button = Button(field.screen, 'reenter nick and host', 4, 0, 520)


    stage = 0
    clock = pg.time.Clock()
    tinput1 = pt.TextInput(font_size=75, font_family='Other\\Unicephalon.ttf', max_string_length=10)
    tinput2 = pt.TextInput(font_size=75, font_family='Other\\Unicephalon.ttf', max_string_length=15)

    while True:

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


        # Ввод ника и хоста
        try:
            enterinput *= 1
        except:
            enterinput = 0
        accept_result = 2
        isthread = True
        while stage == 1:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    try:
                        del thread
                    except: pass
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    enterinput += 1
                    if enterinput == 1:
                        nick = tinput1.get_text()
                        del tinput1
                    if enterinput == 2:
                        host = tinput2.get_text()
                        del tinput2
                if event.type == pg.MOUSEBUTTONDOWN:
                    stage = take_file_button.check(event.button, stage)
                    stage = menu_button.check(event.button, stage)
                    stage = reenter_button.check(event.button, stage)



            field.screen.fill((150, 0, 100))
            draw_inputs(field.screen)

            if enterinput == 0:
                tinput1.update(events)
                field.screen.blit(tinput1.get_surface(), (668, 202))
                try:
                    print_text(field.screen, host, 668, 302, font_size=75)
                except: pass
            if enterinput == 1:
                print_text(field.screen, nick, 668, 202, font_size=75)
                tinput2.update(events)
                field.screen.blit(tinput2.get_surface(), (668, 302))

            if enterinput > 1:
                print_text(field.screen, nick, 668, 202, font_size=75)
                print_text(field.screen, host, 668, 302, font_size=75)
                if accept_result == 2:
                    print_text(field.screen, "Waiting for the opponent...", 0, 620, font_size=65)
                elif accept_result:
                    print_text(field.screen, "success connection to server", 0, 620, font_size=65)
                else:
                    print_text(field.screen, "retry to connect", 0, 620, font_size=65)
                write_to_files(nick, host)

                if isthread:
                    isthread = False
                    threadevent = Event()
                    threadevent.clear()
                    ans = [None, None]
                    thread = Thread(target=sc.match, args=(host, nick, threadevent, ans))
                    thread.start()
                if not isthread:
                    if threadevent.is_set():
                        thread.join()
                        accept_result = ans[0]
                        if accept_result:
                            stage = 6


            if stage == 3:
                stage = 1
                try:
                    with open('D:\\PycharmProjects\\SeaBattle\\Other\\nick.txt', 'r') as f:
                        nick = f.readline()[:-1]
                    with open('D:\\PycharmProjects\\SeaBattle\\Other\\host.txt', 'r') as f:
                        host = f.readline()[:-1]

                    if nick == '' or host == '':
                        print_text(field.screen, "files are empty", 0, 600, font_size=65)
                    else:
                        tinput1.input_string = nick
                        tinput1.cursor_position = len(nick)
                        tinput2.input_string = host
                        tinput2.cursor_position = len(host)
                        enterinput = 0
                except:
                    pass

            menu_button.update_draw()
            take_file_button.update_draw()
            reenter_button.update_draw()
            pg.display.flip()
            clock.tick(30)


        if stage == 4:
            stage = 1
            enterinput = 0
            tinput1 = pt.TextInput(font_size=75, font_family='Other\\Unicephalon.ttf', max_string_length=10)
            tinput2 = pt.TextInput(font_size=75, font_family='Other\\Unicephalon.ttf', max_string_length=15)

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
                oppname = ans[1]
                print_text(field.screen, f'enemy: {ans[1]}', 0, 680, font_size=25)
            except: pass
            try:
                if add_ships_message:
                    print_text(field.screen, 'add ships', 0, 630, font_size=30, font_color=(255, 0, 0))
            except: pass

            try:
                if not isdead:
                    field.screen.blit(ship.image, (ship.rect.x, ship.rect.y))
            except: pass
            pg.display.flip()
            clock.tick(30)

        # Бой
        if stage == 5:
            if sum(ship_quant):
                stage = 6
                add_ships_message = True
            else:
                # ship_map.transpose()
                add_ships_message = False
                threadevent = Event()
                threadevent.clear()
                ans = [False, None, None] #Наносит удар (False-нет, True-да, 2 - ждёт ответ ), координаты удара, результат удара
                thread = Thread(target=sc.start, args=(ans, threadevent, animate))
                thread.start()

        while stage == 5:
            # print('ans ', ans)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    threadevent.set()
                    del thread
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN and ans[0] == 1:
                    ans[1] = check_bomb_position(event.pos)
                    if ans[1] is not None:
                        ans[0] = 2



            field.draw_static(0)
            # if ans[2] is not None:
            #     animate(ans)
            #     ans[2] = None
            if ans[0]:
                print_text(field.screen, 'ur turn', 0, 630, font_size=30, font_color=(255, 0, 0))
            ships.draw(field.screen)
            draw_marks(field.screen)
            print_text(field.screen, f'enemy: {oppname}', 0, 680, font_size=25)
            if ans[0] == 3:
                print_text(field.screen, f'you win', 0, 100, font_size=40)
            elif ans[0] == 4:
                print_text(field.screen, f'you lose', 0, 100, font_size=40)
            pg.display.flip()
            clock.tick(30)



if __name__ == '__main__':
    main()