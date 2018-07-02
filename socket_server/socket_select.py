# 非阻塞 select 代理

from time import ctime
import socket
import select
import queue

HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 服务器端创建 socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind(ADDR)
serverSock.listen(5)

inputs = [serverSock]  # 接收服务列表
outputs = []  # 发送服务列表
timeout = 20
message_queues = {}

"""
对于 select 代理最核心的调用 readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
该调用将可读可写的socket存储到 readable 和 writable 列表中，从而我们可以直接调用这些 socket的 recv 和 send 时不会发生阻塞。
注意除了 serverSock 只读以外，其他 socket 都会存在同时存在于 inputs 和 outputs 列表中。
"""

while inputs:
    # print("doing select ...")
    # select 函数监视的文件描述符分3类，分别是writefds、readfds、和exceptfds 或者超时
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

    for s in readable:
        if s is serverSock:
            # 创建连接
            server2client_Sock, addr = serverSock.accept()
            print(" Connection from ")
            server2client_Sock.setblocking(0)
            inputs.append(server2client_Sock)
            message_queues[server2client_Sock] = queue.Queue()

        else:
            server2client_Sock = s
            # 接收数据
            data = server2client_Sock.recv(BUFSIZE).decode()

            # 如果数据接收完，则退出 recv, 进入到下一个连接
            if data:
                print("Received data from ", server2client_Sock.getpeername())
                data = "[{}] {}".format(ctime(), data).encode()
                message_queues[server2client_Sock].put(data)

                # 将建立连接的 socket 放入到可以写的 socket 列表中
                if server2client_Sock not in outputs:
                    outputs.append(server2client_Sock)
            else:
                if server2client_Sock in outputs:
                    outputs.remove(server2client_Sock)
                inputs.remove(server2client_Sock)
                server2client_Sock.close()
                del message_queues[server2client_Sock]

    if s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            print(" ", s.getpeername(), 'queue empty')
            outputs.remove(s)
        else:
            print(" sending ", next_msg, " to ", s.getpeername())
            s.send(next_msg.encode())

    for s in exceptional:
        print(" exception condition on ", s.getpeername())
        # stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        # 清除队列信息

serverSock.close()

"""
核心思想是将不同客户端socket连接存入列表，接收/发送消息存入key为socket连接的字典
这样可以处理多个不同的client连接，分别响应不同的客户端
"""