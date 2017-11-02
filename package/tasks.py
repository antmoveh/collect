from celery import Celery

broker = 'redis://172.30.221.158:6379/5'
backend = 'redis://172.30.221.158:6379/6'


app = Celery('tasks', broker=broker, backend=backend)


@app.task
def add(x, y):
    return x+y
