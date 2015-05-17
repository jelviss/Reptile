# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from rq_dashboard import RQDashboard
from rq import Queue
from redis import Redis
import time
from trainTicketsSprider import getandsend
from ConfigParser import ConfigParser
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
parse = ConfigParser()
config_path = os.path.split(os.path.realpath(__file__))[0]
config_file = os.path.join(config_path, 'ttsprider.conf')
parse.read(config_file)
r = Redis(host=parse.get("redis_db", "host"), port=parse.get("redis_db", "port"), db=parse.get("redis_db", "name"))
Bootstrap(app)
RQDashboard(app)


@app.route("/")
def index():
    res = r.zrevrange('email_que_set_all', 0, 14)
    args = []
    for y in res:
        args.append(eval(y))   
    return render_template('index.html', args=args)


@app.route("/task", methods=['POST'])
def task():
    if request.method == 'POST':
        '''获取POST参数'''
        publishtime =  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        purpose_codes = request.form.get('ticketstype')
        querydate = request.form.get('date')
        from_station = request.form.get('fromstation')
        to_station = request.form.get('tostation')
        receiver = request.form.get('email')
        noticetime = request.form.get('noticetime')
        save_to_redis(receiver, to_station, from_station, querydate, purpose_codes, noticetime, publishtime)        
        '''将提交的信息立即加入rq队列'''
        append_que(getandsend, purpose_codes, querydate, from_station, to_station ,parse.get("email", "smtpserver"), parse.get("email", "sender"), receiver, parse.get("email", "username"), parse.get("email", "password"), parse.get("email", "subject"))
        return redirect('/')


@app.route("/del/<int:uid>/<string:noticetime>", methods=['GET'])
def del_email(uid, noticetime):
    del_quename = ['email_que_set_',noticetime]
    #暂时这样
    del_success_fromall = r.zremrangebyscore('email_que_set_all', uid-1, uid)
    del_success_fromque = r.zremrangebyscore(''.join(del_quename), uid-1, uid)
    if del_success_fromall and del_success_fromque:
        return redirect('/')
    else:
        return 'fail'


def append_que(func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject):
    '''将爬虫任务加入rq队列'''
    q = Queue(connection=Redis())
    result = q.enqueue(
      func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
    )


def save_to_redis(receiver, to_station, from_station, querydate, purpose_codes, noticetime, publishtime):
    '''将需要抓取的信息存入redis'''
    uid = r.incr('uid')
    tickets_info = {'uid':uid, 'receiver':receiver, 'to_station':to_station, 'from_station':from_station, 'querydate':querydate, 'purpose_codes':purpose_codes, 'noticetime':noticetime, 'publishtime': publishtime}
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
