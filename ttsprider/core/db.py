#-*- coding:utf-8 -*-
import os
import json
import redis
from redis import StrictRedis

class RedisDB(object):

    def __init__(self):
        if not hasattr(RedisDB, 'pool'):
            RedisDB.createPool()
        self.r = StrictRedis(connection_pool = RedisDB.pool)

    @staticmethod  
    def createPool():  
        RedisDB.pool = redis.ConnectionPool(  
        host = '127.0.0.1',  
        port = 6379,  
        db   = 0
        )

    def saveToRedis(self, receiver, to_station_ab, to_station_name, from_station_ab, from_station_name, querydate, purpose_code, noticetime, publishtime):
        '''将需要抓取的信息存入redis'''
        uid = self.r.incr('uid')    
        tickets_info = {'uid':uid, 'receiver':receiver, 'to_station_ab':to_station_ab, 'to_station_name':to_station_name, 'from_station_ab':from_station_ab,'from_station_name':from_station_name, 'querydate':querydate, 'purpose_code':purpose_code, 'noticetime':noticetime, 'publishtime': publishtime}
        self.r.zadd('email_que_set_all', uid, str(tickets_info))
        if noticetime == '9am':
            self.r.zadd('email_que_set_9am', uid, str(tickets_info))
        elif noticetime == '11am':
            self.r.zadd('email_que_set_11am', uid, str(tickets_info))
        elif noticetime == '3pm':
            self.r.zadd('email_que_set_3pm', uid, str(tickets_info))
        elif noticetime == '5pm':
            self.r.zadd('email_que_set_5pm', uid, str(tickets_info))
        self.r.save()

    def getStation(self, set, name):
        return self.r.hget(set, name)

    def zrevrange(self, set, begin, end):
        return self.r.zrevrange(set, begin, end)
    
    def zremrangebyscore(self, queue, uid):
        return self.r.zremrangebyscore(queue, uid, uid)

    def station_validate(self, form, field):  
        ''' 
        表单tostation和tostation验证函数
        '''
        if not self.r.getStation(field.data):
     
            raise ValidationError(u'木有这个站') 

    def saveJSONToSet(self, setName, json):
        if not self.r.exists(setName):
            for i, name in enumerate(json):
                self.r.hset(setName, name, json[name])
                print 'insert'+name
            self.r.save()
        else:
            pass

def stationNameInit():
    ''' 
    将车站中文名和缩写对应关系存入redis
    '''
    r = RedisDB()
    #获取车站名与拼音缩写文件路径
    station_path=os.path.split(os.path.realpath(__file__))[0]
    station_file=os.path.join(station_path, '../static/station.json')
    #将车站名与拼音缩写用json保存
    station_json = open(station_file,'r').read()
    station_json = json.loads(station_json)


    #连接redis，将站名和对应拼音存入redis
    r.saveJSONToSet('stationname.to.ab', station_json)

