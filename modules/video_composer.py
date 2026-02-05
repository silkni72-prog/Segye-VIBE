"""
영상 합성 모듈
아바타, 나레이션, 자막, B-roll을 합성하여 최종 영상 생성
"""
import os
from pathlib import Path
from datetime import datetime
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, 
    CompositeVideoClip, TextClip, concatenate_videoclips
)
from moviepy.video.fx.resize import resize
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.fadein import fadein
import numpy as np

from config import (
    VIDEO_SETTINGS, AVATAR_SETTINGS, OUTPUT_DIR,
    SUBTITLE_SETTINGS, AVATARS_DIR, BROLL_DIR
)


class VideoComposer:
    """영상 합성 클래스"""
    
    def __init__(self):
        self.width = VIDEO_SETTINGS['width']
        self.height = VIDEO_SETTINGS['height']
        self.fps = VIDEO_SETTINGS['fps']
    
    def select_broll(self, article: dict, scripts: dict) -> dict:
        """
        기사 내용에 맞는 B-roll 선택
        
        Args:
            article: 파싱된 기사 정보
            scripts: 생성된 스크립트
            
        Returns:
            dict: {
                'images': 기사 이미지 리스트,
                'stock_videos': 스톡 영상 리스트 (추후 구현)
            }
        """
        return {
            'images': article.get('images', []),
            'stock_videos': []  # 추후 Pexels/Unsplash API 연동
        }
    
    def compose(self, scripts: dict, audio_files: dict, 
                subtitles: dict, broll_data: dict, article: dict) -> Path:
        """
        최종 영상 합성
        
        Args:
            scripts: 스크립트 딕셔너리
            audio_files: 오디오 파일 경로 딕셔너리
            subtitles: 자막 데이터 딕셔너리
            broll_data: B-roll 데이터
            article: 기사 정보
            
        Returns:
            Path: 생성된 영상 파일 경로
        """
        try:
            clips = []
            current_time = 0
            
            # 1. 인트로 (아바타 영상)
            intro_clip = self._create_intro_clip(
                audio_files.get('intro'),
                subtitles.get('intro', [])
            )
            if intro_clip:
                clips.append(intro_clip)
                current_time += intro_clip.duration
            
            # 2. 본문 (B-roll + 기사 이미지)
            body_clip = self._create_body_clip(
                audio_files.get('narration', []),
                subtitles.get('narration', []),
                broll_data
            )
            if body_clip:
                clips.append(body_clip)
                current_time += body_clip.duration
            
            # 3. 아웃트로 (아바타 영상)
            outro_clip = self._create_outro_clip(
                audio_files.get('outro'),
                subtitles.get('outro', [])
            )
            if outro_clip:
                clips.append(outro_clip)
            
            # 전체 영상 합성
            if not clips:
                raise Exception("생성할 클립이 없습니다")
            
            final_video = concatenate_videoclips(clips, method="compose")
            
            # 파일 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"shorts_{timestamp}.mp4"
            output_path = OUTPUT_DIR / output_filename
            
            print("최종 영상 렌더링 중...")
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4
            )
            
            # 리소스 정리
            final_video.close()
            for clip in clips:
                clip.close()
            
            print(f"✓ 영상 생성 완료: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"영상 합성 중 오류: {str(e)}")
    
    def _create_intro_clip(self, audio_path: Path, subtitle_data: list) -> VideoFileClip:
        """인트로 클립 생성 (아바타)"""
        try:
            # 아바타 영상이 있으면 사용, 없으면 단색 배경 생성
            avatar_files = list(AVATARS_DIR.glob('intro_*.mp4'))
            
            if avatar_files:
                # 아바타 영상 사용
                clip = VideoFileClip(str(avatar_files[0]))
            else:
                # 단색 배경 생성 (더미)
                duration = self._get_audio_duration(audio_path) if audio_path else 5
                clip = self._create_colored_clip(duration, color=(20, 30, 60))
            
            # 오디오 추가
            if audio_path and audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                clip = clip.set_audio(audio)
                clip = clip.set_duration(audio.duration)
            
            # 자막 추가
            if subtitle_data:
                clip = self._add_subtitles(clip, subtitle_data)
            
            # 리사이즈 (세로형)
            clip = clip.resize((self.width, self.height))
            
            return clip
            
        except Exception as e:
            print(f"⚠️ 인트로 생성 실패: {e}")
            return None
    
    def _create_body_clip(self, audio_paths: list, subtitle_data: list, 
                          broll_data: dict) -> VideoFileClip:
        """본문 클립 생성 (B-roll + 기사 이미지)"""
        try:
            clips = []
            images = broll_data.get('images', [])
            
            # 각 나레이션 문장에 대해 클립 생성
            for idx, audio_path in enumerate(audio_paths):
                if not audio_path or not audio_path.exists():
                    continue
                
                audio = AudioFileClip(str(audio_path))
                duration = audio.duration
                
                # 이미지 선택 (순환)
                if images:
                    image_url = images[idx % len(images)]
                    img_clip = self._create_image_clip(image_url, duration)
                else:
                    # 이미지 없으면 단색 배경
                    img_clip = self._create_colored_clip(duration, color=(40, 50, 70))
                
                # 오디오 추가
                img_clip = img_clip.set_audio(audio)
                
                # 해당 문장의 자막 추가
                if idx < len(subtitle_data):
                    # 해당 인덱스의 자막만 (시작 시간을 0으로 조정)
                    subtitle_for_clip = [(0, duration, subtitle_data[idx][2])]
                    img_clip = self._add_subtitles(img_clip, subtitle_for_clip)
                
                clips.append(img_clip)
            
            if not clips:
                return None
            
            # 클립 연결
            final_clip = concatenate_videoclips(clips, method="compose")
            return final_clip
            
        except Exception as e:
            print(f"⚠️ 본문 생성 실패: {e}")
            return None
    
    def _create_outro_clip(self, audio_path: Path, subtitle_data: list) -> VideoFileClip:
        """아웃트로 클립 생성 (아바타)"""
        # 인트로와 동일한 로직, 파일명만 다름
        try:
            avatar_files = list(AVATARS_DIR.glob('outro_*.mp4'))
            
            if avatar_files:
                clip = VideoFileClip(str(avatar_files[0]))
            else:
                duration = self._get_audio_duration(audio_path) if audio_path else 5
                clip = self._create_colored_clip(duration, color=(20, 30, 60))
            
            if audio_path and audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                clip = clip.set_audio(audio)
                clip = clip.set_duration(audio.duration)
            
            if subtitle_data:
                clip = self._add_subtitles(clip, subtitle_data)
            
            clip = clip.resize((self.width, self.height))
            return clip
            
        except Exception as e:
            print(f"⚠️ 아웃트로 생성 실패: {e}")
            return None
    
    def _create_colored_clip(self, duration: float, color: tuple) -> VideoFileClip:
        """단색 배경 클립 생성"""
        # numpy 배열로 단색 이미지 생성
        img_array = np.full((self.height, self.width, 3), color, dtype=np.uint8)
        return ImageClip(img_array, duration=duration)
    
    def _create_image_clip(self, image_url: str, duration: float) -> VideoFileClip:
        """이미지 URL로부터 클립 생성 (Ken Burns 효과)"""
        try:
            import requests
            from PIL import Image
            from io import BytesIO
            
            # 이미지 다운로드
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            # PIL Image를 numpy 배열로 변환
            img_array = np.array(img)
            
            # ImageClip 생성
            clip = ImageClip(img_array, duration=duration)
            
            # 리사이즈 (세로형 맞춤)
            clip = clip.resize((self.width, self.height))
            
            # 간단한 Ken Burns 효과 (줌 인)
            # clip = clip.resize(lambda t: 1 + 0.05 * t / duration)
            
            return clip
            
        except Exception as e:
            print(f"⚠️ 이미지 로드 실패 ({image_url}): {e}")
            # 실패 시 단색 배경 반환
            return self._create_colored_clip(duration, color=(60, 70, 90))
    
    def _add_subtitles(self, video_clip: VideoFileClip, subtitle_data: list) -> CompositeVideoClip:
        """영상에 자막 추가"""
        try:
            subtitle_clips = []
            
            for start, end, text in subtitle_data:
                # TextClip 생성
                txt_clip = TextClip(
                    text,
                    fontsize=SUBTITLE_SETTINGS['font_size'],
                    color=SUBTITLE_SETTINGS['color'],
                    stroke_color=SUBTITLE_SETTINGS['stroke_color'],
                    stroke_width=SUBTITLE_SETTINGS['stroke_width'],
                    method='caption',
                    size=(self.width - 100, None),
                    font='Arial'  # 시스템 폰트 사용
                )
                
                # 위치 및 타이밍 설정
                txt_clip = txt_clip.set_position(('center', self.height - 200))
                txt_clip = txt_clip.set_start(start)
                txt_clip = txt_clip.set_duration(end - start)
                
                subtitle_clips.append(txt_clip)
            
            # 영상과 자막 합성
            if subtitle_clips:
                return CompositeVideoClip([video_clip] + subtitle_clips)
            else:
                return video_clip
                
        except Exception as e:
            print(f"⚠️ 자막 추가 실패: {e}")
            return video_clip
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """오디오 길이 반환"""
        try:
            if audio_path and audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                duration = audio.duration
                audio.close()
                return duration
        except:
            pass
        return 5.0  # 기본값


if __name__ == '__main__':
    print("VideoComposer 모듈 테스트")
    composer = VideoComposer()
    print(f"비디오 설정: {composer.width}x{composer.height} @ {composer.fps}fps")
