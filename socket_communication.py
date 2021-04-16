import socket
from threading import Event
from game_engine import check_hit
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
from time import sleep

def another(i):
    return int(not i)

def match(host, nick, threadevent, ans):
    try:
        sock.connect((host, 9999))
        sock.send(nick.encode('utf-8'))
        ans[0] = True
        oppname = sock.recv(1024)
        ans[1] = oppname.decode('utf-8')
        threadevent.set()
        return
    except:
        sock.close()
        threadevent.set()
        ans[0] = True
        return


def start(ans, threadevent, animate_function):
    moving_player = sock.recv(1024)
    ans[0] = bool(int(moving_player))
    moving_player = ans[0]
    enemysdeadships = 0
    mysdeadships = 0


    while True:
        if moving_player:
            while ans[0] != 2:
                sleep(0.2)
            tosend = (str(ans[1][0]) + ' ' + str(ans[1][1])).encode('utf-8')
            sock.send(tosend)
            bomb_result = int(sock.recv(1024))
            print('bomb res', bomb_result)
            ans[2] = bomb_result
            animate_function(ans)
            if bomb_result == 0:
                moving_player = another(moving_player)
                ans[0] = 0
            elif bomb_result == 2:
                enemysdeadships += 1
            else:
                ans[0] = 1
                ans[1] = None
                ans[2] = None
            if enemysdeadships == 2:
                print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeend')
                return
        else:
            coords = sock.recv(1024)
            coords = list(map(int, coords.decode('utf-8').split(' ')))
            print('coords', coords)
            hit_result = check_hit(coords)
            ans[1] = coords
            print('hit_result', hit_result)
            ans[2] = hit_result
            animate_function(ans)
            sock.send(str(hit_result).encode('utf-8'))
            if not hit_result:
                moving_player = another(moving_player)
                ans[0] = 1
            if mysdeadships == 1:
                print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeend')
                return

        if threadevent.is_set():
            print(1)
            return




