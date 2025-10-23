import random
import threading
import time
from datetime import datetime
from queue import Queue
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from collections import defaultdict


##################################################################
# 0. Class 생성 ( 1, 초기값 함수 / 2. Setdata 함수 / 3. Getdata 함수) 
# 1. Sensor Data 출력 (OutputSensor)
# 2. Print 된 Sensor Data 를 Queue 에 저장 함수

# 6. DB 접속 정보 
# 7., DB 접속 함수
# 8. Queus 저장된 내용을 DB에 저장 
# 9. Ctrl+C 클릭하면 DB 정보 읽어 오기
# A. 읽어온 데이타 graph 로 표시를 위한 DATA 가공 
# B, 가공된 DATA Graph 로 표시 하기 
##################################################################

##################################################################
# 환경 변수 저장 (DB 환경)
# Threading Event
# Queue 생성
##################################################################
MYSQL_Config = {
     'host': 'localhost',
     'user': 'root',
     'password':'1234',
     'database': 'codyssey'
     }

stop_flag = threading.Event()
sensorQ  = Queue()


#################################################################
# 0. Class 생성 ( 1, 초기값 함수 / 2. Setdata 함수 / 3. Getdata 함수) 
#################################################################
class ParmSensor:
    def __init__(self,name):   #초기값 
        self.name         = name
        self.temperature = 0 
        self.light           = 0
        self.humidity     = 0

    def Setdata(self):
        self.temperature = random.randint(20,30)
        self.light           = random.randint(5000,10000)
        self.humidity      = random.randint(40,70)

    def Getdata(self):
        return self.temperature,  self.light,  self.humidity

#################################################################
# 1. Queue 에 저장 (In_Queue) : Queue 에 저장 
#################################################################
stop_flag = threading.Event()
sensorQ  = Queue()

def In_Queue(sensor):
     while not stop_flag.is_set():
        sensor.Setdata()
        _temp_,_light_,_humi_ = sensor.Getdata()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} : Temperature - {_temp_},  Light - {_light_},   Humidity - {_humi_}")
        data = {
             'sensor_name' : sensor.name,
             'timestamp'   :  now,
             'temperature' : _temp_,
             'light'       : _light_,
             'humidity'    : _humi_
              }
     
        sensorQ.put(data)
        time.sleep(1)

#################################################################
# 2. DB 연결 함수
#################################################################
def create_mysql_connect():
     conn = None
     try:
        conn = mysql.connector.connect(**MYSQL_Config)
        if conn.is_connected():
            print("MY SQL 연결 성공")
            return conn
     except Error as e:
            print(f"MY SQL 연결 오류 : {e}")
            return None

#################################################################
# 3-A. DB Insert (Insert_data) 함수
#################################################################
def insert_data(conn,timestamp,temperature,light,humidity):
     query = """
             insert into parm_data(parm_dt, parm_temp,parm_light, parm_humi)
             value(%s, %s, %s, %s)
              """
     data_tuple = (timestamp,temperature,light,humidity)
     cursor = conn.cursor()

     try:
        cursor.execute(query,data_tuple)
        conn.commit()
        print(f"DB 저장 완료  {timestamp} - Temp : {temperature},  Light : {light},  Humidity : {humidity}")
     except Error as e:
        print(f"Insert Error : {e}")
        conn.rollback()
     finally:
        cursor.close()

#################################################################
# 3-B. DB Select (select_data) 함수
#################################################################
def select_data(conn):
     query = """
                 select parm_dt, parm_temp, parm_light, parm_humi
                       from parm_data
                """
     cursor = conn.cursor()

     try: 
        cursor.execute(query)
        selected_data = cursor.fetchall()
        print(f"총 {len(selected_data)}개의 데이터를 가져 왔습니다.")
        return selected_data
     except Error as e:
        print(f"Select Error : {e}")
        return 
     finally:
        cursor.close()


 

