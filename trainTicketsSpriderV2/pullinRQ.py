# /bin/env python
# -*- coding:utf-8 -*-
from redis import Redis
from rq import Queue
import sys
from trainTicketsSprider import getandsend

class pullinRQ:
    def __init__(self):
        self.r = Redis(host="127.0.0.1", port=6379, db=0)

    def append_rq_que(self, func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject): 
        q = Queue(connection=Redis()) 
        result = q.enqueue( 
          func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject 
        )

    def getandpullin(self,times):
        res = self.r.zrange('email_que_set_' + times, 0 , -1)
        reslist = []
        for y in res:
            reslist.append(eval(y))

        sender = 'hyqhyq2012123@163.com'
        subject = u'火车票信息'
        smtpserver = 'smtp.163.com'
        username = 'hyqhyq2012123@163.com'
        password = 'basketbaqq'
        for args in reslist:
            purpose_codes = args['purpose_codes']
            querydate = args['querydate']
            from_station = args['from_station']
            to_station = args['to_station']
            receiver =  args['receiver']
            self.append_rq_que(getandsend, purpose_codes, querydate, from_station, to_station ,smtpserver, sender, receiver,username, password, subject)

cron = pullinRQ()
cron.getandpullin(sys.argv[1])
