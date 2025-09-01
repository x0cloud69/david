import random
import os 
from datetime import datetime, timedelta
import csv
import json
import time 
import threading
import numpy as np

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
                print(json.dumps(ds.env_values, indent=4, ensure_ascii=False))
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
    print("프로그램 시작...")
    print("'s': 일시정지, 'q': 종료, 기타키: 재시작")
    
    # 입력 스레드 시작
    input_thread = threading.Thread(target=key_input)
    input_thread.daemon = True
    input_thread.start()
    
    # 잠시 대기하여 입력 스레드가 준비되도록 함
    time.sleep(1)
    
    ds = DummySensor(0,0,0,0,0,0)
    RunComputer = MissionComputer(0,0,0,0,0,0)
    RunComputer.get_sensor_data()
