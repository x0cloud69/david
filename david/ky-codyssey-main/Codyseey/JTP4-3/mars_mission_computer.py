import random
import os 
from datetime import datetime
import json
import sys
import time
import threading
import csv

env_values_mean = {}


class DummySensor:
    def __init__(self,internal_temperature,external_temperature,internal_humidity,external_illuminance,internal_co2,internal_oxygen):
        self.env_values = {
            'Date' : datetime.now().strftime("%Y=%m-%d %H:%M:%S"),
            'mars_base_internal_temperature':internal_temperature,
            'mars_base_external_temperature':external_temperature,
            'mars_base_internal_humidity':internal_humidity,
            'mars_base_external_illuminance':external_illuminance,
            'mars_base_internal_co2':internal_co2,
            'mars_base_internal_oxygen':internal_oxygen
        }
    def set_env(self):
        self.env_values['mars_base_internal_temperature']=random.uniform(18,30)
        self.env_values['mars_base_external_temperature']=random.uniform(0,21)
        self.env_values['mars_base_internal_humidity']=random.randint(50,60)
        self.env_values['mars_base_external_illuminance']=random.uniform(500,715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02,0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4,7)
    
    ###################################################
    # 보너스 과제 : log 파일 저장
    # CSV.DictWriter 사용
    ###################################################

    def get_env(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_file = (
            f"Date :  {current_time} \n"
            f"mars_base_internal_temperature : {self.env_values['mars_base_internal_temperature'] : .2f} \n"
            f"mars_base_external_temperature : {self.env_values['mars_base_external_temperature'] : .2f} \n"
            f"mars_base_internal_humidity : {self.env_values['mars_base_internal_humidity'] : .2f} \n"
            f"mars_base_external_illuminance : {self.env_values['mars_base_external_illuminance'] : .2f} \n"
            f"mars_base_internal_co2 : {self.env_values['mars_base_internal_co2'] : .2f} \n"
            f"mars_base_internal_oxygen : {self.env_values['mars_base_internal_oxygen'] : .2f} \n"
        )

        file_path = os.path.join("C:\\", "codyssey", "david", "ky-codyssey-main", "Codyseey", "JTP4-3", "mars_base_log.csv")
        with open(file_path,'w',encoding='utf-8') as file:
            header_names = ['Date','mars_base_internal_temperature','mars_base_external_temperature','mars_base_internal_humidity','mars_base_external_illuminance','mars_base_internal_co2','mars_base_internal_oxygen']
            writer = csv.DictWriter(file,fieldnames=header_names)
            writer.writeheader()
            writer.writerow(self.env_values)
       

        return self.env_values

ds=DummySensor(0,0,0,0,0,0)
ds.set_env()
env_values=ds.get_env()

for key,value  in env_values.items():
    print(f"{key}:{value}") 

###################################################################
# 문제 2. 미션 컴퓨터 제작
###################################################################
""" 
class MissionComputer:
    def __init__(self):
        self.ds = DummySensor(0,0,0,0,0,0)

    
    def get_sensor_data(self):
        try:
            while not pause:
                self.ds.set_env()

                #env_values 값에 저장
                self.ds.env_values = self.ds.get_env()

                #Json 으로 저장 
                print("\n 문제2. Json 으로 변환 하여 출력 \n")
                print(json.dumps(self.ds.env_values,indent=4, ensure_ascii=False))
                time.sleep(2)
        #     return self.ds.env_values
        except KeyboardInterrupt:
            print("프로그램 종료")
        except Exception as e:
            print(f"\n 오류 발생 : {e}")

#RunComputer = MissionComputer() # 인스턴스 생성
#RunComputer.get_sensor_data() # 메서드 호출

###################################################
# 보너스 과제
# 1. Key_Press == "S"  => "System stoped…", "G" => 계속
# 2. 5분에 한번씩 5분 평균값 
###################################################

pause = False

# Key 입력을 감지 하는 함수
def check_input():
    global pause,computer
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            pause = True
            print("System Stopped ...")
        elif user_input.lower() == 'x':
            print("프로그램 종료 합니다")
            os._exit(0) #프로그램 즉시 종료
        else:
            if pause:
                pause = False
                print("System restarted ....")

# 
def run_mission_computer():
    global pause
    computer = MissionComputer()
    computer.get_sensor_data()

    while True:
        if not pause:
            computer.get_sensor_data()

if __name__ == "__main__":
    print("멀티 스레트를 시작합니다")
    print("q 를 입력하면 일시중지, 재시작 하려면 아무 키나 클릭하세요")

    #입력 감시 스레스 생성 및 시작
  
    input_thread = threading.Thread(target=check_input)
    input_thread.daemon = True
    input_thread.start()

    run_mission_computer()
   """