# Segye VIBE 빠른 시작 가이드

## 1단계: 초기 설정

```bash
# 설정 스크립트 실행
python setup.py
```

## 2단계: FFmpeg 설치

### Windows
1. https://ffmpeg.org/download.html 에서 다운로드
2. 압축 해제 후 `bin` 폴더를 시스템 PATH에 추가
3. 확인: 
```bash
ffmpeg -version
```

### 간편 설치 (Chocolatey)
```bash
choco install ffmpeg
```

## 3단계: Python 패키지 설치

```bash
pip install -r requirements.txt
```

**주의**: 설치 중 오류가 발생하면:
```bash
# 최신 pip로 업그레이드
python -m pip install --upgrade pip

# 재시도
pip install -r requirements.txt
```

## 4단계: API 키 설정

`.env` 파일을 열고 다음 내용 수정:

```env
# 필수
OPENAI_API_KEY=sk-...

# 선택사항 (더 나은 음성 품질)
ELEVENLABS_API_KEY=...
```

### OpenAI API 키 발급
1. https://platform.openai.com/api-keys 접속
2. "Create new secret key" 클릭
3. 생성된 키를 복사하여 `.env`에 붙여넣기

## 5단계: 서버 실행

```bash
python app.py
```

다음과 같은 메시지가 나타나면 성공:

```
==================================================
Segye VIBE 서버 시작
==================================================
출력 디렉토리: c:\...\output
브라우저에서 http://localhost:5000 접속
==================================================
```

## 6단계: 브라우저에서 접속

http://localhost:5000 열기

## 첫 영상 생성해보기

1. 세계일보 기사 URL 입력
   예: `https://www.segye.com/newsView/20240101000001`

2. "미리보기" 버튼 클릭 (선택사항)
   - 생성될 스크립트를 미리 확인

3. "영상 생성" 버튼 클릭
   - 1-2분 대기
   - 완료 시 다운로드 링크 표시

## 테스트 모드 (API 키 없이)

API 키 없이도 테스트 가능합니다:
- OpenAI API 키가 없으면 더미 스크립트 사용
- 기본 TTS(gTTS) 사용

실제 프로덕션 사용 시에는 OpenAI API 키가 필수입니다.

## 문제 해결

### FFmpeg 오류
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
**해결**: FFmpeg를 설치하고 PATH에 추가

### ImportError
```
ImportError: No module named 'moviepy'
```
**해결**: `pip install -r requirements.txt` 다시 실행

### OpenAI API 오류
```
openai.error.AuthenticationError
```
**해결**: `.env` 파일의 API 키 확인

### 포트 이미 사용 중
```
Address already in use
```
**해결**: 다른 포트 사용
```bash
# app.py 마지막 줄 수정
app.run(debug=DEBUG, host='0.0.0.0', port=5001)  # 5000 → 5001
```

## 아바타 영상 추가 (선택사항)

기본적으로는 단색 배경이 사용됩니다. 실제 아바타를 사용하려면:

1. D-ID, HeyGen 등에서 아바타 영상 생성
2. `assets/avatars/` 디렉토리에 배치:
   - `intro_avatar.mp4` (5초)
   - `outro_avatar.mp4` (5초)

## 다음 단계

- [ ] 여러 기사로 테스트
- [ ] 생성된 영상 품질 확인
- [ ] 필요 시 `config.py`에서 설정 조정
  - 영상 해상도
  - 자막 크기/색상
  - TTS 속도
- [ ] 아바타 영상 추가
- [ ] BGM 추가

## 추가 도움말

자세한 내용은 `README.md` 참고
