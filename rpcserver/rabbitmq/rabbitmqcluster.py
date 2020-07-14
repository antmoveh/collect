
"""
HAProxy 以下所有的配置均在haproxy-server上面執行
安裝haproxy
yum install haproxy

配置haproxy
vim/etc/haproxy/haproxy.cfg
"""
# global
# daemon
# 
# defaults
# mode tcp
# maxconn 10000
# timeout connect 5s
# timeout client 100s
# timeout server 100s
# 
# listen rabbitmq 172.16.0.100: 5672
# mode tcp
# balance roundrobin
# server rabbit-master 172.16.0.10: 5672 check inter 5s rise 2 fall 3
# server rabbit-node1 172.16.0.11: 5672 check inter 5s rise 2 fall 3
# server rabbit-node2 172.16.0.12: 5672 check inter 5s rise 2 fall 3
"""
啟動haproxy
systemctl start haproxy
RabbitMQ Cluster Product & Consume Test
"""


# 生產者: send.py
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.0.100', port=5672))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()


# 消費者: receive.py
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.0.100', port=5672))
channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()