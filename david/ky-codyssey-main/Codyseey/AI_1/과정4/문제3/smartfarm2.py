import random
import threading
import time
from datetime import datetime
from pynput import keyboard
import mysql.connector
from mysql.connector import Error

#DB 연결 정보
MYSQL_Config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '1234',
    'database' : 'codyssey'
}

def create_mysql_connect():
     conn = None
     try:
        conn = mysql.connector.connect(**MYSQL_Config)
        if conn.is_connected():
           print("MY SQL 연결 성공")
           return conn
     except Error as e:
           print(f"My SQL 연결 오류 : {e}")
           return None

def insert_sensor_data(conn, timestamp, temperature, light, humidity):
     query = """
                insert into parm_data(parm_dt, parm_temp, parm_light, parm_humi)
                values(%s,%s,%s,%s)
               """
     data_tuple = (timestamp, temperature, light, humidity)
     cursor = conn.cursor()
     
     try:
         cursor.execute(query,data_tuple)
         conn.commit()
     except Error as e:
         print(f"Insert Error : {e}")
         conn.rollback()
     finally:
         cursor.close()

class ParmSensor:
    def __init__(self,name):
        self.name          = name
        self.temperature = 0
        self.light           = 0
        self.humidity      = 0

    def Setdata(self):
        self.temperature = random.randint(20,30)
        self.light           = random.randint(5000,10000)
        self.humidity      = random.randint(40,70)

    def Getdata(self):
        return self.temperature, self.light, self.humidity

stop_flag = threading.Event()

def print_sendor(sensor):
     conn = create_mysql_connect()
     if conn is None:
        print(f"{sensor.name} - MySQL 연결 실패")
        return
     try:
        while not stop_flag.is_set():
            sensor.Setdata()
            _temp_,_light_,_humidity_ = sensor.Getdata()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} {sensor.name} - Temp : {_temp_}, light : {_light_}, humidity : {_humidity_}")
            insert_sensor_data(conn, now, _temp_, _light_, _humidity_)
            time.sleep(1)
     except Exception as e:
            print(f"{sensor.name} - 오류: {e}")
     finally:
            if conn.is_connected():
                conn.close()
            print(f"{sensor.name} - MySQL 연결 종료")


def main():
     _num_sensor_ = 5
     sensors = [ParmSensor(f"Parm-{i+1}") for i in range(_num_sensor_)]
     # 스레스 생성
     threads = []
     for _sensor_ in sensors:
         thread = threading.Thread(target=print_sendor, args=(_sensor_,),daemon=True, name=_sensor_.name)
         thread.start()
         threads.append(thread)
     try:
       while True:
            time.sleep(1)
     except KeyboardInterrupt:
            print("프로그램 종료 중 ...")
            stop_flag.set()
            for i, thread in enumerate(threads,1):
                 thread.join(timeout=2)
                 print(f" [{i}/{_num_sensor_}] {thread.name} 종료")

if __name__ == '__main__':
    main()



