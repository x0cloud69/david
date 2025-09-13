import sounddevice as sd
import soundfile as sf
import numpy as np
#import wave
import os
from datetime import datetime
import speech_recognition as sr 
import pandas as pd
from pydub import AudioSegment

# 특정 device로부터 오디오 입력 받기
def record_from_device(device_index, duration, fs=44100):
    try:
        #녹음 시작
        print(f"녹음시작 (장치 : {device_index})")
        device_info = sd.query_devices(device_index, 'input')
        fs = int(device_info['default_samplerate']) #샘플링 주파수

        recording = sd.rec(
            int(duration * fs), #총 샘플수
            samplerate = fs, #샘플링 주파수
            channels = 1, #모도
            dtype = np.int16, #샘플링 데이터 타입
            device = device_index #녹음 장치 인덱스
        )
        sd.wait() #녹음 완료 대기   
        print("녹음 완료")

        #WAV 파일로 저장
        file_dir= os.path.dirname(os.path.abspath(__file__))
        file_name = datetime.now().strftime("%Y%m%d_%H%M%S.wav")
        write_file = os.path.join(file_dir, file_name)

        sf.write(write_file,
                 recording,
                 fs,
                 subtype='PCM_16'
                 )
        
        # with wave.open(write_file,'wb') as wf:
        #     wf.setnchannels(1)
        #     wf.setsampwidth(2)
        #     wf.setframerate(fs)
        #     wf.writeframes(recording.tobytes())
        print(f"WAV 파일로 저장 완료 : {write_file}")
    except Exception as e:
        print(f"오류 발생: {e}")
        
def conver_speech_to_csv(audio_path,output_csv):
    # 1. 오디오 파일 로드
    audio = AudioSegment.from_file(audio_path)
    
    # 2.음성 인식을 위한 recognizer 객체 생성
    recognizer = sr.Recognizer()
    
    # 3.결과를 저장할 리스트
    results = []
    
    # 4.오디오를 일정 구간으로 나누어 처리 (예 : 5초)
    chuck_length = 5 * 1000 # 5초
    
    for i in range(0, len(audio), chuck_length):
        # 시작 시간과 종료 시간을 먼저 계산
        start_time = i / 1000
        end_time = (i + chuck_length) / 1000
        
        # 현재 청크 추출
        chunck = audio[i:i+chuck_length]
        
        # 임시 WAV 파일 저장 
        chunck.export("temp.wav", format="wav")
        
        # 음성 파일 열기
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            
            try:
                # 음성을 텍스트로 변환
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                
                # 결과 저장
                results.append({
                    'start_time' : start_time,
                    'end_time'   : end_time,
                    'text'       : text
                })        
            except sr.UnknownValueError:
                print(f"음성을 인식할 수 없는 구간 {start_time} ~ {end_time}")
            except sr.RequestError as e:
                print(f"음성 인식 서비스 오류: {e}")
                
    if os.path.exists(output_csv):
        os.remove(output_csv)
        
    # 결과를 DataFrame으로 변환
    df = pd.DataFrame(results)
    
    # CSV 파일로 저장
    df.to_csv(output_csv,index=False,encoding='utf-8-sig')
    
    return df

# 마이크 목록 확인
def list_device():
    devices = sd.query_devices()

    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
          print (f"{idx}: device {idx} : {device['name']} max_input_channels : {device['max_input_channels']} max_output_channels : {device['max_output_channels']} ")

def FileSearch(dirctory, keyword):
    matched_files = []
    for root,dirs,files in os.walk(dirctory):
        for file in files:
            if keyword in file:
                matched_files.append(os.path.join(root,file))
    return matched_files

def tranfer_audio_file(file_path):
    # speech_recognition 라이브러리를 사용하여 오디오 파일을 텍스트로 변환하는 함수
    
    try:
        # 음성 인식기 초기화
        r = sr.Recognizer()
        
        # 오디오 파일 읽기
        with sr.AudioFile(file_path) as source:
            print("오디오 파일을 읽는 중...")
            audio = r.record(source)
        
        # 음성 인식 수행 (Google Web Speech API 사용)
        print("음성 인식 중...")
        try:
            # 한국어로 인식 시도
            text = r.recognize_google(audio, language='ko-KR')
            print(f"텍스트 변환 결과 : {text}")
            print("정확도 : Google Web Speech API는 정확도를 제공하지 않습니다.")
            return text
        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
            return None
        except sr.RequestError as e:
            print(f"음성 인식 서비스 오류: {e}")
            return None
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return None


