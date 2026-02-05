# Segye VIBE 배포 가이드

## 🚀 추천 배포 플랫폼

### 1. Railway.app (가장 추천) ⭐⭐⭐⭐⭐

**장점:**
- ✅ Python 앱에 최적화
- ✅ FFmpeg 자동 설치
- ✅ 무료 티어 제공 ($5 크레딧/월)
- ✅ GitHub 자동 배포
- ✅ 긴 실행 시간 허용
- ✅ 파일 저장 가능

**배포 방법:**

1. **Railway 가입**
   - https://railway.app/ 접속
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - `Segye-VIBE` 리포지토리 선택

3. **환경변수 설정**
   - Settings → Variables 탭
   - 다음 환경변수 추가:
     ```
     OPENAI_API_KEY=sk-...
     PORT=8080
     ```

4. **배포 완료!**
   - 자동으로 빌드 및 배포됨
   - 생성된 URL로 접속

**Railway CLI로 배포:**
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up
```

---

### 2. Render.com (무료 옵션) ⭐⭐⭐⭐

**장점:**
- ✅ 완전 무료 티어
- ✅ GitHub 자동 배포
- ✅ FFmpeg 지원
- ⚠️ 비활성 시 sleep (첫 요청 시 느림)

**배포 방법:**

1. **Render 가입**
   - https://render.com/ 접속
   - GitHub 계정으로 로그인

2. **Web Service 생성**
   - "New +" → "Web Service"
   - GitHub 리포지토리 연결
   - 설정:
     ```
     Name: segye-vibe
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
     ```

3. **환경변수 설정**
   - Environment 탭에서 추가:
     ```
     OPENAI_API_KEY=sk-...
     PYTHON_VERSION=3.11.7
     ```

4. **배포 완료!**

---

### 3. Google Cloud Run (확장성 우수) ⭐⭐⭐⭐⭐

**장점:**
- ✅ 사용한 만큼만 과금
- ✅ 자동 스케일링
- ✅ 긴 실행 시간 (최대 60분)
- ⚠️ 설정이 복잡함

**배포 방법:**

1. **Dockerfile 생성** (이미 제공됨)
2. **Google Cloud Console에서 프로젝트 생성**
3. **Cloud Build 활성화**
4. **배포 명령:**
   ```bash
   gcloud run deploy segye-vibe \
     --source . \
     --platform managed \
     --region asia-northeast3 \
     --allow-unauthenticated
   ```

---

### 4. Heroku (전통적 선택) ⭐⭐⭐

**주의:** 2022년부터 무료 티어 종료 (최소 $5/월)

**배포 방법:**

1. **Heroku CLI 설치**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   ```

2. **배포**
   ```bash
   heroku login
   heroku create segye-vibe
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
   heroku buildpacks:add --index 2 heroku/python
   git push heroku main
   ```

3. **환경변수 설정**
   ```bash
   heroku config:set OPENAI_API_KEY=sk-...
   ```

---

## ❌ Vercel은 적합하지 않음

**이유:**
- ❌ 실행 시간 제한 (최대 60초, 영상 생성은 1-2분)
- ❌ 파일 시스템 제약 (임시 파일만 가능)
- ❌ FFmpeg 바이너리 제한
- ❌ 메모리 제한 (1GB)

Vercel은 **정적 사이트 / API / Next.js**에 최적화되어 있습니다.

---

## 🎯 추천 순위

### 내부 사용 (세계일보):
1. **Railway** - 가장 쉽고 빠름
2. **Google Cloud Run** - 확장성 필요 시
3. **자체 서버** - 완전한 제어 필요 시

### 외부 서비스:
1. **Railway** - 개발/베타
2. **Google Cloud Run** - 프로덕션
3. **AWS ECS** - 엔터프라이즈

---

## 📝 배포 전 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] API 키를 환경변수로 설정
- [ ] `gunicorn` 설치 (requirements.txt에 추가됨)
- [ ] FFmpeg가 플랫폼에서 지원되는지 확인
- [ ] 첫 배포 후 테스트 기사로 영상 생성 테스트

---

## 🔧 트러블슈팅

### 타임아웃 오류
→ 서버 타임아웃 설정 늘리기:
```python
# config.py에 추가
REQUEST_TIMEOUT = 300  # 5분
```

### FFmpeg 오류
→ 빌드팩에 FFmpeg 추가 확인

### 메모리 부족
→ worker 수 줄이기 (gunicorn workers=1)

---

더 자세한 도움이 필요하면 말씀해주세요!
