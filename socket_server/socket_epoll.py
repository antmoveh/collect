# 非阻塞 epoll 代理

import socket
import select

"""
对于 epoll 代理最核心的就是 events = epoll.poll(1)
该调用不需要输入观察的 socket，它是之前通过 register 来指定的。和select模式一样，这些socket都是可读可写的，通过如下代码实现：
poller.modifyepoll.register(connection.fileno(), select.EPOLLIN)
"""

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)
serversocket.setblocking(0)  # 设置为非阻塞模式

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
 connections = requests = responses = {}
 while True:
    events = epoll.poll(1)
    for fileno, event in events:
       if fileno == serversocket.fileno():
          connection, address = serversocket.accept()
          connection.setblocking(0)
          epoll.register(connection.fileno(), select.EPOLLIN)
          connections[connection.fileno()] = connection
          requests[connection.fileno()] = b''
          responses[connection.fileno()] = response
       elif event & select.EPOLLIN:
          requests[fileno] += connections[fileno].recv(1024)
          if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
             epoll.modify(fileno, select.EPOLLOUT)
             print('-'*40 + '\n' + requests[fileno].decode()[:-2])
       elif event & select.EPOLLOUT:
          byteswritten = connections[fileno].send(responses[fileno])
          responses[fileno] = responses[fileno][byteswritten:]
          if len(responses[fileno]) == 0:
             epoll.modify(fileno, 0)
             connections[fileno].shutdown(socket.SHUT_RDWR)
       elif event & select.EPOLLHUP:
          epoll.unregister(fileno)
          connections[fileno].close()
          del connections[fileno]
finally:
 epoll.unregister(serversocket.fileno())
 epoll.close()
 serversocket.close()


 """
 select模型采用遍历文件描述符的方式，限制能打开最大文件描述符1024，性能随着fd的增长线性下降
 poll和select方式相同，只是没有1024的限制
 epoll采用触发试，将socket连接注册为时间，发生读/写/异常时间时触发时间
 epoll两种触发方式（默认水平触发tornado框架也采用此模式）：
 边缘触发，调用程序必须处理与该事件相关的所有数据，后续不会发出进一步的通知，可能造成事件丢失发生异常
 水平触发，可以发起多次文件描述事件，直到被调用程序接收，不会发生异常
 epoll模型与基于事件的异步程序和注册回调函数等同等思想
 """