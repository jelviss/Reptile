# coding:utf-8
import os
import json
import sys
from ConfigParser import ConfigParser
from redis import Redis
class ttspriderInit():
    '''将车站中文名和缩写对应关系存入redis'''
    @staticmethod
    def stationNameInit():
        parse = ConfigParser()
        config_path = os.path.split(os.path.realpath(__file__))[0]
        config_file = os.path.join(config_path, 'ttsprider.conf')
        parse.read(config_file)
        r = Redis(host=parse.get("redis_db", "host"), port=parse.get("redis_db", "port"), db=parse.get("redis_db", "name"))
        stationname_path=os.path.split(os.path.realpath(__file__))[0]
        stationname_file=os.path.join(stationname_path, 'static/station.json')
        stationname_json = open(stationname_file,'r').read()
        stationname_json = json.loads(stationname_json)
        if not r.exists('stationname.to.ab'):
            for i,name in enumerate(stationname_json):
                r.hset('stationname.to.ab', name, stationname_json[name])
                print 'Init:stationName.to.ab:Insert One'
            r.save()
        else:
            pass
