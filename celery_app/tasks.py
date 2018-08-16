

import time
from app import app


@app.task
def sendmail(mail):
    print('sending mail to %s ...'%mail)
    time.sleep(2)
    print('mail send.')
    return 'Send Successful!'


from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour='16', minute='58'))
def schedule_sendmail():
    print('sending mail task')
    time.sleep(2)
    print('mail send.')
    return 'Send Successful!'


@app.task
def add(x, y, queue="default"):
    return x + y



from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@app.task(bind=True)
def div(self, x, y):
    logger.info('Executing task id {0.id}, args: {0.args!r}'
                'kwargs: {0.kwargs!r}'.format(self.request))
    try:
        result = x / y
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return result
