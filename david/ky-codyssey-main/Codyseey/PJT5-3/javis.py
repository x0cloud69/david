import sounddevice as sd
import soundfile as sf
import numpy as np
#import wave
import os
from datetime import datetime


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
        file_dir = os.path.join(file_dir,"record")
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
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
         print (f"device {idx} : {device['name']} max_input_channels : {device['max_input_channels']} max_output_channels : {device['max_output_channels']} ")
   
if __name__ == "__main__":

    list_device()
    input_device_index = int(input("녹음할 장치 인덱스를 입력하세요:"))
    record_from_device(input_device_index, duration=10)