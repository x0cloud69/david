import sounddevice as sd
import soundfile as sf
import numpy as np
#import wave
import os
from datetime import datetime
import speech_recognition as sr 
import csv

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
            if (not keyword.strip() or keyword in file) and file.endswith('.wav'):
                matched_files.append(os.path.join(root,file))
    return matched_files

def tranfer_audio_file(file_path):
    # speech_recognition 라이브러리를 사용하여 오디오 파일을 텍스트로 변환하는 함수
    
    data_csv = [['time','text']]
    data_dict = {'time':[],'text':[]}
    
    
    try:
        # 음성 인식기 초기화
        r = sr.Recognizer()
        
        # 오디오 파일 읽기 전 메타데이터 확인
        # file_stats_before = os.stat(file_path)
        # print("=== 파일 읽기 전 메타데이터 ===")
        # print(f"읽기 전 접근 시간: {datetime.fromtimestamp(file_stats_before.st_atime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 오디오 파일 읽기
        with sr.AudioFile(file_path) as source:
            print("오디오 파일을 읽는 중...")
            # 오디오 파일의 정보를 먼저 가져오기
            duration = source.DURATION
            audio = r.record(source)
        
        # 음성 인식 수행 (Google Web Speech API 사용)
        print("음성 인식 중...")
        try:
            # 한국어로 인식 시도
            text = r.recognize_google(audio, language='ko-KR')
            print(f"텍스트 변환 결과 : {text}")
            print(f"오디오 파일 길이 : {duration:.2f}초")
            # CSV 파일로 저장 (CSV 사용)
            # data_csv.append([duration, text])
            # with open(file_path.replace('.wav', '.csv'), 'w',newline='', encoding='utf-8') as file:
            #     writer = csv.writer(file)
            #     writer.writerows(data_csv)
            # return text
            # Dictionary 사용
            data_dict['time'] = duration
            data_dict['text'] = text
            with open(file_path.replace('.wav','.csv'),'w',newline='',encoding='utf-8') as file:
                writer = csv.DictWriter(file,fieldnames=['time','text'])
                writer.writeheader()
                writer.writerow(data_dict)
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


   
if __name__ == "__main__":

    #list_device()
    # input_device_index = int(input("녹음할 장치 인덱스를 입력하세요:"))
    # record_from_device(input_device_index, duration=10)

    str_input = (input("검색할 파일명을 입력하세요 혹은 엔터(전체 검색):" ))
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
        tranfer_audio_file(selected_file)
    else:
        print("잘못된 번호를 입력하였습니다.")
        exit()

