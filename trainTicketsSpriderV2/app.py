# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask.ext.bootstrap import Bootstrap

from rq_dashboard import RQDashboard
from rq import Queue

from redis import Redis
from trainTicketsSprider import getandsend
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
Bootstrap(app)
RQDashboard(app)

@app.route("/")
def index():
    args = None
    return render_template('index.html', args=args)


@app.route("/task", methods=['GET', 'POST'])
def task():
    if request.method == 'POST':

        purpose_codes = request.form.get('ticketstype')
        queryDate = request.form.get('date')
        from_station = request.form.get('fromstation')
        to_station = request.form.get('tostation')
        receiver = request.form.get('email')

        sender = 'example@163.com'
        subject = u'火车票信息'
        smtpserver = 'smtp.163.com'
        username = 'example@163.com'
        password = 'yourpassword'

        q = Queue(connection=Redis())
        result = q.enqueue(
          getandsend, purpose_codes, queryDate, from_station, to_station, smtpserver, sender, receiver, username, password, subject
        )

        return '票种:' + purpose_codes +'日期:' + queryDate + '出发站:' + from_station + '目的站:' + to_station + '接受者:' + receiver
    
    if request.method == 'GET':
        if request.args:
            return 'the arg is ' + request.args.get('email')
        else:
            return 'receive:nothing'
     

if __name__ == "__main__":
    app.run(debug=True)
