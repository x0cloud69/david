import random
import platform
import os 
import ctypes
from datetime import datetime, timedelta
import csv
import json
import time 
import threading
import numpy as np
import subprocess

env_values_mean = {}

# 전역 변수를 먼저 정의
pause = False

#result_log = []
class DummySensor:
    def __init__(self,internal_temperature,external_temperature,internal_humidity,external_illuminance,internal_co2,internal_oxygen):
        self.env_values = {
            'Date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'mars_base_internal_temperature':internal_temperature,
            'mars_base_external_temperature':external_temperature,
            'mars_base_internal_humidity':internal_humidity,
            'mars_base_external_illuminance':external_illuminance,
            'mars_base_external_co2':internal_co2,
            'mars_base_internal_oxygen':internal_oxygen
        }
    def set_env(self):
        self.env_values['mars_base_internal_temperature']=round(random.uniform(18,30), 3)
        self.env_values['mars_base_external_temperature']=round(random.uniform(0,21), 3)
        self.env_values['mars_base_internal_humidity']=random.randint(50,60)
        self.env_values['mars_base_external_illuminance']=round(random.uniform(500,715), 3)
        self.env_values['mars_base_external_co2'] = round(random.uniform(0.02,0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4,7), 3)
        # 날짜 업데이트
        self.env_values['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       
    
    ###################################################
    # 보너스 과제 : log 파일 저장
    # CSV.DictWriter 사용
    ###################################################

    def get_env(self):
        # 현재 스크립트 위치 기준으로 파일 경로 설정
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # log_file_path = os.path.join(script_dir, "mars_base_log.csv")
        
        # # CSV 파일로 저장
        # with open(log_file_path, 'w', newline='', encoding='utf-8') as file:
        #     header_names = ['Date','mars_base_internal_temperature','mars_base_external_temperature','mars_base_internal_humidity','mars_base_external_illuminance','mars_base_external_co2','mars_base_internal_oxygen']
        #     writer = csv.DictWriter(file, fieldnames=header_names)
        #     writer.writeheader()
        #     writer.writerow(self.env_values)
       
        # print(f"로그 파일이 저장되었습니다: {log_file_path}")
        return self.env_values

""" ds=DummySensor(0,0,0,0,0,0)
ds.set_env()
env_values=ds.get_env()
for key,value  in env_values.items():
    if isinstance(value, float):
        print(f"{key}: {value:.3f}")
    else:
        print(f"{key}: {value}") 
 """

################################################
# 문제2 
################################################       
class MissionComputer:
    def __init__(self,internal_temperature,external_temperature,internal_humidity,external_illuminance,internal_co2,internal_oxygen):
        self.result_log = []
        self.result_log_avg = {}
        self.last_5min_check = datetime.now()
        self.env_values = {
                'mars_base_internal_temperature':internal_temperature,
                'mars_base_external_temperature':external_temperature,
                'mars_base_internal_humidity':internal_humidity,
                'mars_base_external_illuminance':external_illuminance,
                'mars_base_external_co2':internal_co2,
                'mars_base_internal_oxygen':internal_oxygen
            }
        # 설정 파일 로드
        self.settings = self.load_settings()
    
    def load_settings(self):
        """설정 파일을 로드하는 메서드"""
        settings = {}
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            setting_file_path = os.path.join(script_dir, "setting.txt")
            
            if os.path.exists(setting_file_path):
                with open(setting_file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                settings[key.strip()] = value.strip().lower() == 'true'
                print("설정 파일을 성공적으로 로드했습니다.")
            else:
                print("설정 파일이 없습니다. 기본값을 사용합니다.")
                # 기본 설정값
                settings = {
                    'system_info': True, 'cpu_info': True, 'memory_info': True, 'timestamp': True,
                    'operating_system': True, 'os_version': True, 'cpu_type': True, 'cpu_cores': True, 'total_memory': True,
                    'cpu_load': True, 'free_memory': True, 'total_visible_memory': True,
                    'sensor_data': True, 'sensor_averages': True
                }
        except Exception as e:
            print(f"설정 파일 로드 중 오류 발생: {e}")
            # 기본 설정값 사용
            settings = {
                'system_info': True, 'cpu_info': True, 'memory_info': True, 'timestamp': True,
                'operating_system': True, 'os_version': True, 'cpu_type': True, 'cpu_cores': True, 'total_memory': True,
                'cpu_load': True, 'free_memory': True, 'total_visible_memory': True,
                'sensor_data': True, 'sensor_averages': True
            }
        return settings
    

    def get_mission_computer_info(self):
        # 설정에 따라 시스템 정보 수집
        while True:
          load_data = {}
          
          if self.settings.get('operating_system', True):
              load_data['운영체제'] = platform.system()
          
          if self.settings.get('os_version', True):
              load_data['운영체제 버전'] = platform.version()
          
          if self.settings.get('cpu_type', True):
              load_data['CPU의 타입'] = platform.processor()
          
          if self.settings.get('cpu_cores', True):
              load_data['CPU의 코어수'] = os.cpu_count()
          
          if self.settings.get('total_memory', True):
              kernel32 = ctypes.windll.kernel32
              total_memory = ctypes.c_ulonglong()
              kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(total_memory))
              # KB를 GB로 변환
              memory_gb = total_memory.value / (1024 * 1024)
              load_data['메모리의 크기'] = f"{memory_gb:.2f} GB"
          
          # 타임스탬프 추가 (설정에 따라)
          if self.settings.get('timestamp', True):
              load_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          
          # 설정에 따라 출력
          
          if self.settings.get('system_info', True):
              print("시스템 정보 (JSON):")
              print(json.dumps(load_data, indent=4, ensure_ascii=False))
          else:
              print("시스템 정보 출력이 설정에서 비활성화되었습니다.")
              
          time.sleep(2)  
         # return load_data
      
    
    def get_mission_computer_load(self):
        try:
            load_data = {}
            
            if self.settings.get('cpu_load', True):
                cpu_cmd = 'wmic cpu get loadpercentage'
                cpu = subprocess.check_output(cpu_cmd,shell=True).decode()
                cpu_load = cpu.split('\n')[1].strip()
                load_data['cpu_load'] = f"{cpu_load}%"
            
            if self.settings.get('free_memory', True) or self.settings.get('total_visible_memory', True):
                mem_cmd = 'wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value'
                mem_info = subprocess.check_output(mem_cmd,shell=True).decode()
                
                # 메모리 정보 파싱
                mem_lines = mem_info.strip().split('\n')
                free_memory = "N/A"
                total_memory = "N/A"
                
                for line in mem_lines:
                    if 'FreePhysicalMemory=' in line:
                        free_memory = line.split('=')[1].strip()
                    elif 'TotalVisibleMemorySize=' in line:
                        total_memory = line.split('=')[1].strip()
                
                # 설정에 따라 메모리 정보 추가
                if self.settings.get('free_memory', True) or self.settings.get('total_visible_memory', True):
                    memory_info = {}
                    if self.settings.get('free_memory', True):
                        memory_info['free_physical_memory_kb'] = free_memory
                    if self.settings.get('total_visible_memory', True):
                        memory_info['total_visible_memory_kb'] = total_memory
                    load_data['memory_info'] = memory_info
            
            # 타임스탬프 추가 (설정에 따라)
            if self.settings.get('timestamp', True):
                load_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 설정에 따라 출력
            if self.settings.get('memory_info', True):
                print("시스템 부하 정보 (JSON):")
                print(json.dumps(load_data, indent=4, ensure_ascii=False))
            else:
                print("시스템 부하 정보 출력이 설정에서 비활성화되었습니다.")
            
            return load_data
            
        except Exception as e:
            error_data = {
                'cpu_load': "CPU 정보를 가져올 수 없습니다.",
                'memory_load': "메모리 정보를 가져올 수 없습니다.",
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print("오류 발생 (JSON):")
            print(json.dumps(error_data, indent=4, ensure_ascii=False))
            
            return error_data  
    
    def get_sensor_data(self):
        while True:  # 무한 루프로 변경
            if not pause:  # pause가 False일 때만 센서 데이터 수집
                # ds 인스턴스의 환경값을 가져와서 설정
                ds.set_env()  # 먼저 환경값 설정
                ds_env_values = ds.get_env()  # 환경값 가져오기
                
                # ds의 환경값을 MissionComputer의 env_values에 복사
                current_time = datetime.now()
                if (current_time - self.last_5min_check) > timedelta(minutes=1):
                    print("5분 경과 하여 history 초기화")
                    keys_list = list(ds_env_values.keys())
                    unique_keys = [key for key in keys_list if key != 'Date']
                    # 평균값 계산
                    values = []
                    for key in unique_keys:
                        if self.result_log:  # result_log가 비어있지 않은지 확인
                            # 해당 키의 모든 값들을 추출
                            # values = [log[key] for log in self.result_log]
                            for log in self.result_log:
                                values.append(log[key])
                            
                            
                            # 숫자형 데이터만 필터링 (Date 제외)
                            numeric_values = [v for v in values if isinstance(v, (int, float))]
                            
                            if numeric_values:  # 숫자 데이터가 있는 경우
                                self.result_log_avg[key] = round(np.mean(numeric_values), 3)
                            else:
                                self.result_log_avg[key] = "N/A"
                        else:
                            self.result_log_avg[key] = "데이터 없음"
                    
                    # 평균값 출력
                    print("각 센서별 평균값:")
                    for key, avg in self.result_log_avg.items():
                        print(f"  {key}: {avg}")
                    
                    print("처리된 키들:", unique_keys)
                    self.last_5min_check = current_time
                    self.result_log = []
                #self.env_values.update(ds_env_values)
                self.env_values = ds.env_values.copy()
                self.result_log.append(self.env_values.copy()) # 로그 저장
                print("Json으로 변환 하여 출력")
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
                print("-" * 50)
                time.sleep(5)
                print("result_log")
                print(self.result_log)
            else:
                # pause 상태일 때는 대기
                print("시스템이 일시정지되었습니다. 재시작하려면 아무 키나 누르세요...")
                time.sleep(1)
            
            
def key_input():
    global pause
    while True:
        try:
            key = input('임시 중지 : s, 종료 : q, 재시작 : 아무런 키\n')
            if key == 's':
                pause = True
                print('System stopped ...')
            elif key == 'q':
                print('System shutting down...')
                os._exit(0)
            else:
                pause = False
                print('System restarted ...')
        except KeyboardInterrupt:
            print('\n프로그램이 중단되었습니다.')
            os._exit(0)
        except Exception as e:
            print(f'오류 발생: {e}')
            continue
      
if __name__ == '__main__':
    RunComputer = MissionComputer(0,0,0,0,0,0)
    ds = DummySensor(0,0,0,0,0,0)
    
    # 모든 메서드를 스레드로 실행
    computer_info_thread = threading.Thread(target=RunComputer.get_mission_computer_info)
    computer_load_thread = threading.Thread(target=RunComputer.get_mission_computer_load)
    computer_sensor_thread = threading.Thread(target=RunComputer.get_sensor_data)
    
    # 데몬 스레드로 설정 (메인 프로그램 종료 시 함께 종료)
    computer_info_thread.daemon = True
    computer_load_thread.daemon = True
    computer_sensor_thread.daemon = True
    
    # 모든 스레드 시작
    computer_info_thread.start()
    computer_load_thread.start()
    computer_sensor_thread.start()
    
    runComputer1 = MissionComputer(0,0,0,0,0,0)
    runComputer2 = MissionComputer(0,0,0,0,0,0)
    runComputer3 = MissionComputer(0,0,0,0,0,0)
    
    
    
    # 메인 스레드가 종료되지 않도록 대기
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다...")