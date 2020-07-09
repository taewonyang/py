from openpyxl import load_workbook
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.project

wb = load_workbook("station.xlsx", data_only=True)
excel = wb['Sheet1']

# temp=[]
# for i in excel.rows :
#     temp.append(i)
#
# del temp[0]
#
# hosun_list = []
# station_list = []
# station_addr_list = []
# doromyung_list = []
# for row in temp :
#     hosun = row[0].value
#     station = row[1].value
#     station_addr = row[4].value
#     #도로명주소 추출
#     juso = station_addr.split()
#     doromyung = juso[len(juso) - 2]
#     doromyung_list.append(doromyung)
#     hosun_list.append(hosun)
#     station_list.append(station)
#     station_addr_list.append(station_addr)
#
# for hosun, station, station_addr, doromyung in zip(hosun_list, station_list, station_addr_list, doromyung_list) :
#     doc = {'hosun':hosun, 'station':station, 'station_addr':station_addr, 'doromyung':doromyung}
#     db.jihachul.insert_one(doc)
#
print(db.jihachu.find())
