"""
Segye VIBE 설정 파일
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# 비디오 설정
VIDEO_SETTINGS = {
    'width': int(os.getenv('VIDEO_WIDTH', 1080)),
    'height': int(os.getenv('VIDEO_HEIGHT', 1920)),
    'fps': int(os.getenv('VIDEO_FPS', 30)),
    'target_duration': int(os.getenv('TARGET_DURATION', 60)),
}

# 아바타 설정
AVATAR_SETTINGS = {
    'intro_duration': int(os.getenv('INTRO_DURATION', 5)),
    'outro_duration': int(os.getenv('OUTRO_DURATION', 5)),
}

# 디렉토리 설정
OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'output')
ASSETS_DIR = BASE_DIR / os.getenv('ASSETS_DIR', 'assets')
AVATARS_DIR = ASSETS_DIR / 'avatars'
BGM_DIR = ASSETS_DIR / 'bgm'
BROLL_DIR = ASSETS_DIR / 'broll'

# 디렉토리 생성
for directory in [OUTPUT_DIR, ASSETS_DIR, AVATARS_DIR, BGM_DIR, BROLL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 템플릿 설정
TEMPLATES = {
    'breaking_news': {
        'name': '속보·정치',
        'bgm': 'tense',
        'subtitle_style': 'bold',
        'transition': 'fast'
    },
    'lifestyle': {
        'name': '생활·문화',
        'bgm': 'soft',
        'subtitle_style': 'smooth',
        'transition': 'gentle'
    },
    'economy': {
        'name': '경제·IT',
        'bgm': 'smart',
        'subtitle_style': 'clean',
        'transition': 'professional'
    }
}

# 자막 설정
SUBTITLE_SETTINGS = {
    'font': 'NanumGothicBold',
    'font_size': 60,
    'color': 'white',
    'stroke_color': 'black',
    'stroke_width': 3,
    'position': ('center', 'bottom'),
    'padding': 100,
}

# 나레이션 설정
NARRATION_SETTINGS = {
    'voice_id': 'ko-KR-Standard-A',  # Google TTS 기본값
    'speaking_rate': 1.0,
    'pitch': 0.0,
}

# 스크립트 생성 프롬프트
SCRIPT_PROMPTS = {
    'headline': """
다음 뉴스 기사의 핵심을 5초 분량의 인트로 멘트로 만들어주세요.
- 시청자의 관심을 즉시 끄는 훅(Hook) 포함
- 20자 이내
- 뉴스 브리핑 톤
- 반말 금지, 존댓말 사용

기사 제목: {title}
기사 요약: {summary}
""",
    'narration': """
다음 뉴스 기사를 50초 분량의 나레이션 스크립트로 만들어주세요.
- 뉴스 브리핑 형식
- 핵심 정보 중심으로 간결하게
- 문장당 10-15자 내외
- 5-6개 문장으로 구성
- 존댓말 사용

기사 내용:
{content}
""",
    'outro': """
다음 멘트를 5초 분량으로 작성해주세요:
"구독과 좋아요로 더 많은 뉴스를 받아보세요"
- 15자 이내
- 친근하지만 격식있는 톤
"""
}

# Flask 설정
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
