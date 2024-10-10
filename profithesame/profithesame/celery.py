import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profithesame.settings')

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

app = Celery('profithesame')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
