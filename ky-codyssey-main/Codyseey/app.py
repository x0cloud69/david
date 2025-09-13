<<<<<<< HEAD


from flask import Flask
=======
# render_template : 템플릿 파일을 렌더링하여 HTML 페이지를 생성하는 함수
from flask import Flask,render_template
import socket
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81

#Flask 웹 애플리케이션을 초기화
#__name__ : 현재 실행 중인 모듈의 이름을 담고 있습니다
#직접 실행할 경우 "__main__"이 됩니다
# 웹 애플리케이션 개발에 필요한 다양한 기능을 Flask 클래스에서 제공
<<<<<<< HEAD
=======
# Hunk 단위로 Git 커밋 가능
# Font size 50 pt
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello DevOps~"

<<<<<<< HEAD
=======
# 메뉴 화면 추가
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81
@app.route('/menu')
def menu():
  return render_template('menu.html')

<<<<<<< HEAD
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
=======
@app.route('/index')
def home():
  if app.debug:
    hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
  else:
    hostname = ''  
  return render_template('index.html',debug=True,computername=hostname)

#Force test1.html ,,,,hh....
""" @app.route('/test1')
def test1():
  return render_template('test1.html') """



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=True)
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81
