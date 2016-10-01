#/usr/bin/env python
from celery import current_app    
from celery.bin import worker
from run import app

from  settings import *
application = current_app._get_current_object()
application.config_from_object('settings')

worker = worker.worker(app=application)
options = { 
    'broker': CELERY_BROKER_URL,
    'loglevel': 'INFO',
    'traceback': True,
}
worker.run(**options)