#################################################################
# 2. Queue 에 있는 Data 를 꺼내서 DB 에 저장 (Out_Queue) 
# 2-1. DB 연결
#################################################################
def Out_Queue():
     conn = None
     try:
       conn = create_mysql_connect()
       if conn is None:
           print("Queue Processor - MySQl 연결 실패")
           return
       while not stop_flag.is_set() or not sensorQ.empty():
           if not sensorQ.empty():
              data = sensorQ.get()
              print(f"Queue 에서 꺼냄 : {data['sensor_name']} - {data['timestamp']}")
              insert_data(conn, data['timestamp'], data['temperature'], data['light'], data['humidity'])
              sensorQ.task_done()
           else:
              time.sleep(0.1)
     except Exception as e:
         print(f"Queue Processor - 오류 : {e}")
     finally:
         if conn and conn.is_connected():
            conn.close()
         print("Queue Processpr - MySQL 연결 종료")
 
#################################################################
# 4.DB 에서 Data 출력 하여 Graph 로 출력 (draw_graph)
#################################################################
def draw_graph():
   conn = None
   conn = create_mysql_connect()
   if conn is None:
      print("Graph 생성 단계 : DB 연결 실패")
      return
   try:
      data = select_data(conn)
      if not data:
         print("Graph 생성 실패 : 데이타가 없습니다")
         return
      time_temps = defaultdict(list)
     
      for _data_ in data:
         _timestamp_   = _data_[0]
         _temperature_ = _data_[1]

         if hasattr(_timestamp_,'strftime'):
           _time_str_ = _timestamp_.strftime("%H:%M:%S")
         else:
           _time_str_ = str(_timestamp_).split()[1] if '  ' in str(_timestamp_) else str(_timestamp_)

         time_temps[_time_str_].append(_temperature_)

       #시간별 평균 계산 (시간순 정렬)
      times = sorted(time_temps.keys())
      avg_temps = [sum(time_temps[t]) / len(time_temps[t]) for t in times]
      
      # 데이터가 너무 많으면 샘플링
      if len(times) > 15:
         step = max(1, len(times) // 15)
         times = times[::step]
         avg_temps = avg_temps[::step]

      plt.figure(figsize=(15,8))
      plt.rcParams['font.family'] = 'Malgun Gothic' 
      plt.rcParams['axes.unicode_minus'] = False

      plt.plot(times, avg_temps, marker = 'o', linewidth=2, markersize=6,
                color='#FF6B6B', label='평균 온도')

      # 평균값 텍스트 표시 (5개마다)
      for i, (t, temp) in enumerate(zip(times, avg_temps)):
        #  if i % max(1, len(times) // 10) == 0:  # 최대 10개만 표시
        plt.text(t, temp, f"{temp:.1f}°C", ha='center', va='bottom', fontsize=8)

      # x축 레이블 회전 및 간격 조정
      plt.xticks(rotation=45, fontsize=8)
      plt.xlabel('시간', fontsize=10, fontweight='bold')
      plt.ylabel('평균온도 (°C)', fontsize=10, fontweight='bold')
      plt.title('시간별 센서 온도 평균', fontsize=14, fontweight='bold')
      plt.legend(fontsize=10)
      plt.grid(True, alpha=0.3, linestyle='--')
      plt.tight_layout()
      plt.show()
   except Exception as e:
     print(f"그래프 생성 오류 : {e}")
   finally:
    if conn and conn.is_connected():
       conn.close()

#################################################################
# 3.출력된 Sensor Data 를 Queue 에 저장 (QueSensor)
#################################################################
def main():
    _num_sensor_ = 5
    sensors = [ParmSensor(f"parm-{i+1}") for i in range(_num_sensor_)]

    threads = []
    for _sensor_ in sensors:
       thread = threading.Thread(
             target = In_Queue,
             args   = (_sensor_,),
             daemon = True,
             name  = _sensor_.name
            )
       thread.start()
       threads.append(thread)

    queue_thread = threading.Thread(
             target = Out_Queue,
             daemon = False,
             name="Queue Processor"
    )
    queue_thread.start() 
    threads.append(queue_thread)

    try: 
       while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("프로그램 종료 중 ...")
        stop_flag.set()  # 스레드 종료 신호 전송
        for thread in threads[:-1]:
             thread.join(timeout=2)
             print(f" {thread.name} 종료")

        reamaining = sensorQ.qsize()
        print(f"\n 큐에 남은 데이터 : {reamaining} 개")
        
        if reamaining > 0:
         print("큐 처리 대기중 ...")
         queue_thread.join(timeout=30)
         print("큐 처리 완료")
        else:
         queue_thread.join(timeout=1)
         print("\n 모든 스레드 종료 완료")
        draw_graph()



if __name__ == '__main__':
    main()