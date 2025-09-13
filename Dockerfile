# Python 공식 이미지를 베이스로 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . .

# requirements.txt에 명시된 패키지들을 설치
RUN pip install -r requirements.txt

# 80번 포트 사용 명시
EXPOSE 80

# gunicorn으로 애플리케이션 실행
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]

