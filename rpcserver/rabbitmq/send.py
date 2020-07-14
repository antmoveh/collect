

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.43.109'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()




# queue
channel.queue_declare(queue="task_queue", durable=True)
# info
channel.basic_publish(exchange="", routing_key="task_queue", body="hello world",
                      properties=pika.BasicProperties(delivery_mode=2,)) # make message persistent

