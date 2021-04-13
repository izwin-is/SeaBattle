import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8888))
sock.listen(2)

print('[ Server is serving ]')
gamers = dict()
for i in range(2):
    try:
        client, addr = sock.accept()
        result = client.recv(1024)
        gamers[i] = [addr, result]
    except KeyboardInterrupt:
        sock.close()
        break

sock.sendto(gamers[0][1], gamers[1][0])
sock.sendto(gamers[1][0], gamers[0][1])
