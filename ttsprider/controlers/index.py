#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify, current_app
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required


from ttsprider.core.forms import indexSubmitForm, loginForm
from ttsprider.core.login import User
from ttsprider.core.emails import getAndSend

from ttsprider.core.db import RedisDB
from ttsprider.core.emails import getAndSend
from settings import EMAIL_SMTPSERVER, EMAIL_SENDER, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_SUBJECT_DJ


tt_index = Blueprint('tt_index', __name__, template_folder="../templates/site")

db = RedisDB()

@tt_index.route("/", methods=['GET','POST'])
@tt_index.route("/index", methods=['GET','POST'])
def index():
    res = db.zrevrange('email_que_set_all', 0, 14) 
    form = indexSubmitForm(request.form)
    args = []
    for y in res:
        args.append(eval(y)) 
    #if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        ''' 
        获取表单参数
        '''
        receiver = form.email.data
        to_station_name = form.tostation.data
        to_station_ab = db.getStation('stationname.to.ab', to_station_name).upper()
        from_station_name = form.fromstation.data
        from_station_ab = db.getStation('stationname.to.ab', from_station_name).upper()
        query_date = '{0[0]}-{0[1]:0>2}-{0[2]:0>2}'.format(form.date.data.split('-'))
        purpose_code = form.purposecode.data
        publish_time =  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        notice_time = form.noticetime.data
        db.saveToRedis(receiver, to_station_ab, to_station_name, from_station_ab, from_station_name,
                                query_date, purpose_code, notice_time, publish_time)    

        #getAndSend(purpose_code, query_date, from_station_ab, to_station_ab, EMAIL_SMTPSERVER, EMAIL_SENDER, receiver, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_SUBJECT_DJ)
        flash(u'提交成功')
        return redirect('/')
    return render_template('index.html', args=args, form=form)

@tt_index.route("/login", methods=["GET", "POST"])
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
            return redirect(request.args.get("next") or url_for("tt_index.index"))
        else:
            flash(u'用户名或密码错误')
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@tt_index.route("/del/<int:uid>/<string:noticetime>", methods=['GET'])
@login_required
def del_email(uid, noticetime):
    del_quename = ['email_que_set_',noticetime]
    #暂时这样
    del_success_fromall = db.zremrangebyscore('email_que_set_all', uid)
    del_success_fromque = db.zremrangebyscore(''.join(del_quename), uid)
    if del_success_fromall and del_success_fromque:
        return redirect(url_for("tt_index.index"))
    else:
        return str(del_success_fromall)

@tt_index.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

