import zipfile
import os
from datetime import datetime 
import threading
from queue import Queue
import itertools
import time
import signal
import sys

base_pwd = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


temp_pwd = ''
seq = 0
success = False
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
start_time_period = datetime.now()
elapsed = 0


# 상대 경로로 변경
script_dir = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(script_dir, 'emergency_storage_key.zip')
extract_folder = os.path.join(script_dir, 'extracted_files')
#zip_path = os.path.join(script_dir, 'input_log_1.zip')

# 파일 존재 확인
if not os.path.exists(zip_path):
    print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
    exit(1)

seq_lock = threading.Lock()
result_lock = threading.Lock()
print_lock = threading.Lock()  # 출력을 위한 새로운 락 추가

def print_status(message):
    with print_lock:
        print(message)

def result(temp_pwd, seq, start_time, end_time, elapsed):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "password.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        # file.write("="*30+"\n")
         file.write(temp_pwd)
        # file.write(f"시도횟수 : {seq}\n")
        # file.write(f"시작시간 : {start_time}\n")
        # file.write(f"종료시간 : {end_time}\n")
        # file.write(f"총 소요시간 : {elapsed}\n")
        # file.write("="*30+"\n")

def try_password(password):
    global success, seq
    

    elapsed = datetime.now() - start_time_period
    with seq_lock:
        seq += 1
        current_seq = seq
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # stop_flag 재체크

                
            #extract_folder = "extracted_files"
            os.makedirs(extract_folder, exist_ok=True)
            encode_pwd = password.encode()
            
            try:
                zip_file.extractall(extract_folder, pwd=encode_pwd)
                return True
            except (zipfile.BadZipFile, RuntimeError):
                # 1000번마다 진행상황 출력
                if current_seq % 1000 == 0:
                    print_status(f"시작시간 : {start_time} 시도 횟수: {current_seq:,} | 진행시간: {str(elapsed)} | 현재 비밀번호: {password}")
                return False
    except Exception as e:
        print_status(f"Error trying password {password}: {str(e)}")
        return False

def password_worker(password_queue, worker_id):
    global success, temp_pwd
    
    print_status(f"작업자 {worker_id} 시작됨")
    
    while not success:
        try:
            # 타임아웃을 1초로 증가하여 안정성 향상
            current_pwd = password_queue.get(timeout=1.0)
        except:
            if success:  # 성공했으면 종료
                break
            continue
            
        if try_password(current_pwd):
            with result_lock:
                if not success:
                    success = True
                    temp_pwd = current_pwd
                    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    end_time_period = datetime.now()
                    elapsed = end_time_period - start_time_period
                    print_status(f"\n암축이 해제 되었습니다!")
                    result(temp_pwd, seq, start_time, end_time, elapsed)
                    print_status("="*30)
                    print_status(f"암호 : {temp_pwd}")
                    print_status(f"시도 횟수 : {seq}")
                    print_status(f"시작시간 : {start_time}")
                    print_status(f"종료시간 : {end_time}")
                    print_status(f"총 소요시간 : {elapsed}")
                    print_status("="*30)
            break
        password_queue.task_done()  # 항상 task_done 호출
    
    print_status(f"작업자 {worker_id} 종료됨")  # 작업자 종료 메시지

def unlock_zip():
    global success
    print_status("비밀번호 해독 시작...")
    print_status(f"시작 시간: {start_time}")
    print_status(f"대상 파일: {zip_path}")
    
    # 메모리 효율적인 비밀번호 생성
    password_queue = Queue(maxsize=10000)  # 큐 크기 제한
    
    # 총 조합 수 계산 (미리 계산)
    total_combinations = len(base_pwd) ** 6
    print_status(f"총 시도할 비밀번호 조합 수: {total_combinations:,}")
    
    # 스레드 생성 및 시작
    thread_count = 8
    print_status(f"생성할 스레드 수: {thread_count}")
    threads = []
    
    # 비밀번호 생성 스레드
    def password_generator():
        try:
            count = 0
            for pwd in itertools.product(base_pwd, repeat=6):
                if success:  # 성공 시 즉시 종료
                    break
                password_queue.put(''.join(str(x) for x in pwd))
                count += 1
                
                # 10000개마다 진행상황 출력
                if count % 10000 == 0:
                    print_status(f"비밀번호 생성 진행: {count:,}개 생성됨")
        except Exception as e:
            print_status(f"비밀번호 생성 중 오류: {e}")
    
    # 생성기 스레드 시작
    generator_thread = threading.Thread(target=password_generator)
    generator_thread.daemon = True
    generator_thread.start()
    
    try:
        # 작업자 스레드들 시작
        for i in range(thread_count):
            t = threading.Thread(target=password_worker, args=(password_queue, i+1))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # 모든 스레드가 완료될 때까지 대기
        for t in threads:
            t.join()
            
    except KeyboardInterrupt:
        print_status("\n프로그램이 강제 종료 되었습니다")
        success = True
    
        
    finally:
        if not success:
            print_status("\n비밀번호를 찾지 못했습니다.")
        print_status("프로그램을 종료합니다.")

if __name__ == "__main__":
    try:
        unlock_zip()
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
        sys.exit(0)
