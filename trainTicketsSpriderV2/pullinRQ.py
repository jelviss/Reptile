# /bin/env python
# -*- coding:utf-8 -*-
from redis import Redis
from rq import Queue
import sys
import os.path
from trainTicketsSprider import getandsend
from ConfigParser import ConfigParser

class pullinRQ:
    def __init__(self):
        self.parse = ConfigParser()
        config_path = os.path.split(os.path.realpath(__file__))[0]
        config_file = os.path.join(config_path, 'ttsprider.conf')
        self.parse.read(config_file)
        self.r = Redis(host=self.parse.get("redis_db", "host"), port=self.parse.get("redis_db", "port"), db=self.parse.get("redis_db", "name"))

    def append_rq_que(self, func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject): 
        self.q = Queue(connection=Redis()) 
        result = self.q.enqueue( 
          func, purpose_code, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject 
        )

    def getandpullin(self,times):
        res = self.r.zrange('email_que_set_' + times, 0 , -1)
        reslist = []
        for y in res:
            reslist.append(eval(y))

        for args in reslist:
            purpose_code = args['purpose_code']
            querydate = args['querydate']
            from_station = args['from_station']
            to_station = args['to_station']
            receiver =  args['receiver']
            self.append_rq_que(getandsend, purpose_code, querydate, from_station, to_station , self.parse.get("email", "smtpserver"), self.parse.get("email", "sender"), receiver, self.parse.get("email", "username"), self.parse.get("email", "password"), self.parse.get("email", "subject"))

cron = pullinRQ()
cron.getandpullin(sys.argv[1])
