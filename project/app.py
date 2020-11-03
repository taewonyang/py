import requests
import urllib.request as req
import urllib.parse  # 아스키코드로 변환시키기 위해 필요한 모듈
from bs4 import BeautifulSoup
import folium
import re
from openpyxl import load_workbook
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://taewon:qlalfqjsgh@54.180.80.43', 27017)
db = client.project

wb = load_workbook("station.xlsx", data_only=True)
excel = wb['Sheet2']

temp = []
for i in excel.rows:
    temp.append(i)

stationList = []
for row in temp:
    name = row[0].value
    stationList.append(name)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/MapView')
def MapView():
    return render_template('map.html')

@app.route('/enrollment')
def enrollment():
    return render_template('enrollment.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/mylist', methods=['post'])
def register():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    station_receive = request.form['station_give']
    memo_receive = request.form['memo_give']
    visit_receive = request.form['visit_give']
    food_kind_receive = request.form['food_kind_give']

    if ((station_receive in stationList) == True):
        # 위도,경도 추출하기
        api_key = '340094C7-00E9-3582-9DDE-6566D6A8605C'
        api_url = f'http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={address_receive}&refine=true&simple=false&format=json&type=ROAD&key={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        res = requests.get(api_url, headers=headers)
        html = res.content.decode('utf8')
        x_code = re.findall('"x" : "(.*?)", "y', html)[0]
        y_code = re.findall('"y" : "(.*?)"}', html)[0]
        if not (list(db.food_store.find({}))):
            doc = {'no': 1, 'name': name_receive, 'address': address_receive, 'x_code': x_code, 'y_code': y_code,
                   'station': station_receive, 'memo': memo_receive, 'visit': visit_receive,
                   'food_kind': food_kind_receive}
            db.food_store.insert_one(doc)
            stationInput_result = 'success'
            print('db등록성공')
        else:
            all = list(db.food_store.find({}))
            no = all[len(all) - 1]['no']
            no = no + 1
            doc = {'no': no, 'name': name_receive, 'address': address_receive, 'x_code': x_code, 'y_code': y_code,
                   'station': station_receive, 'memo': memo_receive, 'visit': visit_receive,
                   'food_kind': food_kind_receive}
            db.food_store.insert_one(doc)
            stationInput_result = 'success'
            print('db등록성공')

        # 지도만들기
        m = folium.Map(location=[37.529471, 127.008920], zoom_start=12)
        all_store = list(db.food_store.find({}))
        for store in all_store:
            name = store['name']
            visit = store['visit']
            x_code = store['x_code']
            y_code = store['y_code']
            if visit == "visit_ok":
                folium.Marker(location=[y_code, x_code], tooltip=name,
                              icon=folium.Icon(color="blue", icon="home")).add_to(m)
            else:
                folium.Marker(location=[y_code, x_code], tooltip=name,
                              icon=folium.Icon(color="red", icon="star")).add_to(m)
        m.save('./templates/map.html')
        print('지도화 성공!')
    else:
        stationInput_result = 'fail'
        print('잘못된 역명칭 입력!')

    return jsonify({'stationInput_result': stationInput_result})

@app.route('/mylist', methods=['get'])
def sarching():
    # 지하철역 근처 매장조회
    inputBox_receive = request.args.get('inputBox_give')
    station = inputBox_receive.split()[0]
    checkedList = inputBox_receive.split()[1].split(',')
    radioVal = inputBox_receive.split()[2]
    store_info = []
    print(station)

    if ((station in stationList) == True): #1. 정확한 역명칭 입력여부확인(True)
        for checkedCategory in checkedList:
            if (radioVal == "visit_all"):  # 1-1.방문여부 상관없이
                stores = list(db.food_store.find({'station': station, 'food_kind': checkedCategory}, {'_id': 0}))
                if (stores != []) :
                    for store in stores :
                        store_info.append(store)

            else: # 1-1.방문여부(가봄 or 안가봄)
                stores = list(db.food_store.find({'station': station, 'visit': radioVal, 'food_kind': checkedCategory},
                                                 {'_id': 0}))
                if (stores != []) : #조건데이터 있음
                    for store in stores :
                        store_info.append(store)

        if(store_info != []):
            stationSearch_result = 'success'
        else :
            stationSearch_result = 'data_empty'

    else: #1. 정확한 역명칭 입력여부확인(False)
        stationSearch_result = 'fail'
        print('아무작업 안함')

    return jsonify({'stationSearch_result': stationSearch_result, 'store_info': store_info})

@app.route('/crawling', methods=['get'])
def crawling():
    nameClick_receive = request.args.get('nameClick_give')
    crawling_result = 'success'
    print(nameClick_receive)
    storeBlog_title = []
    storeBlog_href = []
    base_url = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query='
    url = base_url + urllib.parse.quote_plus(nameClick_receive)
    html = req.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find_all(class_='api_txt_lines total_tit')
    result = result[:5]

    for blog in result :
        href = blog.attrs['href']
        title = blog.text
        storeBlog_title.append(title)
        storeBlog_href.append(href)
    stores = {'storeBlog_title': storeBlog_title, 'storeBlog_href': storeBlog_href}
    return jsonify({'crawling_result': crawling_result, 'stores': stores})


@app.route('/revise', methods=['get'])
def revise():
    storeName_receive = request.args.get('storeName_give')
    print(storeName_receive)
    if storeName_receive=="" :
       store_info = list(db.food_store.find({}, {'_id': 0}))
       result = "success"
    else :
        all = list(db.food_store.find({}, {'_id': 0}))
        for i in all :
            one = i['name']
            if (storeName_receive in one) == True :
                store_info = list(db.food_store.find({'name': one}, {'_id': 0}))
                result = "success"
    return jsonify({'result':result, 'store_info':store_info})

# @app.route('/revise', methods=['post'])
# def revise():
    # stationBox_receive = request.args.get('stationBox_give')
    # if stationBox_receive=="" :
    #    store_info = list(db.food_store.find({}, {'_id': 0}))
    #    result = "success"
    # else :
    #     store_info = list(db.food_store.find({'station':stationBox_receive}, {'_id': 0}))
    #     result = "success"
    # return jsonify({'result':result, 'store_info':store_info})
    # return jsonify({'result': 'result'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)