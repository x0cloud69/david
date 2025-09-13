# Python 3.9 이미지를 기반으로 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    alsa-utils \
    libasound2 \
    libasound2-plugins \
    pulseaudio \
    python3-pygame \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 파일 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 애플리케이션 파일들 복사 (명시적 경로 지정)
COPY ./app.py .
COPY ./templates/ templates/
COPY ./static/ static/

# 포트 80 노출
EXPOSE 80

# 환경 변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 애플리케이션 실행 (프로덕션용 gunicorn 사용)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80", "--workers", "2"] 