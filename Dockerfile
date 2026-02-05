# Dockerfile for Segye VIBE
FROM python:3.11-slim

# FFmpeg 설치
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 출력 디렉토리 생성
RUN mkdir -p output/audio assets/avatars assets/bgm assets/broll

# 포트 설정
ENV PORT=8080
EXPOSE 8080

# 실행
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 300 --workers 2 app:app
