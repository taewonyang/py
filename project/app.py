import requests
import folium
import re
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.project  # 'project'라는 이름의 db를 만듭니다.

app = Flask(__name__)
@app.route('/')
def home() :
    return render_template('index.html')

@app.route('/MapView')
def MapView() :
    return render_template('map.html')

@app.route('/enrollment')
def enrollment() :
    return render_template('enrollment.html')

@app.route('/search')
def search() :
    return render_template('search.html')

@app.route('/mylist', methods=['post'])
def register() :
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    memo_receive = request.form['memo_give']
    visit_receive = request.form['visit_give']
    food_kind_receive = request.form['food_kind_give']
    juso = address_receive.split()  # 도로명주소에서 도로명 추출
    doromyung_name = juso[len(juso)-2]

    doc = {'name' : name_receive, 'address': address_receive, 'doromyung' : doromyung_name, 'memo': memo_receive, 'visit' : visit_receive, 'food_kind' : food_kind_receive}

    db.food_store.insert_one(doc)
    print('db등록성공')

    # 지도만들기
    all_store = list(db.food_store.find({}))
    name_list = []
    address_list = []
    visit_list = []
    food_kind_list = []
    memo_list = []
    for store in all_store:
        name = store['name']
        address = store['address']
        visit = store['visit']
        food_kind = store['food_kind']
        memo = store['memo']
        name_list.append(name)
        address_list.append(address)
        visit_list.append(visit)
        food_kind_list.append(food_kind)
        memo_list.append(memo)

    # 3.x_code_list(좌표-위도리스트) 추출
    # 4.y_code_list(좌표-경도리스트) 추출
    api_key = '340094C7-00E9-3582-9DDE-6566D6A8605C'
    x_code_list = []
    y_code_list = []
    for addr in address_list:
        api_url = f'http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={addr}&refine=true&simple=false&format=json&type=ROAD&key={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        res = requests.get(api_url, headers=headers)
        html = res.content.decode('utf8')
        x_code = re.findall('"x" : "(.*?)", "y', html)[0]
        y_code = re.findall('"y" : "(.*?)"}', html)[0]
        x_code_list.append(x_code)
        y_code_list.append(y_code)

    # part2.지도화 하기
    m = folium.Map(location=[37.4838699, 127.0565831], zoom_start=12)
    for x_code, y_code, name, visit, food_kind in zip(x_code_list, y_code_list, name_list, visit_list , food_kind_list):
        if visit == "visit_ok" :
            folium.Marker(location=[y_code, x_code], tooltip=name, icon=folium.Icon(color="blue", icon="star")).add_to(m)
        else:
            folium.Marker(location=[y_code, x_code], tooltip=name, icon=folium.Icon(color="red", icon="star")).add_to(m)
    m.save('./templates/map.html')
    print('지도화 성공!')
    return jsonify({'result':'success'})

@app.route('/mylist', methods=['get'])
def sarching() :
    station_receive = request.args.get('station_give')
    print(station_receive)
    station_data = db.jihachul.find_one({'station':station_receive}, {'_id': 0})
    print(station_data)
    addr = station_data['doromyung']
    print(addr)
    store_info = db.food_store.find_one({'doromyung' : addr}, {'_id': 0})
    print(store_info)
    return jsonify({'result':'success', 'info': store_info})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
