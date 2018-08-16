
import time
#from server import sendmail, add
from tasks import sendmail

print(sendmail.delay('celery@python.org'))

answer = sendmail.delay('windard@windard.com')

while 1:
    print('wait for ready')
    if answer.ready():
        break
    time.sleep(0.5)

print(answer.get())


# task queue
result = add.apply_async((1, 2), routing_key='task.add')
result = add.apply_async(args=(1, 2), queue="default")

# expires 
add.apply_async((1, 2), expires=10)

# group 
from celery import group

res = group(add.s(i,i) for i in range(10))()
res.get()

return: [......]

# chain
from celery import chain

res = chain(add.s(2, 2), add.s(4), add.s(8))()
res.get(timeout=1)

# Effect of equivalent

c2 = (add.s(4, 16)|mul.s(2)|(add.s(4)|mul.s(8)))()
