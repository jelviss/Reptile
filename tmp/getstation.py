#-*-coding:utf-8-*-
'''
功能：从station_name.js中将车站名与拼音缩写的信息提取出来
(station_name.js是从12306的爬下来的一个js文件，里面存有车站与拼音缩写信息)
'''

import json
content = open('station_name.js').read()
station_stations = content.split('@')
station_list = {}
for each_station in station_stations:
    my_data = each_station.split('|')
    try:
        station_list[my_data[1]]=my_data[2]
    except:
        pass
print json.dumps(station_list)
