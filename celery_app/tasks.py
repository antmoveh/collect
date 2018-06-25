from celery import Celery

broker = 'redis_apply://172.30.221.158:6379/5'
backend = 'redis_apply://172.30.221.158:6379/6'


app = Celery('tasks', broker=broker, backend=backend)


@app.task
def add(x, y):
    return x+y
