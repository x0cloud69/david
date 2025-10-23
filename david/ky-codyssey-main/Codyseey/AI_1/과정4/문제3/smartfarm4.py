import random
import threading
import time
from datetime import datetime
from queue import Queue
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from collections import defaultdict

# DB 연결 정보
MYSQL_Config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'codyssey'
}

# 큐 생성 (FIFO 구조)
sensorQ = Queue()

def create_mysql_connect():
    conn = None
    try:
        conn = mysql.connector.connect(**MYSQL_Config)
        if conn.is_connected():
            print("MySQL 연결 성공")
            return conn
    except Error as e:
        print(f"MySQL 연결 오류: {e}")
        return None

def insert_sensor_data(conn, timestamp, temperature, light, humidity):
    """센서 데이터를 DB에 삽입"""
    query = """
        INSERT INTO parm_data(parm_dt, parm_temp, parm_light, parm_humi)
        VALUES(%s, %s, %s, %s)
    """
    data_tuple = (timestamp, temperature, light, humidity)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        print(f"✓ DB 저장 완료: {timestamp} - Temp: {temperature}°C")
    except Error as e:
        print(f"Insert Error: {e}")
        conn.rollback()
    finally:
        cursor.close()

def get_sensor_data(conn):
    """테이블에서 센서 데이터 가져오기"""
    query = """
        SELECT parm_dt, parm_temp, parm_light, parm_humi
        FROM parm_data
        ORDER BY parm_dt
    """
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"총 {len(results)}개의 데이터를 가져왔습니다.")
        return results
    except Error as e:
        print(f"Select Error: {e}")
        return []
    finally:
        cursor.close()

class ParmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.light = 0
        self.humidity = 0

    def Setdata(self):
        self.temperature = random.randint(20, 30)
        self.light = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def Getdata(self):
        return self.temperature, self.light, self.humidity

stop_flag = threading.Event()

def print_sensor(sensor):
    """센서 데이터를 읽어서 큐에 저장"""
    try:
        while not stop_flag.is_set():
            sensor.Setdata()
            _temp_, _light_, _humidity_ = sensor.Getdata()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 콘솔 출력
            print(f"{now} {sensor.name} - Temp: {_temp_}°C, Light: {_light_}lux, Humidity: {_humidity_}%")
            
            # 큐에 데이터 저장 (DB 직접 저장 X)
            data = {
                'sensor_name': sensor.name,  # 출력용으로만 사용
                'timestamp': now,
                'temperature': _temp_,
                'light': _light_,
                'humidity': _humidity_
            }
            sensorQ.put(data)
            print(f"→ 큐에 저장: {sensor.name} (큐 크기: {sensorQ.qsize()})")
            
            time.sleep(1)
    except Exception as e:
        print(f"{sensor.name} - 오류: {e}")
    finally:
        print(f"{sensor.name} - 센서 스레드 종료")

