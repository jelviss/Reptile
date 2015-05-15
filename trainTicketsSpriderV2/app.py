# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask.ext.bootstrap import Bootstrap

from rq_dashboard import RQDashboard
from rq import Queue

from redis import Redis
from trainTicketsSprider import getandsend
import time
import cPickle

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
Bootstrap(app)
RQDashboard(app)

@app.route("/")
def index():
    r = Redis(host="127.0.0.1", port=6379, db=0)
    res = r.lrange('email_que', 0 , 10)
    args = []
    for y in res:
        args.append(eval(y))   
    return render_template('index.html', args=args)


@app.route("/task", methods=['POST'])
def task():
    if request.method == 'POST':

        sender = 'example@163.com'
        subject = u'火车票信息'
        smtpserver = 'smtp.163.com'
        username = 'examole@163.com'
        password = 'yourpassword'

        purpose_codes = request.form.get('ticketstype')
        queryDate = request.form.get('date')
        from_station = request.form.get('fromstation')
        to_station = request.form.get('tostation')
        receiver = request.form.get('email')

        r = Redis(host="127.0.0.1", port=6379, db=0)
        tickets_info = {'receiver':receiver, 'to_station':to_station, 'from_station':from_station, 'queryDate':queryDate, 'purpose_codes':purpose_codes}
        r.lpush('email_que', str(tickets_info))
        r.save()
        
        q = Queue(connection=Redis())
        result = q.enqueue(
          getandsend, purpose_codes, queryDate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
        )

        #return '票种:' + purpose_codes +'日期:' + queryDate + '出发站:' + from_station + '目的站:' + to_station + '接受者:' + receiver
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
