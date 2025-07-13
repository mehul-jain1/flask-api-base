from app import celery
from app.celery_utils import init_celery
from app.factory import create_app

app = create_app()
init_celery(celery, app)
