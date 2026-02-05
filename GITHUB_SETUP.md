# GitHub 연결 가이드

## 방법 1: 명령어로 직접 연결 (추천)

### 1단계: Git 초기화 및 첫 커밋

프로젝트 폴더에서 다음 명령어 실행:

```bash
# Git 저장소 초기화
git init

# 모든 파일 스테이징
git add .

# 첫 커밋
git commit -m "Initial commit: Segye VIBE 프로젝트 기본 구조"
```

### 2단계: GitHub에서 새 리포지토리 생성

1. https://github.com/new 접속
2. Repository name: `segye-vibe` (또는 원하는 이름)
3. Description: `기사 URL로 쇼츠 영상을 자동 생성하는 뉴스 브리핑 툴`
4. **Private** 선택 (내부 프로젝트이므로)
5. ❌ "Add a README file" 체크 해제 (이미 있음)
6. "Create repository" 클릭

### 3단계: 원격 저장소 연결 및 푸시

GitHub에서 생성 후 나타나는 명령어를 복사하여 실행:

```bash
# 원격 저장소 추가 (URL은 본인의 GitHub URL로 변경)
git remote add origin https://github.com/YOUR_USERNAME/segye-vibe.git

# 기본 브랜치를 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

---

## 방법 2: GitHub CLI 사용 (간편)

GitHub CLI가 설치되어 있다면:

```bash
# Git 초기화 및 커밋
git init
git add .
git commit -m "Initial commit: Segye VIBE 프로젝트"

# GitHub에 자동으로 리포지토리 생성 및 푸시
gh repo create segye-vibe --private --source=. --remote=origin --push
```

---

## 방법 3: GitHub Desktop 사용 (GUI)

1. GitHub Desktop 설치: https://desktop.github.com/
2. GitHub Desktop 실행
3. File → Add Local Repository
4. 프로젝트 폴더 선택
5. "Publish repository" 클릭
6. Private 체크
7. Publish 클릭

---

## 이후 작업 흐름

### 파일 수정 후 업로드

```bash
# 변경사항 확인
git status

# 파일 스테이징
git add .

# 커밋
git commit -m "커밋 메시지"

# GitHub에 푸시
git push
```

### 자주 사용하는 Git 명령어

```bash
# 현재 상태 확인
git status

# 변경사항 확인
git diff

# 커밋 히스토리 보기
git log --oneline

# 원격 저장소 확인
git remote -v

# 최신 코드 받기
git pull
```

---

## .gitignore 설정 확인

이미 `.gitignore` 파일이 생성되어 있어 다음 항목들은 자동으로 제외됩니다:

- ✅ `.env` (API 키 등 민감 정보)
- ✅ `output/` (생성된 영상 파일)
- ✅ `__pycache__/` (Python 캐시)
- ✅ 큰 미디어 파일 (mp4, mp3 등)

**중요**: `.env` 파일은 절대 GitHub에 올리지 마세요!

---

## 협업 설정 (필요시)

### 팀원 초대

1. GitHub 리포지토리 페이지 → Settings → Collaborators
2. "Add people" 클릭
3. 팀원 GitHub 아이디 입력

### 브랜치 전략

```bash
# 새 기능 개발 시
git checkout -b feature/새기능명

# 개발 완료 후
git push origin feature/새기능명

# GitHub에서 Pull Request 생성
```

---

## 문제 해결

### "git: command not found" 오류

Git이 설치되지 않음 → https://git-scm.com/download/win 에서 설치

### 인증 오류

```bash
# Personal Access Token 사용 (추천)
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token
# repo 권한 체크 후 생성
# 비밀번호 대신 토큰 입력
```

### 푸시 거부됨

```bash
# 원격 저장소의 변경사항 먼저 받기
git pull origin main --rebase
git push
```

---

## 추천 설정

### Git 사용자 정보 설정

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 한글 파일명 깨짐 방지

```bash
git config --global core.quotepath false
```

---

프로젝트가 GitHub에 올라가면 팀원과 공유하고 협업할 수 있습니다!
