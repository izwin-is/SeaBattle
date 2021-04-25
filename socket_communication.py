import socket
from threading import Event
from game_engine import check_hit, myhits, createframe
from time import sleep
import pickle


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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


# def sayready(host):
#     # sock.sendto(b'r', (host, 9999))
#     pass

def start(ans, threadevent, animate_function, readyness):
    sock.send(b'r')
    sock.recv(16)
    readyness[0] = True


    moving_player = sock.recv(1024)
    ans[0] = bool(int(moving_player))
    moving_player = ans[0]
    enemysdeadships = 0
    mysdeadships = 0


    while True:
        if moving_player:
            while ans[0] != 2:
                sleep(0.2)
            if ans[1] in myhits:
                ans[0] = 1
                continue
            myhits.append(ans[1])
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
                frame = pickle.loads(sock.recv(1024))
                myhits.extend(frame)
                for hit in frame:
                    animate_function([1, hit, 0])
            else:
                ans[0] = 1
                ans[1] = None
                ans[2] = None
            if enemysdeadships == 10:
                print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeend')
                ans[0] = 3 #win
                return
        else:
            coords = sock.recv(1024)
            coords = list(map(int, coords.decode('utf-8').split(' ')))
            # print('coords', coords)
            hit_result = check_hit(coords)
            ans[1] = coords
            print('hit_result', hit_result)
            ans[2] = hit_result
            animate_function(ans)
            sock.send(str(hit_result).encode('utf-8'))
            if hit_result == 2:
                frame = pickle.dumps(createframe(coords))
                sock.send(frame)
            if not hit_result:
                moving_player = another(moving_player)
                ans[0] = 1
            elif hit_result == 2:
                mysdeadships += 1
            if mysdeadships == 10:
                ans[0] = 4 # lose
                print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeend')
                return

        if threadevent.is_set():
            print(1)
            return




