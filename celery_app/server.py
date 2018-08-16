
import time
from celery import Celery

app = Celery('tasks', backend='redis://172.17.43.109:6379/5', broker='redis://172.17.43.109:6379/6')

@app.task
def sendmail(mail):
    print('sending mail to %s ...'%mail)
    time.sleep(2)
    print('mail send.')
    return 'Send Successful!'

@app.task
def add(x, y):
    return x + y

