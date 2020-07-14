
import socket

HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 客户端创建 socket
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect(ADDR)


while True:
    data = input("> ").encode()
    if not data:
        break

    clientSock.send(data)
    recData = clientSock.recv(BUFSIZE).decode()
    if not recData:
        break

    print(recData)

clientSock.close()
