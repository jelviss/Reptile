# -*- coding:utf-8 -*-
# 功能:用于自动查询火车票余票
# @author HuanYq

import requests
import json
import smtplib
import time
from email.mime.text import MIMEText


class trainTicketsSprider:
    '''
    获得火车票的信息
    '''
    def getTicketsInfo(self, purpose_codes, queryDate,
                       from_station, to_station):
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


class notify:
    '''
    通过邮件将火车票的信息反馈给自己
    '''
    def sendEmail(self, smtpserver, sender, receiver,
                  username, password, subject, content):
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
    if (num == '--') or (num == '无'):
        return '0'
    else:
        return num


def main():
    '''
    ***************************
    邮箱配置
    @sender 发送者邮箱账号
    @receiver 收件邮箱账号
    @username 邮箱账号
    @password 邮箱密码
    @subject 邮件主题
    @smtpserver smtp服务器地址
    @content 火车票信息
    @relay 多久发送一次,单位s
    ***************************
    '''
    sender = 'example@163.com'
    receiver = 'example@live.com'
    subject = '火车票信息'
    smtpserver = 'smtp.163.com'
    username = 'example@163.com'
    password = 'yourpassword'
    relay = 120

    '''
    ***************************
    查询信息配置
    @purpose_codes 票的种类-成人票(ADULT)还是学生票(0X00)
    @queryDate 日期
    @from_station 起始站
    @to_station 目的站
    ***************************
    '''
    purpose_codes = '0X00'
    queryDate = '2015-05-23'
    from_station = 'NCG'
    to_station = 'CZQ'

    '''
    ***************************
    配置结束
    ****************************
    '''
    TicketSprider = trainTicketsSprider()
    res = TicketSprider.getTicketsInfo(purpose_codes, queryDate,
                                       from_station, to_station)
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
        '''
        print "**********************************"
        print u"车次:%s" %ticketInfo["station_train_code"]
        print u"起始站:%s" %ticketInfo["start_station_name"]
        print u"目的地:%s" %ticketInfo["to_station_name"]
        print u"开车时间:%s" %ticketInfo["start_time"]
        print u"到达时间:%s" %ticketInfo["arrive_time"]
        print u"二等座还剩:%s张票" %isZero(ticketInfo["ze_num"])
        print u"硬座还剩:%s张票" %isZero(ticketInfo["yz_num"])
        print u"硬卧还剩:%s张票" %isZero(ticketInfo["yw_num"])
        print u"无座还剩:%s张票" %isZero(ticketInfo["wz_num"])
        print u"是否有票:%s" %ticketInfo["canWebBuy"]
        '''
    content = content.join(contentlist)
    notifyme = notify()
    notifyme.sendEmail(smtpserver, sender, receiver,
                     username, password, subject, content)
    time.sleep(relay)


if __name__ == '__main__':
    while(True):
        main()
