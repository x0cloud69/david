from flask import Flask, render_template, request, send_file
from gtts import gTTS
import base64
import io
import os
from datetime import datetime

app = Flask(__name__)

# Flask가 템플릿 폴더를 어떻게 찾는지 확인
<<<<<<< HEAD
# Git Branch 확인
=======
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81
print(f"현재 파일 경로: {__file__}")
print(f"현재 디렉토리: {os.path.dirname(os.path.abspath(__file__))}")
print(f"템플릿 폴더: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')}")

# 지원하는 언어 목록 (유효성 검증용)
LANGUAGES = {
    'ko': '한국어',
    'en': '영어',
    'ja': '일본어',
    'es': '스페인어',
    'fr': '프랑스어',
    'de': '독일어',
    'zh': '중국어'
}

def log_user_input(input_text, lang, success=True, error_msg=None):
    """사용자 입력을 로그 파일에 저장"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Text: '{input_text}', Lang: {lang}, Success: {success}"
    if error_msg:
        log_entry += f", Error: {error_msg}"
    log_entry += "\n"
    
    try:
        with open('input_log.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"로그 저장 중 오류: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    audio = None
    input_text = ""
    selected_lang = "ko"
    download_link = None
    
    if request.method == 'POST':
        try:
            # 사용자 입력 받기
            input_text = request.form.get('input_text', '').strip()
            selected_lang = request.form.get('lang', 'ko')
            
            # 빈 텍스트 검증
            if not input_text:
                error = "텍스트를 입력해주세요."
                log_user_input(input_text, selected_lang, success=False, error_msg=error)
                return render_template('index.html', error=error, input_text=input_text, selected_lang=selected_lang, languages=LANGUAGES)
            
            # 언어 코드 유효성 검증 (보너스 과제 1)
            if selected_lang not in LANGUAGES:
                error = f"지원하지 않는 언어 코드입니다: {selected_lang}. 지원 언어: {', '.join(LANGUAGES.keys())}"
                log_user_input(input_text, selected_lang, success=False, error_msg=error)
                return render_template('index.html', error=error, input_text=input_text, selected_lang=selected_lang, languages=LANGUAGES)
            
            # gTTS를 사용하여 음성 생성
            tts = gTTS(text=input_text, lang=selected_lang)
            
            # 음성 데이터를 메모리에 저장
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Base64로 인코딩하여 HTML에서 재생 가능하게 변환 (보너스 과제 3)
            audio_data = base64.b64encode(audio_buffer.read()).decode('utf-8')
            audio = audio_data
            
            # MP3 다운로드 링크 생성 (보너스 과제 2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            download_link = f"tts_audio_{timestamp}.mp3"
            
            # 성공 로그 저장 (보너스 과제 4)
            log_user_input(input_text, selected_lang, success=True)
            
        except Exception as e:
            error = f"음성 변환 중 오류가 발생했습니다: {str(e)}"
            log_user_input(input_text, selected_lang, success=False, error_msg=error)
            
    #render_template : 템플릿 파일을 렌더링하고 결과를 반환
    #index.html 파일 검색 규칙 : templates 폴더 안에 있는 index.html 파일을 찾아서 렌더링
    #flask 템플릿 엔진은 기본적으로 templates 폴더를 찾음
    #templates 폴더가 현재 파일이 있는 디렉토리의 상위 폴더에 있어야 함 
    #템프릿에 전달되는 변수 : error, audio, input_text, selected_lang, languages (html 파일에서 사용되는 변수)
    #LANGUAGES 딕셔너리는 템플릿에서 사용되는 언어 목록을 정의'
    return render_template('index.html', error=error, audio=audio, input_text=input_text, selected_lang=selected_lang, languages=LANGUAGES, download_link=download_link)

<<<<<<< HEAD
@app.route('/menu')
def menu():
    """메뉴 페이지"""
    return render_template('menu.html')

=======
>>>>>>> ce49b728e666dc113f3dda61af2c42885dcf1a81
@app.route('/download/<filename>')
def download_file(filename):
    """MP3 파일 다운로드 (보너스 과제 2)"""
    try:
        # URL 파라미터에서 base64 데이터 가져오기
        audio_data = request.args.get('data')
        if not audio_data:
            return "음성 데이터를 찾을 수 없습니다.", 404
        
        # URL 디코딩 후 base64 디코딩
        import urllib.parse
        decoded_audio = urllib.parse.unquote(audio_data)
        audio_binary = base64.b64decode(decoded_audio)
        
        # 메모리에서 파일 전송
        audio_buffer = io.BytesIO(audio_binary)
        audio_buffer.seek(0)
        
        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return f"파일 다운로드 중 오류가 발생했습니다: {str(e)}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
