"""
Segye VIBE 초기 설정 스크립트
"""
import os
from pathlib import Path

def setup_project():
    """프로젝트 초기 설정"""
    
    print("=" * 60)
    print("Segye VIBE 프로젝트 초기 설정")
    print("=" * 60)
    
    # 1. 필요한 디렉토리 생성
    directories = [
        'static/css',
        'static/js',
        'static/images',
        'output',
        'output/audio',
        'assets/avatars',
        'assets/bgm',
        'assets/broll',
    ]
    
    print("\n[1/4] 디렉토리 생성 중...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {directory}")
    
    # 2. .env 파일 확인
    print("\n[2/4] 환경 설정 파일 확인...")
    if not Path('.env').exists():
        print("  [!] .env 파일이 없습니다.")
        print("  -> .env.example을 .env로 복사하고 API 키를 설정하세요.")
        
        # .env 파일 자동 생성 (기본값)
        with open('.env.example', 'r', encoding='utf-8') as f:
            content = f.read()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        print("  [OK] .env 파일 생성됨 (API 키를 설정해주세요)")
    else:
        print("  [OK] .env 파일이 존재합니다.")
    
    # 3. README 생성 (assets 디렉토리용)
    print("\n[3/4] 리소스 디렉토리 안내 파일 생성...")
    
    avatar_readme = """# Avatars 디렉토리

이 디렉토리에 AI 기자 아바타 영상을 배치하세요.

## 필요한 파일

- `intro_avatar.mp4`: 인트로용 아바타 영상 (5초)
- `outro_avatar.mp4`: 아웃트로용 아바타 영상 (5초)

## 아바타 생성 방법

1. **D-ID**: https://www.d-id.com/
2. **HeyGen**: https://www.heygen.com/
3. **Synthesia**: https://www.synthesia.io/

아바타 영상이 없으면 자동으로 단색 배경이 사용됩니다.
"""
    
    with open('assets/avatars/README.md', 'w', encoding='utf-8') as f:
        f.write(avatar_readme)
    
    broll_readme = """# B-roll 디렉토리

이 디렉토리에 기본 B-roll 영상이나 이미지를 배치하세요.

## 추천 소스

- **Pexels**: https://www.pexels.com/ko-kr/videos/
- **Unsplash**: https://unsplash.com/
- **Pixabay**: https://pixabay.com/ko/videos/

현재는 기사 내 이미지가 자동으로 추출되어 사용됩니다.
"""
    
    with open('assets/broll/README.md', 'w', encoding='utf-8') as f:
        f.write(broll_readme)
    
    bgm_readme = """# BGM 디렉토리

이 디렉토리에 배경음악(BGM) 파일을 배치하세요.

## 필요한 파일 (선택사항)

- `tense.mp3`: 속보/정치 뉴스용
- `soft.mp3`: 생활/문화 뉴스용
- `smart.mp3`: 경제/IT 뉴스용

## 추천 소스 (저작권 무료)

- **YouTube Audio Library**: https://studio.youtube.com/
- **Bensound**: https://www.bensound.com/
- **Incompetech**: https://incompetech.com/

BGM이 없어도 영상 생성은 정상적으로 진행됩니다.
"""
    
    with open('assets/bgm/README.md', 'w', encoding='utf-8') as f:
        f.write(bgm_readme)
    
    print("  [OK] 안내 파일 생성 완료")
    
    # 4. 다음 단계 안내
    print("\n[4/4] 설정 완료!")
    print("\n" + "=" * 60)
    print("다음 단계:")
    print("=" * 60)
    print("\n1. 패키지 설치:")
    print("   pip install -r requirements.txt")
    print("\n2. FFmpeg 설치 (필수):")
    print("   - Windows: https://ffmpeg.org/download.html")
    print("   - 설치 후 시스템 PATH에 추가")
    print("\n3. API 키 설정:")
    print("   - .env 파일을 열고 OPENAI_API_KEY 입력")
    print("   - (선택) ELEVENLABS_API_KEY 입력")
    print("\n4. 서버 실행:")
    print("   python app.py")
    print("\n5. 브라우저 접속:")
    print("   http://localhost:5000")
    print("\n" + "=" * 60)
    print("프로젝트 준비 완료!")
    print("=" * 60)


if __name__ == '__main__':
    setup_project()
