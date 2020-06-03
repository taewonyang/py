from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.project  # 'project1'라는 이름의 db를 만듭니다.

@app.route('/')
def home() :
    return render_template('re_design.html')

@app.route('/mylist', methods=['post'])
def register() :
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    food_receive = request.form['food_give']
    memo_receive = request.form['memo_give']

    doc = {'name' : name_receive, 'address': address_receive, 'food' : food_receive, 'memo': memo_receive}

    db.food_store.insert_one(doc)
    print('db등록성공')
    return jsonify({'result':'success'})
    print('json화 성공')

@app.route('/mylist', methods=['get'])
def listing() :
    store = list(db.food_store.find({}, {'_id': 0}))
    return jsonify({'result':'success', 'store':store})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)

