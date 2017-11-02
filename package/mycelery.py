from celery import Celery


app = Celery('tasks', broker='redis://localhost', backend='redis://localhost')


@app.task
def send(message):
    return message


app.conf.beat_schedule = {
    "send-every-10-seconds": {
        "task": "mycelery.send",
        "schedule": 10.0,
        "args": ("Hello World", )
    }
}