from celery import Celery

def create_celery(app_name = __name__):
    redis_uri = "redis://redis:6379/0"
    return Celery(app_name, backend=redis_uri, broker=redis_uri, include=['project.celery.celery_wrappers'])


celery = create_celery()
