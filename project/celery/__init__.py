from celery import Celery
from config import Constants

def create_celery(app_name=__name__):
    """
    Creates Celery instance used to manage model training and prediction tasks on Flask. Uses a Redis server.
    :return: Celery instance
    """
    return Celery(app_name, backend=Constants.REDIS_SERVER, broker=Constants.REDIS_SERVER, include=['project.celery.celery_wrappers'])


celery = create_celery()
