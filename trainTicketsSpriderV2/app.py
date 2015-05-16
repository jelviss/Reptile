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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
Bootstrap(app)
RQDashboard(app)


@app.route("/")
def index():
    r = Redis(host="127.0.0.1", port=6379, db=0)
    res = r.lrange('email_que_list', 0 , 14)
    args = []
    for y in res:
        args.append(eval(y))   
    return render_template('index.html', args=args)


@app.route("/task", methods=['POST'])
def task():
    if request.method == 'POST':
        sender = 'examole@163.com'
        subject = u'火车票信息'
        smtpserver = 'smtp.163.com'
        username = 'example@163.com'
        password = 'yourpassword'
        '''获取参数'''
        publishtime =  time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        purpose_codes = request.form.get('ticketstype')
        querydate = request.form.get('date')
        from_station = request.form.get('fromstation')
        to_station = request.form.get('tostation')
        receiver = request.form.get('email')
        noticetime = request.form.get('noticetime')
        save_to_redis(receiver, to_station, from_station, querydate, purpose_codes, noticetime, publishtime)        
        append_que(getandsend, purpose_codes, querydate, from_station, to_station ,smtpserver, sender, receiver,username, password, subject)
        #return '票种:' + purpose_codes +'日期:' + querydate + '出发站:' + from_station + '目的站:' + to_station + '接受者:' + receiver
        return redirect('/')


def append_que(func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject):
    '''将爬虫任务加入rq队列'''
    q = Queue(connection=Redis())
    result = q.enqueue(
      func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
    )


def save_to_redis(receiver, to_station, from_station, querydate, purpose_codes, noticetime, publishtime):
    '''将需要爬的信息存入redis'''
    r = Redis(host="127.0.0.1", port=6379, db=0)
    uid = r.incr('uid')
    tickets_info = {'uid':uid, 'receiver':receiver, 'to_station':to_station, 'from_station':from_station, 'querydate':querydate, 'purpose_codes':purpose_codes, 'noticetime':noticetime, 'publishtime': publishtime}
    r.lpush('email_que_list', str(tickets_info))
    if noticetime == '10am':
        r.zadd('email_que_set_10am', str(tickets_info), uid)
    elif noticetime == '3pm':
        r.zadd('email_que_set_3pm', str(tickets_info), uid)
    r.save()


if __name__ == "__main__":
    app.run(debug=True)
