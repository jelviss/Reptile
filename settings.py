#-*- coding:utf-8 -*-
import os
from celery.schedules import crontab
from datetime import timedelta
APP_NAME = 'ttsprider'

HOST = '0.0.0.0'
PORT = 9999
DEBUG = True

EMAIL_SENDER = 'hyqhyq2012123@163.com'
EMAIL_SUBJECT = u'火车票信息'
EMAIL_SUBJECT_DJ = u'恭喜订阅成功_火车票信息'
EMAIL_SMTPSERVER = 'smtp.163.com'
EMAIL_USERNAME = 'hyqhyq2012123@163.com'
EMAIL_PASSWORD = 'xxx'

DBHOST = '127.0.0.1'
DBPORT = 6379
DBID = 0

SECRET_KEY= 'rv6fc05ulvyqpcc='

#Celery
CELERY_BROKER_URL = 'redis://localhost:6379/5'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYBEAT_SCHEDULE = { 
    'on-9am': {
    'task': 'ttsprider.celerys.celery.sendEmail',
    'schedule': timedelta(seconds=5),
    'args': (),
    },
}
