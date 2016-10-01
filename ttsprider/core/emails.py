# -*- coding:utf-8 -*-
# 功能:查询火车票余票并通过邮件发送
import requests
import json
import smtplib
import time
from email.mime.text import MIMEText

def getTicketsInfo(purpose_codes, query_date, from_station, to_station):
    '''
    获得火车票的信息
    '''
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=%s&queryDate=%s&from_station=%s&to_station=%s' %(
           purpose_codes, query_date, from_station, to_station)
    headers = {
                    "Accept": "text/html,   \
                    application/xhtml+xml,  \
                    application/xml;",
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/42.0.2311.90 Safari/537.36"
                   }
    TicketSession = requests.Session()
    TicketSession.verify = False  # 关闭https验证
    TicketSession.headers = headers
    try:
        resp_json = TicketSession.get(url)
        ticketsDatas = json.loads(resp_json.text)["data"]["datas"]
        return ticketsDatas
    except Exception, e:
        print e


def sendEmail(smtpserver, sender, receiver, username, password, subject, content):
    '''
    发送邮件
    '''
    msg = MIMEText(content, 'html', 'utf8')
    msg.set_charset('utf8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    #smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def isZero(num):
    if (num == '--') or (num == '无'):
        return '0'    
    else:
        return num 

def getAndSend(purpose_codes, query_date, from_station, to_station ,smtpserver, sender, receiver, 
              username, password, subject): 
    res = getTicketsInfo(purpose_codes, query_date, from_station, to_station) 
    contentlist = []
    content = ''
    try:
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
    except:
        content='error'

    sendEmail(smtpserver, sender, receiver,
              username, password, subject, content)
    return True

