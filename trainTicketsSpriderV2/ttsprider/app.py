# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import TextField, StringField, validators, SubmitField, SelectField, DateTimeField, PasswordField
from wtforms.validators import ValidationError
from flask_bootstrap import Bootstrap
from flask import flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)
import requests
import rq_dashboard
from rq import Queue
from redis import Redis
import time
import datetime
from trainTicketsSprider import getandsend
from ConfigParser import ConfigParser
import sys
import os
from ttspriderInit import ttspriderInit
import json
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rv6fc05ulvyqpcc='
parse = ConfigParser()
config_path = os.path.split(os.path.realpath(__file__))[0]
config_file = os.path.join(config_path, 'ttsprider.conf')
parse.read(config_file)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"请先登录"
login_manager.refresh_view = "reauth"

r = Redis(host=parse.get("redis_db", "host"), port=parse.get("redis_db", "port"), db=parse.get("redis_db", "name"))
Bootstrap(app)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint)

'''
表单相关
'''
def station_validate(form, field):  
    '''表单tostation和tostation验证函数'''
    if not r.hget('stationname.to.ab', field.data):
        raise ValidationError(u'木有这个站') 

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


class indexSubmitForm(FlaskForm):
    email = TextField(u'邮箱', [validators.Email(message=u"邮箱格式不正确"),validators.required()])
    fromstation = TextField(u'出发站', [station_validate, validators.required()])
    tostation = TextField(u'目的站', [station_validate, validators.required()])
    date = TextField(u'发车日期', [date_validate, validators.required()])
    noticetime = SelectField(u'通知时间', choices=[('9am', u'9:00'),
                                                    ('11am', u'11:00'),
                                                    ('3pm', u'15:00'),
                                                    ('5pm', u'17:00')])
    purposecode = SelectField(u'种类', choices=[('0X00', u'学生票'),
                                               ('ADULT', u'成人票')]
                                               )
    submit = SubmitField('提交')

class loginForm(FlaskForm):
    stuid = TextField(u'账号', [validators.required()])
    pwd = PasswordField(u'密码', [validators.required()])
    submit = SubmitField('登录')
   

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
        to_station_name = form.tostation.data
        to_station_ab = r.hget('stationname.to.ab', to_station_name).upper()
        from_station_name = form.fromstation.data
        from_station_ab = r.hget('stationname.to.ab', from_station_name).upper()
        querydate = '{0[0]}-{0[1]:0>2}-{0[2]:0>2}'.format(form.date.data.split('-'))
        purpose_code = form.purposecode.data
        publishtime =  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        noticetime = form.noticetime.data
        save_to_redis(receiver, to_station_ab, to_station_name, from_station_ab, from_station_name,
                                querydate, purpose_code, noticetime, publishtime)        
        '''将提交的信息立即加入rq队列'''
        append_que(getandsend, purpose_code, querydate, from_station_ab, to_station_ab,parse.get("email", "smtpserver"), parse.get("email", "sender"), receiver, parse.get("email", "username"), parse.get("email", "password"), parse.get("email", "subject_dj"))
        flash(u'提交成功')
        return redirect('/')
    return render_template('index.html', args=args, form=form)


#删除登记信息
@app.route("/del/<int:uid>/<string:noticetime>", methods=['GET'])
@login_required
def del_email(uid, noticetime):
    del_quename = ['email_que_set_',noticetime]
    #暂时这样
    del_success_fromall = r.zremrangebyscore('email_que_set_all', uid, uid)
    del_success_fromque = r.zremrangebyscore(''.join(del_quename), uid, uid)
    if del_success_fromall and del_success_fromque:
        return redirect(url_for("index"))
    else:
        return 'fail'


#返回车站名与缩写json
@app.route("/fm")
def station_name():
    return render_template('station.json')


#需要登录访问的的后台
@app.route("/manager")
@login_required
def manager():
    pass


#以下为登录处理函数
class UserNotFoundError(Exception):
    pass


class User(UserMixin):
    def __init__(self, id, pwd):
        self.id = id
        self.pwd = pwd
        self.s = requests.Session()
        '''
        self.data={"username":self.id,"password":self.pwd}
        self.res1 = self.s.post('http://user.ecjtu.net/login?redirect', data=self.data)
        self.res2 = self.s.get("http://user.ecjtu.net/user")
        try:
            #json.loads(self.res2.text)
            self.isOk = False
        except:
            self.isOk = True
        '''
        if self.id=='admin' and self.pwd=='admin':
            self.isOk = True        
        else:
            self.isOK = False        
        

    @classmethod
    def get(self_class, id, pwd):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id, pwd)
        except UserNotFoundError:
            return None


@login_manager.user_loader
def load_user(id):
    return User.get(id, None)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit():
        stuid = form.stuid.data
        pwd = form.pwd.data
        user = User.get(stuid, pwd)
        if user.isOk == True:
            login_user(user)
            next = request.args.get('next')
            flash(u"登录成功")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash(u'用户名或密码错误')
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


'''
辅助函数
'''
def append_que(func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject):
    '''将爬虫任务加入rq队列'''
    q = Queue(connection=Redis())
    result = q.enqueue(
      func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
    )


def save_to_redis(receiver, to_station_ab, to_station_name, from_station_ab, from_station_name, querydate, purpose_code, noticetime, publishtime):
    '''将需要抓取的信息存入redis'''
    uid = r.incr('uid')
    tickets_info = {'uid':uid, 'receiver':receiver, 'to_station_ab':to_station_ab, 'to_station_name':to_station_name, 'from_station_ab':from_station_ab,'from_station_name':from_station_name, 'querydate':querydate, 'purpose_code':purpose_code, 'noticetime':noticetime, 'publishtime': publishtime}
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
    ttspriderInit.stationNameInit()
    app.run(debug=True, host='0.0.0.0', port=9999)
