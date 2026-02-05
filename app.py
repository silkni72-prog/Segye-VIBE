"""
Segye VIBE 메인 애플리케이션
기사 URL을 입력받아 쇼츠 영상을 생성하는 웹앱
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from pathlib import Path
import traceback

from config import DEBUG, SECRET_KEY, OUTPUT_DIR
from modules.article_parser import ArticleParser
from modules.script_generator import ScriptGenerator
from modules.tts_engine import TTSEngine
from modules.subtitle_generator import SubtitleGenerator
from modules.video_composer import VideoComposer

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

# 모듈 초기화
article_parser = ArticleParser()
script_generator = ScriptGenerator()
tts_engine = TTSEngine()
subtitle_generator = SubtitleGenerator()
video_composer = VideoComposer()


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """
    영상 생성 API
    Request: { "url": "기사 URL" }
    Response: { "status": "success", "video_path": "생성된 영상 경로" }
    """
    try:
        data = request.get_json()
        article_url = data.get('url')
        
        if not article_url:
            return jsonify({'status': 'error', 'message': 'URL이 필요합니다'}), 400
        
        # 1단계: 기사 파싱
        print(f"[1/6] 기사 파싱 중... {article_url}")
        article = article_parser.parse(article_url)
        
        # 2단계: 스크립트 생성
        print("[2/6] 스크립트 생성 중...")
        scripts = script_generator.generate(article)
        
        # 3단계: TTS 생성
        print("[3/6] 음성 생성 중...")
        audio_files = tts_engine.generate(scripts)
        
        # 4단계: 자막 생성
        print("[4/6] 자막 생성 중...")
        subtitles = subtitle_generator.generate(scripts, audio_files)
        
        # 5단계: B-roll 선택
        print("[5/6] 자료화면 선택 중...")
        broll_data = video_composer.select_broll(article, scripts)
        
        # 6단계: 영상 합성
        print("[6/6] 영상 합성 중...")
        video_path = video_composer.compose(
            scripts=scripts,
            audio_files=audio_files,
            subtitles=subtitles,
            broll_data=broll_data,
            article=article
        )
        
        return jsonify({
            'status': 'success',
            'video_path': str(video_path),
            'article_title': article['title'],
            'message': '영상이 성공적으로 생성되었습니다'
        })
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/preview', methods=['POST'])
def preview_script():
    """
    스크립트 미리보기 API
    기사 URL을 받아 생성될 스크립트만 반환
    """
    try:
        data = request.get_json()
        article_url = data.get('url')
        
        if not article_url:
            return jsonify({'status': 'error', 'message': 'URL이 필요합니다'}), 400
        
        # 기사 파싱
        article = article_parser.parse(article_url)
        
        # 스크립트 생성
        scripts = script_generator.generate(article)
        
        return jsonify({
            'status': 'success',
            'article': {
                'title': article['title'],
                'summary': article['summary'],
                'content': article['content'][:200] + '...'
            },
            'scripts': scripts
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/download/<filename>')
def download_video(filename):
    """생성된 영상 다운로드"""
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'status': 'error', 'message': '파일을 찾을 수 없습니다'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/videos')
def list_videos():
    """생성된 영상 목록 조회"""
    try:
        videos = []
        for video_file in OUTPUT_DIR.glob('*.mp4'):
            videos.append({
                'filename': video_file.name,
                'size': video_file.stat().st_size,
                'created': video_file.stat().st_ctime
            })
        
        # 최신순 정렬
        videos.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'videos': videos
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("Segye VIBE 서버 시작")
    print("=" * 50)
    print(f"출력 디렉토리: {OUTPUT_DIR}")
    print("브라우저에서 http://localhost:5000 접속")
    print("=" * 50)
    
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
