#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery
from ttsprider.core.emails import getAndSend

def init_celery(app):
    celery = Celery(app.config["APP_NAME"], broker=app.config['CELERY_BROKER_URL'])
    #celery.config_from_object('settings')
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstruct = True
        def __call__(self, *args, **keywords):
            with app.app_context():
                return TaskBase.__call__(self, *args, **keywords)

        @celery.task(name = 'ttsprider.celerys.celery.sendEmail')
        def sendEmail(): 
            #获得需要发送的信息
            return 'ok'

    celery.Task = ContextTask
    return celery
