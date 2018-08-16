
from celery import Celery
app = Celery('app', include=['tasks'])
app.config_from_object('config')
