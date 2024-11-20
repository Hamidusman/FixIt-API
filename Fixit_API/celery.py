from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fixit_API.settings')

app = Celery('Fixit_API')

# Read config from Django settings, the CELERY namespace means all celery-related
# configs in Django settings must be prefixed with 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')