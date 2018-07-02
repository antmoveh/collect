from socket import *
import time


def client():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1', 8001))
    time.sleep(1)
    sock.send('600'.encode())
    while True:
        data = sock.recv(4096)
        if data == '0':
            pass
        elif data == '1':
            pass
        else:
            if not data:
                break
            else:
                with open('E:\\m.xlsx', 'ab') as f:
                    f.write(data)

    # data = sock.recv(1024).decode()
    # print(data)
    sock.close()

if __name__ == '__main__':
    client()