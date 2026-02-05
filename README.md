# Segye VIBE

기사 URL 하나로 인스타그램/유튜브 쇼츠 뉴스 영상을 자동 생성하는 웹앱

## 주요 기능

- 기사 URL 입력만으로 60초 쇼츠 영상 자동 생성
- AI 기자 아바타 인트로/아웃트로 (각 5초)
- 기사 맥락 기반 자료화면(B-roll) 자동 매칭
- AI 성우 나레이션 및 자막 자동 생성
- 뉴스 브리핑 형식의 전문적인 영상 출력

## 프로젝트 구조

```
Segye VIBE/
├── app.py                    # Flask 메인 애플리케이션
├── config.py                 # 설정 파일
├── requirements.txt          # Python 패키지 의존성
├── .env.example              # 환경변수 예시
├── README.md                 # 프로젝트 문서
├── modules/                  # 핵심 모듈
│   ├── article_parser.py     # 기사 파싱
│   ├── script_generator.py   # AI 스크립트 생성
│   ├── tts_engine.py         # Text-to-Speech
│   ├── subtitle_generator.py # 자막 생성
│   └── video_composer.py     # 영상 합성
├── templates/                # HTML 템플릿
│   └── index.html
├── static/                   # 정적 파일
├── output/                   # 생성된 영상 저장
└── assets/                   # 리소스 (아바타, BGM 등)
    ├── avatars/
    ├── bgm/
    └── broll/
```

## 설치 방법

### 1. 필수 요구사항

- Python 3.8 이상
- FFmpeg (영상 처리용)

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example` 파일을 `.env`로 복사하고 API 키 설정:

```bash
cp .env.example .env
```

`.env` 파일 수정:
```
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 4. FFmpeg 설치

**Windows:**
1. https://ffmpeg.org/download.html 에서 다운로드
2. 시스템 PATH에 추가

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## 사용 방법

### 1. 서버 실행

```bash
python app.py
```

### 2. 브라우저 접속

```
http://localhost:5000
```

### 3. 영상 생성

1. 기사 URL 입력
2. "미리보기" 버튼으로 스크립트 확인 (선택사항)
3. "영상 생성" 버튼 클릭
4. 1-2분 대기 후 영상 다운로드

## API 엔드포인트

### POST /api/preview
스크립트 미리보기

**Request:**
```json
{
  "url": "https://www.segye.com/newsView/..."
}
```

**Response:**
```json
{
  "status": "success",
  "article": {
    "title": "기사 제목",
    "summary": "기사 요약"
  },
  "scripts": {
    "intro": "인트로 멘트",
    "narration": ["문장1", "문장2", ...],
    "outro": "아웃트로 멘트"
  }
}
```

### POST /api/generate
영상 생성

**Request:**
```json
{
  "url": "https://www.segye.com/newsView/..."
}
```

**Response:**
```json
{
  "status": "success",
  "video_path": "output/shorts_20240101_120000.mp4",
  "article_title": "기사 제목",
  "message": "영상이 성공적으로 생성되었습니다"
}
```

### GET /api/videos
생성된 영상 목록 조회

### GET /api/download/<filename>
영상 파일 다운로드

## 모듈 설명

### article_parser.py
- 기사 URL로부터 제목, 본문, 이미지 추출
- newspaper3k, BeautifulSoup 사용
- 카테고리 자동 추정

### script_generator.py
- OpenAI GPT-4 기반 스크립트 생성
- 인트로 (5초), 본문 (50초), 아웃트로 (5초) 분리
- 뉴스 브리핑 톤 유지

### tts_engine.py
- Google TTS (gTTS) 사용
- 한국어 음성 합성
- 문장 단위 오디오 파일 생성

### subtitle_generator.py
- 오디오 타이밍 기반 자막 데이터 생성
- SRT 파일 저장 지원
- moviepy 연동

### video_composer.py
- 최종 영상 합성
- 인트로/본문/아웃트로 조합
- 자막 오버레이
- 세로형 (1080x1920) 출력

## 개발 로드맵

### M1: MVP 구축 (현재)
- ✅ 기본 프로젝트 구조
- ✅ 기사 파싱
- ✅ 스크립트 생성
- ✅ TTS 생성
- ✅ 영상 합성

### M2: 내부 베타
- [ ] UI/UX 개선
- [ ] 아바타 영상 연동
- [ ] B-roll 자동 매칭 고도화
- [ ] 피드백 수집 시스템

### M3: 정식 운영
- [ ] 유튜브/인스타그램 API 연동
- [ ] 자동 업로드 파이프라인
- [ ] 비용 모니터링
- [ ] 일일 5건+ 생산 안정화

### M4: 고도화
- [ ] AI 기자 커스터마이징
- [ ] 멀티 템플릿 시스템
- [ ] 성과 분석 대시보드
- [ ] 외부 확장 검토

## 트러블슈팅

### FFmpeg 오류
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
→ FFmpeg가 설치되지 않았거나 PATH에 없음. 위의 설치 방법 참고

### OpenAI API 오류
```
⚠️ OPENAI_API_KEY가 설정되지 않았습니다
```
→ `.env` 파일에 API 키 설정

### moviepy 메모리 오류
→ 영상 길이를 줄이거나 해상도 조정 (config.py 수정)

## 라이센스

내부 사용 전용 (세계일보)

## 문의

프로젝트 담당자에게 문의하세요.
