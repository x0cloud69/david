import random
import os 
from datetime import datetime
import csv

env_values_mean = {}


class DummySensor:
    def __init__(self,internal_temperature,external_temperature,internal_humidity,external_illuminance,internal_co2,internal_oxygen):
        self.env_values = {
            'Date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'mars_base_internal_temperature' :0,
            'mars_base_external_temperature':0,
            'mars_base_internal_humidity':0,
            'mars_base_external_illuminance':0,
            'mars_base_internal_co2':0,
            'mars_base_internal_oxygen':0
            }
    def set_env(self):
        self.env_values['mars_base_internal_temperature']=round(random.uniform(18,30), 3)
        self.env_values['mars_base_external_temperature']=round(random.uniform(0,21), 3)
        self.env_values['mars_base_internal_humidity']=random.randint(50,60)
        self.env_values['mars_base_external_illuminance']=round(random.uniform(500,715), 3)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02,0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4,7), 3)
        # 날짜 업데이트
        self.env_values['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ###################################################
    # 보너스 과제 : log 파일 저장
    # CSV.DictWriter 사용
    ###################################################

    def get_env(self):
        # 현재 스크립트 위치 기준으로 파일 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(script_dir, "mars_base_log.csv")
        
        # CSV 파일로 저장
        with open(log_file_path, 'w', newline='', encoding='utf-8') as file:
            header_names = ['Date','mars_base_internal_temperature','mars_base_external_temperature','mars_base_internal_humidity','mars_base_external_illuminance','mars_base_internal_co2','mars_base_internal_oxygen']
            writer = csv.DictWriter(file, fieldnames=header_names)
            writer.writeheader()
            writer.writerow(self.env_values)
       
        print(f"로그 파일이 저장되었습니다: {log_file_path}")
        return self.env_values

ds=DummySensor(0,0,0,0,0,0)
ds.set_env()
env_values=ds.get_env()
for key,value  in env_values.items():
    if isinstance(value, float):
        print(f"{key}: {value:.3f}")
    else:
        print(f"{key}: {value}") 
