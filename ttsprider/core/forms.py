# -*- coding:utf-8 -*-
import sys
reload(sys)
#默认是ascii，解码中文会报错， 设置为utf-8即可
sys.setdefaultencoding('utf-8')

from flask_wtf import FlaskForm
from wtforms import TextField, StringField, validators, SubmitField, SelectField, DateTimeField, PasswordField
from validate import date_validate, station_validate

class indexSubmitForm(FlaskForm):
    '''
    提交查询任务的表单
    '''
    email = TextField(u'邮箱', [validators.Email(message=u"邮箱格式不正确"),validators.required()])
    fromstation = TextField(u'出发站', [validators.required()])
    tostation = TextField(u'目的站', [validators.required()])
    date = TextField(u'发车日期', [date_validate, validators.required()])
    noticetime = SelectField(u'通知时间', choices=[('9am', u'9:00'),
                                                   ('11am', u'11:00'),
                                                   ('3pm', u'15:00'),
                                                   ('5pm', u'17:00')])
    purposecode = SelectField(u'种类', choices=[('0X00', u'学生票'),
                                               ('ADULT', u'成人票')])
    submit = SubmitField('提交')

class loginForm(FlaskForm):
    '''
    登录表单
    '''
    stuid = TextField(u'账号', [validators.required()])
    pwd = PasswordField(u'密码', [validators.required()])
    submit = SubmitField('登录')

