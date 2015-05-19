# coding:utf-8
import json
content = open('station_name.js').read()
each_stations = content.split('@')
station_list = {}
for each_station in station_stations:
    my_data = each_station.split('|')
    try:
        station_list[my_data[1]]=my_data[2]
    except:
        pass
print json.dumps(station_list)
