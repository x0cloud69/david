

from flask import Flask

#Flask 웹 애플리케이션을 초기화
#__name__ : 현재 실행 중인 모듈의 이름을 담고 있습니다
#직접 실행할 경우 "__main__"이 됩니다
# 웹 애플리케이션 개발에 필요한 다양한 기능을 Flask 클래스에서 제공

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello DevOps~"

@app.route('/menu')
def menu():
  return render_template('menu.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)