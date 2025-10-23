import random
import threading
import time
from datetime import datetime

class ParmSensor:
    def __init__(self,name):
         self.name = name
         self.temperature = 0
         self.light           = 0
         self.humidity      = 0

    def Setdata(self):
         self.temperature = random.randint(20,30)
         self.light           = random.randint(5000,10000)
         self.humidity      = random.randint(40,70)

    def Getdata(self):
         return self.temperature, self.light,  self.humidity

stop_flag = threading.Event()

def print_sensor(sensor):
     while not stop_flag.is_set():
         sensor.Setdata()
         _temp_,_light_,_humi_ = sensor.Getdata()
         now = datetime.now().strftime("%H:%M:%S")
         print(f"{now} {sensor.name} - temp {_temp_}, light {_light_}, humi {_humi_}")
         time.sleep(1)  # 1초마다 출력
         
 
def main():
   _num_sensor_ = 5
   # sensor 생성
   sensors = [ParmSensor(f"Parm-{i+1}") for i in range(_num_sensor_)]
   # 스레드 생성 및 시작
   threads = []
   for _sensor_ in sensors:
       thread = threading.Thread(target=print_sensor, args=(_sensor_,), daemon=True,name = _sensor_.name)
       thread.start()
       threads.append(thread)
   try:
     while True:
          time.sleep(1)
   except KeyboardInterrupt:
      print("프로그램 종료 중 ... ")
      stop_flag.set()
      for i, thread in enumerate(threads,1):
           thread.join(timeout=2)
           print(f" [{i} / {_num_sensor_} ] {thread.name} 종료")

if __name__ == '__main__':
   main()
