


BROKER_URL = 'redis://172.17.43.109:6379/6'
CELERY_RESULT_BACKEND = 'redis://172.17.43.109:6379/5'
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']



CELERY_TIMEZONE = 'Asia/Shanghai'
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'send-every-30-seconds': {
        'task': 'tasks.sendmail',
        'schedule': timedelta(seconds=30),
        'args': ('windard@windard.com', )
    }
}


#from celery.schedules import crontab
#CELERYBEAT_SCHEDULE = {
#    'send-every-30-seconds': {
#        'task': 'tasks.sendmail',
#        'schedule': crontab(hour=16, minute=30),
#        'args': (dict(to='windard@windard.com'), )
#    }
#}

from kombu import Queue

CELERY_QUEUES = (
    Queue("default", routing_key='task.#'),
    Queue('web_tasks', routing_key="web.#"),
)
