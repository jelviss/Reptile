#/usr/bin/env python
from celery import current_app    
from celery.bin import beat
from run import app

from  settings import *
application = current_app._get_current_object()
application.config_from_object('settings')

beat = beat.beat(app=application)
options = { 
    'broker': CELERY_BROKER_URL,
    'loglevel': 'INFO',
    'traceback': True,
}
beat.run(**options)
