import json
import selectScraping # 파이썬 함수 임포트
import yurim
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS #크로스오리진 허용 매우중요
scraper = selectScraping   
sc=yurim
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 노드서버로 데이터 던져줄때 한글깨져서 추가함 
cors = CORS(app) #크로스오리진 허용 매우중요




@app.route('/request2', methods =['POST'])  #일반 신용 대출 금리 계산 처리 서버 
def request2():
    # value = request.form['SensorID'] 신용등급 받아와야함
    a= scraper.hi()
    return a # 이건 jsonify하면 오류남 애초부터 노드한테 던져줄때 딕셔너리 : 리스트 형태로 던져서 괜찬



@app.route('/request3', methods =['POST']) #  원리금 균등 , 원금 균등 , 만기일시 상환 처리 서버
def request3():
    # value = request.form['SensorID']  신용등급 받아와야함
    b= scraper.fin()
    return jsonify(b)  # 원래는 항상 jsonify로 던져줘야함 알겟쥐?



@app.route('/test', methods =['POST']) #  원리금 균등 , 원금 균등 , 만기일시 상환 처리 서버
def test():
    # value = request.form['SensorID']  신용등급 받아와야함

    return jsonify("d")  # 원래는 항상 jsonify로 던져줘야함 알겟쥐?



@app.route('/public', methods =['POST']) # 평균월상환금, 최소, 최대
def public():
    # value = request.form['SensorID']  신용등급 받아와야함
    p1=sc.cal_principal(10000000, 3, sc.publicloan(), 'year' )
    return jsonify(p1)  # 원래는 항상 jsonify로 던져줘야함 알겟쥐?

@app.route('/public2', methods =['POST']) #  월이자액
def public2():
    # value = request.form['SensorID']  신용등급 받아와야함
    p2=sc.publicloanmonth()
    return jsonify(p2)  # 원래는 항상 jsonify로 던져줘야함 알겟쥐?
 



# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/register', methods=['GET','POST'])
# def register():
    
#     if request.method == 'GET':
#         return render_template('register.html')

  
#     if request.method == 'POST':
#         return render_template('register.html')


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=5000, debug=True)
