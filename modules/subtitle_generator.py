"""
자막 생성 모듈
스크립트와 오디오 타이밍을 기반으로 자막 데이터 생성
"""
from pathlib import Path
import pysrt
from datetime import timedelta


class SubtitleGenerator:
    """자막 생성 클래스"""
    
    def __init__(self):
        pass
    
    def generate(self, scripts: dict, audio_files: dict) -> dict:
        """
        스크립트와 오디오 파일로부터 자막 데이터 생성
        
        Args:
            scripts: 스크립트 딕셔너리
            audio_files: 오디오 파일 경로 딕셔너리
            
        Returns:
            dict: {
                'intro': [(start, end, text), ...],
                'narration': [(start, end, text), ...],
                'outro': [(start, end, text), ...]
            }
        """
        try:
            subtitles = {
                'intro': [],
                'narration': [],
                'outro': []
            }
            
            current_time = 0.0
            
            # 인트로 자막
            if scripts.get('intro') and audio_files.get('intro'):
                duration = self._estimate_duration(audio_files['intro'])
                subtitles['intro'].append((
                    current_time,
                    current_time + duration,
                    scripts['intro']
                ))
                current_time += duration
            
            # 본문 나레이션 자막
            if scripts.get('narration') and audio_files.get('narration'):
                for idx, (sentence, audio_path) in enumerate(
                    zip(scripts['narration'], audio_files['narration'])
                ):
                    duration = self._estimate_duration(audio_path)
                    subtitles['narration'].append((
                        current_time,
                        current_time + duration,
                        sentence
                    ))
                    current_time += duration
            
            # 아웃트로 자막
            if scripts.get('outro') and audio_files.get('outro'):
                duration = self._estimate_duration(audio_files['outro'])
                subtitles['outro'].append((
                    current_time,
                    current_time + duration,
                    scripts['outro']
                ))
            
            return subtitles
            
        except Exception as e:
            raise Exception(f"자막 생성 중 오류: {str(e)}")
    
    def _estimate_duration(self, audio_path: Path) -> float:
        """
        오디오 파일의 재생 시간 추정
        
        Args:
            audio_path: 오디오 파일 경로
            
        Returns:
            float: 재생 시간(초)
        """
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(audio_path))
            return len(audio) / 1000.0  # ms to seconds
        except Exception as e:
            print(f"⚠️ 오디오 길이 측정 실패, 추정값 사용: {e}")
            # 파일 크기 기반 대략 추정 (매우 부정확하지만 fallback)
            return 3.0
    
    def save_srt(self, subtitles: dict, output_path: Path):
        """
        자막을 SRT 파일로 저장
        
        Args:
            subtitles: 자막 딕셔너리
            output_path: 저장할 SRT 파일 경로
        """
        try:
            srt_subs = pysrt.SubRipFile()
            index = 1
            
            # 모든 섹션의 자막 병합
            all_subtitles = []
            for section in ['intro', 'narration', 'outro']:
                if section in subtitles:
                    all_subtitles.extend(subtitles[section])
            
            # SRT 형식으로 변환
            for start, end, text in all_subtitles:
                sub = pysrt.SubRipItem(
                    index=index,
                    start=timedelta(seconds=start),
                    end=timedelta(seconds=end),
                    text=text
                )
                srt_subs.append(sub)
                index += 1
            
            # 파일 저장
            srt_subs.save(str(output_path), encoding='utf-8')
            print(f"✓ 자막 파일 저장: {output_path}")
            
        except Exception as e:
            print(f"⚠️ SRT 파일 저장 실패: {e}")
    
    def to_moviepy_format(self, subtitles: dict) -> list:
        """
        moviepy TextClip에서 사용할 수 있는 형식으로 변환
        
        Returns:
            list: [(start, end, text), ...]
        """
        result = []
        for section in ['intro', 'narration', 'outro']:
            if section in subtitles:
                result.extend(subtitles[section])
        return result


if __name__ == '__main__':
    # 테스트
    generator = SubtitleGenerator()
    
    test_scripts = {
        'intro': '속보입니다.',
        'narration': ['첫 번째 문장.', '두 번째 문장.'],
        'outro': '구독 부탁드립니다.'
    }
    
    # 더미 오디오 파일 (실제로는 존재해야 함)
    test_audio = {
        'intro': Path('test_intro.mp3'),
        'narration': [Path('test_1.mp3'), Path('test_2.mp3')],
        'outro': Path('test_outro.mp3')
    }
    
    try:
        subtitles = generator.generate(test_scripts, test_audio)
        print("생성된 자막:")
        for section, subs in subtitles.items():
            print(f"\n{section}:")
            for start, end, text in subs:
                print(f"  {start:.2f}s - {end:.2f}s: {text}")
    except Exception as e:
        print(f"테스트 실패: {e}")