def queue_processor():
    """큐에서 데이터를 꺼내서 DB에 저장하는 스레드"""
    conn = create_mysql_connect()
    if conn is None:
        print("Queue Processor - MySQL 연결 실패")
        return
    
    try:
        # stop_flag가 설정되어도 큐가 빌 때까지 처리
        while not stop_flag.is_set() or not sensorQ.empty():
            # 큐가 비어있지 않으면 데이터 꺼내기
            if not sensorQ.empty():
                data = sensorQ.get()  # FIFO: 먼저 들어온 데이터부터 꺼냄
                
                print(f"← 큐에서 꺼냄: {data['sensor_name']} - {data['timestamp']}")
                
                # DB에 저장 (sensor_name 제외)
                insert_sensor_data(
                    conn,
                    data['timestamp'],
                    data['temperature'],
                    data['light'],
                    data['humidity']
                )
                
                sensorQ.task_done()
            else:
                time.sleep(0.1)  # 큐가 비어있으면 짧게 대기
    
    except Exception as e:
        print(f"Queue Processor - 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn and conn.is_connected():
            conn.close()
        print("Queue Processor - MySQL 연결 종료")

def draw_temperature_graph():
    """시간별 온도 평균 그래프 그리기"""
    conn = create_mysql_connect()
    if conn is None:
        print("그래프 생성 실패 - MySQL 연결 불가")
        return
    
    try:
        # 데이터 가져오기
        data = get_sensor_data(conn)
        
        if not data:
            print("그래프 생성 실패 - 데이터 없음")
            return
        
        # 시간별 온도 데이터 정리
        time_temps = defaultdict(list)
        
        for row in data:
            timestamp = row[0]
            temperature = row[1]
            
            # 시간 (HH:MM:SS)만 추출
            if hasattr(timestamp, 'strftime'):
                time_str = timestamp.strftime("%H:%M:%S")
            else:
                time_str = str(timestamp).split()[1] if ' ' in str(timestamp) else str(timestamp)
            
            time_temps[time_str].append(temperature)
        
        # 시간별 평균 계산
        times = sorted(time_temps.keys())
        avg_temps = [sum(time_temps[t]) / len(time_temps[t]) for t in times]
        
        print(f"\n그래프 데이터:")
        print(f"시간대 수: {len(times)}")
        print(f"온도 범위: {min(avg_temps):.1f}°C ~ {max(avg_temps):.1f}°C")
        
        # 그래프 그리기
        plt.figure(figsize=(15, 8))
        plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 (Windows)
        # plt.rcParams['font.family'] = 'AppleGothic'  # 한글 폰트 (Mac)
        plt.rcParams['axes.unicode_minus'] = False
        
        plt.plot(times, avg_temps, marker='o', linewidth=2, markersize=8, 
                color='#FF6B6B', label='평균 온도')
        
        # 데이터 포인트에 값 표시
        for i, (t, temp) in enumerate(zip(times, avg_temps)):
            if i % 5 == 0:  # 5개마다 표시 (너무 많으면 생략)
                plt.text(t, temp, f'{temp:.1f}°C', 
                        ha='center', va='bottom', fontsize=8)
        
        plt.xlabel('시간', fontsize=12, fontweight='bold')
        plt.ylabel('평균 온도 (°C)', fontsize=12, fontweight='bold')
        plt.title('시간별 센서 온도 평균', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 그래프 저장 및 표시
        plt.savefig('sensor_temperature_graph.png', dpi=300, bbox_inches='tight')
        print("\n✓ 그래프 저장 완료: sensor_temperature_graph.png")
        plt.show()
    
    except Exception as e:
        print(f"그래프 생성 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn and conn.is_connected():
            conn.close()

def main():
    _num_sensor_ = 5
    sensors = [ParmSensor(f"Parm-{i+1}") for i in range(_num_sensor_)]
    
    # 센서 스레드 생성
    threads = []
    for _sensor_ in sensors:
        thread = threading.Thread(
            target=print_sensor,
            args=(_sensor_,),
            daemon=True,
            name=_sensor_.name
        )
        thread.start()
        threads.append(thread)
    
    # 큐 처리 스레드 생성 (daemon=False로 변경!)
    queue_thread = threading.Thread(
        target=queue_processor,
        daemon=False,  # ← 중요! False로 변경
        name="QueueProcessor"
    )
    queue_thread.start()
    threads.append(queue_thread)
    
    print(f"\n{'='*60}")
    print(f"센서 모니터링 시작 ({_num_sensor_}개 센서)")
    print(f"큐 기반 데이터 처리 활성화")
    print(f"Ctrl+C를 눌러 종료하세요")
    print(f"{'='*60}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n프로그램 종료 중...")
        stop_flag.set()
        
        # 센서 스레드 종료 대기 (큐 처리 스레드 제외)
        print("\n센서 스레드 종료 중...")
        for thread in threads[:-1]:  # 마지막 큐 스레드 제외
            thread.join(timeout=2)
            print(f"✓ {thread.name} 종료")
        
        # 큐에 남은 데이터 확인
        remaining = sensorQ.qsize()
        print(f"\n큐에 남은 데이터: {remaining}개")
        
        if remaining > 0:
            print("큐 처리 대기 중...")
            # 큐 처리 스레드가 모든 데이터를 처리할 때까지 대기
            queue_thread.join(timeout=30)  # 최대 30초 대기
            print("✓ 큐 처리 완료")
        else:
            queue_thread.join(timeout=2)
        
        print("\n모든 스레드 종료 완료")
        
        # 그래프 그리기
        print("\n그래프 생성 중...")
        time.sleep(1)  # 마지막 데이터 저장 대기
        draw_temperature_graph()

if __name__ == '__main__':
    main()
