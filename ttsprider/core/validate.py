#!/usr/bin/env python
#-*- coding:utf-8 -*-

from db import RedisDB


def station_validate(form, field):  
    ''' 
    表单tostation和tostation验证函数
    '''
    r = RedisDB()
    if not r.getStation(field.data):

        raise ValidationError(u'木有这个站') 

def date_validate(form, field):
    pass
