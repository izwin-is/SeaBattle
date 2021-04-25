import numpy as np
from forimport import *

pg.init()
ships = pg.sprite.Group()
# marks = pg.sprite.Group()
marks = []
ship_map = np.array([[0] * 12 for _ in range(12)])
ship_quant = [4, 3, 2, 1]
myhits = []


SCREEN_HEIGHT, SCREEN_WIDTH = 750, 1875

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
            ship_map[realy:realy + deck_num, realx] = np.ones((1, deck_num))
            return True
    else:
        submat = ship_map[realy - 1:realy + 2, realx - 1:realx + deck_num + 1]
        if np.sum(submat) == 0:
            ship_map[realy, realx:realx + deck_num] = np.ones((1, deck_num))
            return True
        return False


def correct_field(x, y, deck_num, orientation):
    # add horizontal
    global ship_map
    realx = 1 + x // 75
    realy = 1 + y // 75
    if orientation == 'vertical':
        ship_map[realy:realy + deck_num, realx] = np.zeros((1, deck_num))
    else:
        ship_map[realy, realx:realx + deck_num] = np.zeros((1, deck_num))


def print_text(screen, message, x=0, y=0, font_color=(0, 0, 0), font_size=35, delta=0):
    font_type = pg.font.Font('Other\\Unicephalon.ttf', font_size)
    text = font_type.render(message, True, font_color)
    xn, yn = text.get_size()
    if x == 0:
        x = (SCREEN_WIDTH - xn) // 2
    if y == 0:
        (SCREEN_HEIGHT - yn) // 2 + delta
    screen.blit(text, (x, y))


def draw_inputs(screen):
    print_text(screen, "please enter your...", 0, 60, font_size=85)

    print_text(screen, "name", 413, 205, font_size=65)
    pg.draw.rect(screen, (0, 0, 0), (660, 194, 807, 75))
    pg.draw.rect(screen, (255, 255, 255), (666, 200, 795, 63))

    print_text(screen, "host", 413, 305, font_size=65)
    pg.draw.rect(screen, (0, 0, 0), (660, 294, 807, 75))
    pg.draw.rect(screen, (255, 255, 255), (666, 300, 795, 63))


def write_to_files(nick, host):
    with open('D:\\PycharmProjects\\SeaBattle\\Other\\nick.txt', 'w') as f:
        print(nick, file=f)
    with open('D:\\PycharmProjects\\SeaBattle\\Other\\host.txt', 'w') as f:
        print(host, file=f)



def check_bomb_position(pos):
    x, y = pos
    x //= 75
    y //= 75
    if 15 <= x <= 24:
        return [x - 14, y + 1]
    else:
        return None



def animate(ans):
    status, coords, bomb_result = ans
    x, y = coords

    if bomb_result:
        color = 255
    else:
        color = 0
    if status:
        marks.append([((x - 1) * 75 + 38 + 15 * 75, (y - 1) * 75 + 38), color])
    else:
        marks.append([((x - 1) * 75 + 38, (y - 1) * 75 + 38), color])



def draw_marks(screen):
    for mark in marks:
        pg.draw.circle(screen, (mark[1], 0, 0), mark[0], 20)



def isdeadf(x, y):
    mas = [[x, y, ship_map[x, y]]]
    for i in range(1, 4):
        if (ship_map[x + i, y] == 0 or ship_map[x + i, y] == 2) or not (1 <= x + i <= 10):
            break
        mas.append([x + i, y, ship_map[x + i, y]])
    for i in range(1, 4):
        if (ship_map[x - i, y] == 0 or ship_map[x - i, y] == 2) or not (1 <= x - i <= 10):
            break
        mas.append([x - i, y, ship_map[x - i, y]])
    for i in range(1, 4):
        if (ship_map[x, y + i] == 0 or ship_map[x, y + i] == 2) or not (1 <= y + i <= 10):
            break
        mas.append([x, y + i, ship_map[x, y + 1]])
    for i in range(1, 4):
        if (ship_map[x, y - i] == 0 or ship_map[x, y - i] == 2) or not (1 <= y - i <= 10):
            break
        mas.append([x, y - i, ship_map[x, y - 1]])
    return mas



def check_hit(coords):
    #return 0 - не попал
    #       1 - попал но не убил
    #       2 - убил

    # поле
    # 0 - не стреляли нет корабля
    # 1 - не стреляли есть корабль
    # 2 - стреляли нет корабля
    # 3 - стреляли есть корабль

    y, x = coords
    if ship_map[x, y] == 0:
        ship_map[x, y] = 2
        return 0
    else:
        if ship_map[x, y] == 1:
            ship_map[x, y] = 3
        dethmas = isdeadf(x, y)
        for i in dethmas:
            if i[2] == 1:
                return 1

        return 2


# def createpartframe(mas, status):
#     adds = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
#     x, y, _ = mas
#     for i in adds:
#         newx = x + i[0]
#         newy = y + i[1]
#         if 1 <= newx <= 10 and 1 <= newy <= 10:
#             if status:
#
#             if ship_map[newx, newy] == 0:
#
#
#

def delextra(mas):
    length = len(mas)
    i = 0
    while i < length:
        if not (1 <= mas[i][0] <= 10 and 1 <= mas[i][1] <= 10):
            del mas[i]
            length -= 1
        else:
            i += 1


