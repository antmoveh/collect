CELERY_RESULT_BACKEND = 'redis_apply://172.30.221.158:6379/5'
BROKER_URL = 'redis_apply://172.30.221.158:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'

#from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'proj.tasks.add',
#        'schedule': timedelta(seconds=30),
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16)
    }
}
