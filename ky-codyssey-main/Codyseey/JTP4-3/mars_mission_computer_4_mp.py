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
import multiprocessing

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
            
        return load_data
      
    
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
        # DummySensor 인스턴스 생성
        ds = DummySensor(0,0,0,0,0,0)
        
        # 센서 데이터 수집 (한 번만 실행)
        ds.set_env()  # 먼저 환경값 설정
        ds_env_values = ds.get_env()  # 환경값 가져오기
        
        # ds의 환경값을 MissionComputer의 env_values에 복사
        self.env_values = ds.env_values.copy()
        self.result_log.append(self.env_values.copy()) # 로그 저장
        
        print("센서 데이터 (JSON):")
        print(json.dumps(self.env_values, indent=4, ensure_ascii=False))
        print("-" * 50)
        
        return self.env_values
            
            
def run_computer_1():
    """첫 번째 컴퓨터 인스턴스 실행 - 시스템 정보"""
    print(f"[프로세스 {os.getpid()}] runComputer1 시작 - 시스템 정보 수집")
    computer = MissionComputer(0,0,0,0,0,0)
    computer.get_mission_computer_info()
    print(f"[프로세스 {os.getpid()}] runComputer1 완료")

def run_computer_2():
    """두 번째 컴퓨터 인스턴스 실행 - 시스템 부하"""
    print(f"[프로세스 {os.getpid()}] runComputer2 시작 - 시스템 부하 모니터링")
    computer = MissionComputer(0,0,0,0,0,0)
    computer.get_mission_computer_load()
    print(f"[프로세스 {os.getpid()}] runComputer2 완료")

def run_computer_3():
    """세 번째 컴퓨터 인스턴스 실행 - 센서 데이터"""
    print(f"[프로세스 {os.getpid()}] runComputer3 시작 - 센서 데이터 수집")
    computer = MissionComputer(0,0,0,0,0,0)
    ds = DummySensor(0,0,0,0,0,0)
    computer.get_sensor_data()
    print(f"[프로세스 {os.getpid()}] runComputer3 완료")

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
    print("멀티프로세스 MissionComputer 실행 시작")
    print(f"메인 프로세스 ID: {os.getpid()}")
    
    # 멀티프로세스로 3개 인스턴스 실행
    process1 = multiprocessing.Process(target=run_computer_1, name="runComputer1")
    process2 = multiprocessing.Process(target=run_computer_2, name="runComputer2")
    process3 = multiprocessing.Process(target=run_computer_3, name="runComputer3")
    
    # 모든 프로세스 시작
    print("프로세스들을 시작합니다...")
    process1.start()
    process2.start()
    process3.start()
    
    # 모든 프로세스가 완료될 때까지 대기
    print("모든 프로세스가 완료될 때까지 대기 중...")
    process1.join()
    process2.join()
    process3.join()
    
    print("모든 프로세스가 완료되었습니다!")
    print("프로그램을 종료합니다...")