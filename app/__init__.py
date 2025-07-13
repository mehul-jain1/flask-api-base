from celery import Celery

from config import Config


def make_celery(app_name=__name__):
    backend = Config.CELERY_RESULT_BACKEND
    broker = Config.CELERY_BROKER_URL
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()
