#-*- coding:utf-8 -*-
import requests
import json

class trainTicketsSprider:

    def getTicketsInfo(self,purpose_codes,queryDate,from_station,to_station):
        url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=%s&queryDate=%s&from_station=%s&to_station=%s' %(purpose_codes,queryDate,from_station,to_station)
        headers = { 
                    "Accept":"text/html,application/xhtml+xml,application/xml;",
                    "Accept-Encoding":"gzip",
                    "Accept-Language":"zh-CN,zh;q=0.8",
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                  }
        TicketSession = requests.Session()
        TicketSession.verify = False #关闭https验证   
        TicketSession.headers = headers
        try:
            resp_json = TicketSession.get(url)
            ticketsDatas = json.loads(resp_json.text)["data"]["datas"]
            return ticketsDatas
        except Exception,e:
            print e

def isZero(num):
    if num == '--' or '无':
        return '0'
    else:
        return num
    
def main():
    purpose_codes = 'ADULT'
    queryDate = '2015-05-23'
    from_station = 'NCG'
    to_station = 'CZQ'
    TicketSprider = trainTicketsSprider()
    res= TicketSprider.getTicketsInfo(purpose_codes,queryDate,from_station,to_station)
    for i,ticketInfo in enumerate(res):        
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
                print "**********************************"
                
                
if __name__ == '__main__':
    main()