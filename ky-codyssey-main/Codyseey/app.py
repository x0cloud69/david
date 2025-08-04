""" ✅ 1. 웹 환경 테스트 (app.py)
Flask를 사용하여 간단한 메시지를 출력하는 웹 애플리케이션을 구현하고, VS Code 환경에서 실행한다.

Python 파일명: app.py
구현 요구사항:
Flask 웹 프레임워크 사용
@app.route("/") 데코레이터 사용
함수 이름: hello_world
반환 문자열: "Hello, DevOps!"
서버 실행 시 호스트: 0.0.0.0, 포트: 8080
Visual Studio Code의 Run 메뉴에서 Run Without Debugging를 선택해서 해당 파일을 실행한다.
웹브라우저로 접속하여 Hello, DevOps! 출력을 확인한다.
Visual Studio Code의 Run 메뉴에서 Stop Debugging를 선택해서 실행을 종료한다.
Visual Studio Code의 Run 메뉴에서 Start Debugging과 Run Without Debugging을 각각 실행해보고 차이점을 확인한다.
 """

from flask import Flask

#Flask 웹 애플리케이션을 초기화
#__name__ : 현재 실행 중인 모듈의 이름을 담고 있습니다
#직접 실행할 경우 "__main__"이 됩니다
# 웹 애플리케이션 개발에 필요한 다양한 기능을 Flask 클래스에서 제공

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello DevOps~"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)