#encoding=utf8

from socket import *
from subprocess import Popen, PIPE
import time
import socketserver


class MyServer:

    def __init__(self):
        self.sock = None
        self.conn = None
        self.buffsize = 1024
        self.filename = 'rjgc.xlsx'

    def startServer(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind(('127.0.0.1', 8001))
            self.sock.listen(1)
            while True:
                self.conn, addr = self.sock.accept()
                try:
                    self.conn.settimeout(5)
                    secs = self.conn.recv(1024).decode()
                    if secs.isdigit():
                        res = self.startMonitor(secs)
                        self.conn.send(res.encode())
                        if res == '0':
                            time.sleep(2)
                            f = open('F:\\性能指标收集.xlsx', 'rb')
                            while True:
                                data = f.read(4096)
                                if not data:
                                    break
                                self.conn.sendall(data)
                            f.close()
                            self.conn.send('5'.encode())
                            # with open('F:\\rjgc.xlsx', 'rb') as f:
                            #     for data in f:
                            #         self.conn.send(data)
                    else:
                        self.conn.send('3'.encode())
                except Exception as e:
                    print(e)
                self.conn.close()
        except:
            self.sock.close()

    def startMonitor(self, sesc):
        shell = ['sudo', '/data/nmon/nmon', '-f', '-s', '30', '-c', str(round(int(sesc)/30))]
        err = ''
#        output, err = Popen(shell, stdout = PIPE, stderr = PIPE).communicate()
        if len(err) > 0:
            return '1'
        else:
            return '0'

if __name__ == '__main__':
    ms = MyServer()
    ms.startServer()

