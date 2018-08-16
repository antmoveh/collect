

# celery -A app worker --loglevel=info

# schedule
# celery -A app worker -B -l info

# queue
# celery -A tasks worker -Q default -l info
