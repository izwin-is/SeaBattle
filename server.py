import socket
from random import randint
from threading import Thread

def another(i):
    return int(not i)

def waitreadyness(s, n):
    s[n].recv(16)

def end_serv():
    sock.close()
    quit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9999))
sock.listen(2)

while True:
    try:
        clients = [None, None]
        names = [None, None]
        client, _ = sock.accept()
        clients[0] = client
        name = client.recv(1024)
        names[0] = name

        client, _ = sock.accept()
        clients[1] = client
        name = client.recv(1024)
        names[1] = name

        clients[0].send(names[1])
        clients[1].send(names[0])
    except:
        exit()

    # Понять, что корабли расставлены

    thread = Thread(target=waitreadyness, args=(clients, 0))
    thread.start()
    waitreadyness(clients, 1)
    thread.join()
    clients[0].send(b'0')
    clients[1].send(b'0')


    # Игра
    moving_player = randint(0, 1)
    moving_player = 0
    clients[moving_player].send(b'1')
    clients[another(moving_player)].send(b'0')

    while True:

        coords = clients[moving_player].recv(1024)
        if coords == b'end':
            clients[moving_player].close()
            clients[another(moving_player)].close()
            break

        clients[another(moving_player)].send(coords)
        bomb_result = clients[another(moving_player)].recv(1024)
        clients[moving_player].send(bomb_result)
        if bomb_result == b'2':
            frame = clients[another(moving_player)].recv(1024)
            clients[moving_player].send(frame)
        if not int(bomb_result):
            moving_player = another(moving_player)



# sock.close()