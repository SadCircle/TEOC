import os
import sys
from celery import Celery
from celery.schedules import crontab
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TEOC.settings')
hashseed = os.getenv('PYTHONHASHSEED')
if hashseed is None:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)
 
app = Celery('TEOC')
app.config_from_object('django.conf:settings',namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get-documents-every-delta': {
        'task': 'client.tasks.get_auto',
        'schedule': crontab(minute=0, hour=0),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}   

def change_download_duration(timedelta,parser_id,minute=0,hour=0):
    app.conf.beat_schedule = {
        'get-documents-every-delta': {
            'task': 'catalog.tasks.get_auto',
            'schedule': crontab(timedelta),
        },
    }