def get_voice_text(file_path):
    audio = AudioSegment.from_file(file_path)
    
    # silence 기준 설정 (더 관대하게 설정)
    min_silence_duration_ms = 200  # 0.2초
    silence_thresh = -50  # 더 낮은 임계값
    
    # 음성 구간 감지 (수동으로 구현)
    segments = []
    start = None
    
    # 100ms씩 체크
    for i in range(0, len(audio), 100):
        chunk = audio[i:i+100]
        if chunk.dBFS > silence_thresh:
            if start is None:
                start = i
        else:
            if start is not None and (i - start) >= min_silence_duration_ms:
                segments.append((start, i))
                start = None
    
    # 마지막 구간 처리
    if start is not None and (len(audio) - start) >= min_silence_duration_ms:
        segments.append((start, len(audio)))
    
    # 너무 짧은 구간들을 합치기 (최소 1초 이상)
    merged_segments = []
    min_duration_ms = 1000  # 최소 1초
    
    for start, end in segments:
        if (end - start) >= min_duration_ms:
            merged_segments.append((start, end))
        elif merged_segments:
            # 이전 구간과 합치기
            prev_start, prev_end = merged_segments[-1]
            merged_segments[-1] = (prev_start, end)
        else:
            # 첫 번째 구간이 너무 짧으면 그냥 추가
            merged_segments.append((start, end))
    
    segments = merged_segments
    
    print(f"감지된 음성 구간: {len(segments)}개")
    for i, (start, end) in enumerate(segments):
        print(f"구간 {i+1}: {start/1000:.1f}초 ~ {end/1000:.1f}초 (길이: {(end-start)/1000:.1f}초)")
    
    # 음성 인식기 초기화
    recognizer = sr.Recognizer()
    results = []
    
    # 각 음성 구간에서 텍스트 변환
    for i, (start, end) in enumerate(segments):
        print(f"\n구간 {i+1} 처리 중... ({start/1000:.1f}초 ~ {end/1000:.1f}초)")
        
        # 해당 구간의 오디오 추출
        segment_audio = audio[start:end]
        
        # 임시 파일로 저장
        temp_file = f"temp_segment_{i}.wav"
        segment_audio.export(temp_file, format="wav")
        
        try:
            # 음성 인식 수행
            with sr.AudioFile(temp_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                
                print(f"인식된 텍스트: {text}")
                
                results.append({
                    'start_time': start/1000,
                    'end_time': end/1000,
                    'text': text
                })
                
        except sr.UnknownValueError:
            print(f"구간 {i+1}: 음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print(f"구간 {i+1}: 음성 인식 서비스 오류: {e}")
        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    return results


    

   
if __name__ == "__main__":

    # list_device()
    # input_device_index = int(input("녹음할 장치 인덱스를 입력하세요:"))
    # record_from_device(input_device_index, duration=10)

    str_input = (input("검색할 파일명을 입력하세요 :" ))
    file_dir = os.path.dirname(os.path.abspath(__file__))

    result = FileSearch(file_dir, str_input)
    print("검색된 파일 목록 :  ")
    print("-" * 30)
    for idx, file in enumerate(result):
        print(f"{idx+1}:  {file}")
    print("-" * 30)

    select_num = int(input("텍스트로 재생할 파일 번호를 입력하세요 : "))

    if 0 < select_num <= len(result):
        selected_file = result[select_num -1]
        print(f"선택된 파일 : {selected_file}")
        # 전체 오디오 파일의 시간대별 텍스트 변환 결과를 CSV로 저장
        results = get_voice_text(selected_file)
        
        # 결과를 CSV로 저장
        if results:
            df = pd.DataFrame(results)
            csv_file = os.path.join(file_dir, os.path.basename(selected_file).replace('.wav', '_voice_segments.csv'))
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"\n시간대별 음성 인식 결과가 저장되었습니다: {csv_file}")
        else:
            print("인식된 음성이 없습니다.")
