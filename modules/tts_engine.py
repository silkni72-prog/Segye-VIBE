"""
TTS (Text-to-Speech) 엔진 모듈
스크립트를 음성으로 변환
"""
import os
from pathlib import Path
from gtts import gTTS
from config import OUTPUT_DIR


class TTSEngine:
    """TTS 생성 클래스"""
    
    def __init__(self):
        self.audio_dir = OUTPUT_DIR / 'audio'
        self.audio_dir.mkdir(exist_ok=True)
    
    def generate(self, scripts: dict) -> dict:
        """
        스크립트를 음성 파일로 변환
        
        Args:
            scripts: script_generator.generate()의 결과
            
        Returns:
            dict: {
                'intro': 인트로 오디오 파일 경로,
                'narration': 나레이션 오디오 파일 경로 리스트,
                'outro': 아웃트로 오디오 파일 경로
            }
        """
        try:
            audio_files = {
                'intro': None,
                'narration': [],
                'outro': None
            }
            
            # 인트로 음성 생성
            if scripts.get('intro'):
                audio_files['intro'] = self._text_to_speech(
                    scripts['intro'], 
                    'intro.mp3'
                )
            
            # 본문 나레이션 음성 생성
            if scripts.get('narration'):
                for idx, sentence in enumerate(scripts['narration']):
                    audio_path = self._text_to_speech(
                        sentence,
                        f'narration_{idx}.mp3'
                    )
                    audio_files['narration'].append(audio_path)
            
            # 아웃트로 음성 생성
            if scripts.get('outro'):
                audio_files['outro'] = self._text_to_speech(
                    scripts['outro'],
                    'outro.mp3'
                )
            
            return audio_files
            
        except Exception as e:
            raise Exception(f"TTS 생성 중 오류: {str(e)}")
    
    def _text_to_speech(self, text: str, filename: str) -> Path:
        """
        텍스트를 음성 파일로 변환
        
        Args:
            text: 변환할 텍스트
            filename: 저장할 파일명
            
        Returns:
            Path: 생성된 오디오 파일 경로
        """
        try:
            # gTTS 사용 (무료, 한국어 지원 양호)
            tts = gTTS(text=text, lang='ko', slow=False)
            
            # 파일 저장
            audio_path = self.audio_dir / filename
            tts.save(str(audio_path))
            
            print(f"✓ 음성 생성 완료: {filename}")
            return audio_path
            
        except Exception as e:
            raise Exception(f"음성 파일 생성 실패 ({filename}): {str(e)}")
    
    def get_duration(self, audio_path: Path) -> float:
        """오디오 파일 길이(초) 반환"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(audio_path))
            return len(audio) / 1000.0  # ms to seconds
        except Exception as e:
            print(f"오디오 길이 측정 실패: {e}")
            # 대략적인 길이 추정 (1초당 3-4 글자 기준)
            return 3.0


if __name__ == '__main__':
    # 테스트
    tts = TTSEngine()
    
    test_scripts = {
        'intro': '속보입니다. 테스트 뉴스입니다.',
        'narration': [
            '첫 번째 문장입니다.',
            '두 번째 문장입니다.',
            '세 번째 문장입니다.'
        ],
        'outro': '구독과 좋아요 부탁드립니다.'
    }
    
    audio_files = tts.generate(test_scripts)
    print("생성된 오디오 파일:")
    print(f"인트로: {audio_files['intro']}")
    print(f"본문: {len(audio_files['narration'])}개 파일")
    print(f"아웃트로: {audio_files['outro']}")