def createframe(coords):
    mas = isdeadf(coords[1], coords[0])
    if len(mas) == 1:
        adds = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        x, y = mas[0][:2]
        for i in adds:
            animate([False, [y + i[1], x + i[0]], 0])
            ship_map[y + i[1], x + i[0]] = 2
        tosend = [[y + i[1], x + i[0]] for i in adds]

    else:
        if mas[0][0] == mas[1][0]:
            minimum = sorted(mas, key=lambda x: x[1])[0][1]
            constx = mas[0][0]
            length = len(mas)
            tosend = [[minimum - 1, constx], [minimum + length, constx]]
            for i in range(minimum - 1, minimum + length + 1):
                tosend.append([i, constx - 1])
                tosend.append([i, constx + 1])
        else:
            minimum = sorted(mas, key=lambda x: x[0])[0][0]
            consty = mas[0][1]
            length = len(mas)
            tosend = [[consty, minimum - 1], [consty, minimum + length]]
            for i in range(minimum - 1, minimum + length + 1):
                tosend.append([consty - 1, i])
                tosend.append([consty + 1, i])

    delextra(tosend)
    for i in tosend:
        animate([False, i, 0])
        ship_map[i[0], i[1]] = 2

    return tosend



class Ship(pg.sprite.Sprite):
    def __init__(self, decknum, x, y, orientation):
        super().__init__(ships)
        self.decknum = decknum
        if orientation == 'vertical':
            self.image = deckimages[decknum - 1]
        else:
            self.image = deckhimages[decknum - 1]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orientation = orientation
        self.cond = [None] * decknum

    def toplace(self, x, y):
        if self.orientation == 'vertical':
            self.adds = [0, 1]
        else:
            self.adds = [1, 0]
        self.rect.x = 75 * x
        self.rect.y = 75 * y
        self.cond[0] = [x + 1, y + 1, 1]
        for i in range(1, self.decknum):
            self.cond[i] = [self.cond[i - 1][0] + self.adds[0], self.cond[i - 1][1] + self.adds[1], 1]

    def update(self, pos, relx, rely, scr):
        self.rect.x = pos[0] + relx
        self.rect.y = pos[1] + rely
        # self.cond[0] = [self.rect.x // 75, self.rect.y // 75]
        # for i in range(1, self.decknum):
        #     self.cond[i] = [self.cond[0][0] + self.adds[0] * i, self.cond[0][1] + self.adds[1] * i]
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

    def change_ships(self, pos, button):
        posx, posy = pos
        if button == 1:
            orientation = 'vertical'
        else:
            orientation = 'horizontal'
        for i in range(4):
            if XS[i] * 75 <= posx <= (XS[i] + 1) * 75 and YS[i] * 75 <= posy <= (YS[i] + i + 1) * 75:
                ship_quant[i] -= 1
                print(ship_quant, ' engine')
                if orientation == 'vertical': addy = 0
                else: addy = round((posy // 75 - YS[i]) * 75) #корректировка координат для горизонтальных кораблей

                Ship(i + 1, XS[i] * 75, YS[i] * 75 + addy, orientation)
                return True, XS[i] * 75 - posx, YS[i] * 75 - posy + addy, -1

        for i, ship in enumerate(ships):
            if ship.rect.collidepoint(pos):
                correct_field(ship.rect.x, ship.rect.y, ship.decknum, ship.orientation)

                return True, ship.rect.x - posx, ship.rect.y - posy, i
        return False, -1, -1, -1

    def place_ship(self, ship_num):
        ship = list(ships)[ship_num]
        realx = round(ship.rect.x / 75)
        realy = round(ship.rect.y / 75)

        if ship.orientation == 'vertical':
            if realx < 0 or realx > 9 or realy < 0 or realy + ship.decknum - 1 > 9:
                ship.kill()
                return True
        else:
            if realx < 0 or realx + ship.decknum - 1 > 9 or realy < 0 or realy > 9:
                ship.kill()
                return True
        if check_collisions(ship.decknum, ship.orientation, realx + 1, realy + 1):
            # ship.rect.x = 75 * realx
            # ship.rect.y = 75 * realy
            ship.toplace(realx, realy)
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

    def draw_static(self, issipsdrawing=1):
        self.screen.fill((0, 60, 180))
        self.draw_net()
        if issipsdrawing:
            self.draw_static_ships()


class Button:
    # Отступы от текста до начала рамки, ширина самой рамки
    # sound = button_sound
    d = 0
    r = 2
    def __init__(self, screen, message, go_stage, x=0, y=0, font_size=65, font_color=(0, 0, 0), delta=0, longer=0):
        self.text_image = pg.font.Font('Other\\Unicephalon.ttf', font_size).render(message, True, font_color)
        self.width, self.height = self.text_image.get_size()
        self.width += 2 * (self.d + self.r + longer) # Ширина и длина кнопки
        self.height += 2 * (self.d + self.r)
        if x == 0:
            x = (SCREEN_WIDTH - self.width) // 2
        if y == 0:
            y = (SCREEN_HEIGHT - self.height) // 2 + delta
        self.x = (x, x + self.d + self.r + longer) # Координаты кнопки, самого текста
        self.y = (y, y + self.d + self.r)
        self.go_stage = go_stage
        self.font_size = font_size
        self.font_color = font_color
        self.ismouse = False
        self.screen = screen


    def update_draw(self):
        cur_x, cur_y = pg.mouse.get_pos()
        if 0 < cur_y - self.y[0] < self.height and 0 < cur_x - self.x[0] < self.width:
            pg.draw.rect(self.screen, (120, 120, 120), (self.x[0], self.y[0], self.width, self.height))
            # if not self.ismouse:
            #     self.sound.play()
            self.ismouse = True
        else:
            pg.draw.rect(self.screen, (180, 180, 180), (self.x[0],  self.y[0], self.width, self.height))
            self.ismouse = False
        pg.draw.rect(self.screen, (0, 0, 0), (self.x[0], self.y[0], self.width, self.height), self.r)
        self.screen.blit(self.text_image, (self.x[1], self.y[1] + self.height * 0.1))

    def check(self, button_code, stage):

        if self.ismouse and button_code == 1:
            return self.go_stage
        else:
            return stage



