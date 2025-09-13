import sounddevice as sd
import soundfile as sf
import numpy as np
#import wave
import os
from datetime import datetime


class FileSearch():
    def __init__(self, directory):
        self.directory = directory

    def search_files(self,keyword):
        matched_files = []
        for root,dirs,files in os.walk(self.directory):
            print(f"현재 디렉토리 : {root}")
            print("하위 디렉토리 :", dirs)
            print("파일 목록 :", files) 
            
            for file in files:
                if keyword in file:
                    matched_files.append(os.path.join(root,file))
        return matched_files


# 마이크 목록 확인
def list_device():
    devices = sd.query_devices()

    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
          print (f"{idx}: device {idx} : {device['name']} max_input_channels : {device['max_input_channels']} max_output_channels : {device['max_output_channels']} ")
   
if __name__ == "__main__":

    str_input = (input("검색할 파일명을 입력하세요 :" ))
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fs = FileSearch(file_dir)
    result = fs.search_files(str_input)
    print("검색된 파일 목록 :")
    print("-" * 30)
    for file in result:
        print(f"{file}")
    print("-" * 30)
    