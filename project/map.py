import requests
import folium
import re
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.project  # 'project1'라는 이름의 db를 만듭니다.

# 1. 상호명리스트(name_list) 추출
# 2. 주소리스트(address_list) 추출
all_store = list(db.food_store.find({}))
name_list = []
address_list = []
for store in all_store :
    name = store['name']
    address = store['address']
    name_list.append(name)
    address_list.append(address)

# 3.x_code_list(좌표-위도리스트) 추출
# 4.y_code_list(좌표-경도리스트) 추출
api_key = '340094C7-00E9-3582-9DDE-6566D6A8605C'
x_code_list = []
y_code_list = []
for addr in address_list :
    api_url =f'http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={addr}&refine=true&simple=false&format=json&type=ROAD&key={api_key}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    res = requests.get(api_url, headers=headers)
    html = res.content.decode('utf8')
    x_code = re.findall('"x" : "(.*?)", "y', html)[0]
    y_code = re.findall('"y" : "(.*?)"}', html)[0]
    x_code_list.append(x_code)
    y_code_list.append(y_code)

# part2.지도화 하기
m = folium.Map(location=[37.4838699,127.0565831], zoom_start=12)
for x_code, y_code, name in zip(x_code_list, y_code_list, name_list):
    folium.Marker(location=[y_code, x_code], tooltip=name, icon=folium.Icon(color ="red", icon="star")).add_to(m)
m.save('index.html')