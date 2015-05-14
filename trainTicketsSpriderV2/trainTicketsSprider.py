# -*- coding:utf-8 -*-
# 功能:用于自动查询火车票余票
# @author HuanYq

import requests
import json
import smtplib
import time
from email.mime.text import MIMEText

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class trainTicketsSprider:
    def getTicketsInfo(self, purpose_codes, queryDate,
                       from_station, to_station):
        '''
        获得火车票的信息
        '''
        self.url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=%s&queryDate=%s&from_station=%s&to_station=%s' %(
               purpose_codes, queryDate, from_station, to_station)
        self.headers = {
                    "Accept": "text/html,   \
                    application/xhtml+xml,  \
                    application/xml;",
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/42.0.2311.90 Safari/537.36"
                  }
        self.TicketSession = requests.Session()
        self.TicketSession.verify = False  # 关闭https验证
        self.TicketSession.headers = self.headers
        try:
            self.resp_json = self.TicketSession.get(self.url)
            self.ticketsDatas = json.loads(self.resp_json.text)["data"]["datas"]
            return self.ticketsDatas
        except Exception, e:
            print e


    def sendEmail(self, smtpserver, sender, receiver,
              username, password, subject, content):
        '''
        通过邮件将火车票的信息反馈给自己
        '''
        self.msg = MIMEText(content, 'html', 'utf8')
        self.msg.set_charset('utf8')
        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.smtp = smtplib.SMTP()
        self.smtp.connect(smtpserver)
        # self.smtp.set_debuglevel(1)
        self.smtp.login(username, password)
        self.smtp.sendmail(sender, receiver, self.msg.as_string())
        self.smtp.quit()

       
def isZero(num):
    if num == '--' or '无':
        return '0'
    else:
        return num


def getandsend(purpose_codes, queryDate, from_station, to_station ,smtpserver, sender, receiver, 
              username, password, subject): 
    r = trainTicketsSprider()
    res = r.getTicketsInfo(purpose_codes, queryDate, from_station, to_station) 
    contentlist = []
    content = ''
    for i, ticketInfo in enumerate(res):
        contentlist.append("**********************************</br>")
        contentlist.append(u"车次:%s</br>" %ticketInfo["station_train_code"])
        contentlist.append(u"起始站:%s</br>" %ticketInfo["start_station_name"])
        contentlist.append(u"目的地:%s</br>" %ticketInfo["to_station_name"])
        contentlist.append(u"开车时间:%s</br>" %ticketInfo["start_time"])
        contentlist.append(u"到达时间:%s</br>" %ticketInfo["arrive_time"])
        contentlist.append(u"二等座还剩:%s张票</br>" %isZero(ticketInfo["ze_num"]))
        contentlist.append(u"硬座还剩:%s张票</br>" %isZero(ticketInfo["yz_num"]))
        contentlist.append(u"硬卧还剩:%s张票</br>" %isZero(ticketInfo["yw_num"]))
        contentlist.append(u"无座还剩:%s张票</br>" %isZero(ticketInfo["wz_num"]))
        contentlist.append(u"是否有票:%s</br>" %ticketInfo["canWebBuy"])
    content = content.join(contentlist)
    r.sendEmail(smtpserver, sender, receiver,
              username, password, subject, content)
    return 'ok'
