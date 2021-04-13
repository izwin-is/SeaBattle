import socket

def match(host, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 8888))
    sock.sendto(name.encode('utf-8'), (host, 8888))
    oppname = sock.recv(1024)
    print(oppname)
    sock.close()

a = input()
match('127.0.0.1', a)