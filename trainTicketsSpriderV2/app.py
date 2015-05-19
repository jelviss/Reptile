# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask.ext.wtf import Form
from wtforms import TextField, StringField, validators, SubmitField, SelectField, DateTimeField
from wtforms.validators import ValidationError
from flask.ext.bootstrap import Bootstrap
from flask import flash
from rq_dashboard import RQDashboard
from rq import Queue
from redis import Redis
import time
import datetime
from trainTicketsSprider import getandsend
from ConfigParser import ConfigParser
import sys
import re
import os
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rv6fc05ulvyqpcc='
parse = ConfigParser()
config_path = os.path.split(os.path.realpath(__file__))[0]
config_file = os.path.join(config_path, 'ttsprider.conf')
parse.read(config_file)
r = Redis(host=parse.get("redis_db", "host"), port=parse.get("redis_db", "port"), db=parse.get("redis_db", "name"))
Bootstrap(app)
RQDashboard(app)

'''
表单相关
'''
def station_validate(form, field):  
    '''表单tostation和tostation验证函数'''
    if len(field.data) != 3:  
        raise ValidationError(u'未完成') 

def date_validate(form, field):
    '''表单date验证函数'''
    date = field.data.split('-')
    try:
        y = int(date[0])
        m = int(date[1])
        d = int(date[2])
        datetime.date(y,m,d)
    except:
        raise ValidationError(u'发车日期格式不正确。格式如:2012-02-02') 


class indexSubmitForm(Form):
    email = TextField(u'邮箱', [validators.Email(message=u"邮箱格式不正确"),validators.required()])
    fromstation = TextField(u'出发站', [station_validate, validators.required()])
    tostation = TextField(u'目的站', [station_validate, validators.required()])
    date = TextField(u'发车日期', [date_validate, validators.required()])
    noticetime = SelectField(u'通知时间', choices=[('9am', u'上午一二节课之间'),
                                                    ('11am', u'上午三四节课之间'),
                                                    ('3pm', u'下午一二节课之间'),
                                                    ('5pm', u'下午三四节课之间')],)
    purposecode = SelectField(u'种类', choices=[('0X00', u'学生票'),
                                               ('ADULT', u'成人票')]
                                               )
    submit = SubmitField('提交')

    

'''
请求处理
'''

@app.route("/", methods=['GET','POST'])
def index():
    res = r.zrevrange('email_que_set_all', 0, 14)
    form = indexSubmitForm(request.form)
    args = []
    for y in res:
        args.append(eval(y))   
    #if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        '''获取表单参数'''
        receiver = form.email.data
        to_station = form.tostation.data
        from_station = form.fromstation.data
        querydate = form.date.data
        purpose_code = form.purposecode.data
        publishtime =  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        noticetime = form.noticetime.data
        save_to_redis(receiver, to_station, from_station, querydate, purpose_code, noticetime, publishtime)        
        '''将提交的信息立即加入rq队列'''
        append_que(getandsend, purpose_code, querydate, from_station, to_station ,parse.get("email", "smtpserver"), parse.get("email", "sender"), receiver, parse.get("email", "username"), parse.get("email", "password"), parse.get("email", "subject_dj"))
        #TODO:判断提交是否成功
        if True:
            flash(u'提交成功')
            return redirect('/')
    return render_template('index.html', args=args, form=form)


@app.route("/del/<int:uid>/<string:noticetime>", methods=['GET'])
def del_email(uid, noticetime):
    del_quename = ['email_que_set_',noticetime]
    #暂时这样
    del_success_fromall = r.zremrangebyscore('email_que_set_all', uid, uid)
    del_success_fromque = r.zremrangebyscore(''.join(del_quename), uid, uid)
    if del_success_fromall and del_success_fromque:
        return redirect('/')
    else:
        return 'fail'


@app.route("/fm")
def station_name():
    return render_template('station.json')


@app.route("/login")
def login():
    return render_template('login.html')

'''
辅助函数
'''
def append_que(func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject):
    '''将爬虫任务加入rq队列'''
    q = Queue(connection=Redis())
    result = q.enqueue(
      func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
    )


def save_to_redis(receiver, to_station, from_station, querydate, purpose_code, noticetime, publishtime):
    '''将需要抓取的信息存入redis'''
    uid = r.incr('uid')
    tickets_info = {'uid':uid, 'receiver':receiver, 'to_station':to_station, 'from_station':from_station, 'querydate':querydate, 'purpose_code':purpose_code, 'noticetime':noticetime, 'publishtime': publishtime}
    r.zadd('email_que_set_all', str(tickets_info), uid)
    if noticetime == '9am':
        r.zadd('email_que_set_9am', str(tickets_info), uid)
    elif noticetime == '11am':
        r.zadd('email_que_set_11am', str(tickets_info), uid)
    elif noticetime == '3pm':
        r.zadd('email_que_set_3pm', str(tickets_info), uid)
    elif noticetime == '5pm':
        r.zadd('email_que_set_5pm', str(tickets_info), uid)
    r.save()


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=9999)
