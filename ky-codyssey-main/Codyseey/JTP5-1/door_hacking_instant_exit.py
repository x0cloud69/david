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

# 즉시 종료 플래그
instant_exit = False

# 시그널 핸들러 함수 (즉시 종료)
def signal_handler(signum, frame):
    global success, instant_exit
    print('\n\n[즉시 종료] Ctrl+C 감지! 프로그램을 즉시 종료합니다...')
    instant_exit = True
    success = True
    stop_flag.set()
    print("[즉시 종료] 1초 후 강제 종료...")
    
    # 1초 후 강제 종료
    def force_exit():
        time.sleep(1)
        os._exit(0)
    
    exit_thread = threading.Thread(target=force_exit)
    exit_thread.daemon = True
    exit_thread.start()

stop_flag = threading.Event()

# 상대 경로로 변경
script_dir = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(script_dir, 'emergency_storage_key.zip')

# 파일 존재 확인
if not os.path.exists(zip_path):
    print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
    exit(1)

seq_lock = threading.Lock()
result_lock = threading.Lock()
print_lock = threading.Lock()

def print_status(message):
    with print_lock:
        print(message)

def result(temp_pwd, seq, start_time, end_time, elapsed):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "password.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(temp_pwd)

def try_password(password):
    global success, seq, instant_exit
    
    # 즉시 종료 체크
    if instant_exit or stop_flag.is_set():
        return False
    
    with seq_lock:
        seq += 1
        current_seq = seq
    
    try:
        # 즉시 종료 재체크
        if instant_exit:
            return False
            
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            if instant_exit:
                return False
                
            extract_folder = "extracted_files"
            os.makedirs(extract_folder, exist_ok=True)
            encode_pwd = password.encode()
            
            try:
                zip_file.extractall(extract_folder, pwd=encode_pwd)
                return True
            except (zipfile.BadZipFile, RuntimeError):
                if current_seq % 1000 == 0:
                    print_status(f"진행중... 반복횟수: {current_seq}, 현재 시도 비밀번호: {password}")
                return False
    except Exception as e:
        if not instant_exit:  # 종료 중이 아닐 때만 에러 출력
            print_status(f"Error trying password {password}: {str(e)}")
        return False

def password_worker(password_queue, worker_id):
    global success, temp_pwd, instant_exit
    
    print_status(f"작업자 {worker_id} 시작됨")
    
    while not success and not stop_flag.is_set() and not instant_exit:
        try:
            current_pwd = password_queue.get(timeout=0.01)  # 매우 짧은 타임아웃
        except:
            if stop_flag.is_set() or instant_exit:
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
                    print_status(f"\n암호가 해제 되었습니다!")
                    result(temp_pwd, seq, start_time, end_time, elapsed)
                    print_status("="*30)
                    print_status(f"암호 : {temp_pwd}")
                    print_status(f"시도 횟수 : {seq}")
                    print_status(f"시작시간 : {start_time}")
                    print_status(f"종료시간 : {end_time}")
                    print_status(f"총 소요시간 : {elapsed}")
                    print_status("="*30)
            break
        password_queue.task_done()
    
    print_status(f"작업자 {worker_id} 종료됨")

def unlock_zip():
    global success, instant_exit
    print_status("비밀번호 해독 시작...")
    print_status(f"시작 시간: {start_time}")
    print_status(f"대상 파일: {zip_path}")
    
    password_queue = Queue(maxsize=10000)
    total_combinations = len(base_pwd) ** 6
    print_status(f"총 시도할 비밀번호 조합 수: {total_combinations:,}")
    
    thread_count = 8
    print_status(f"생성할 스레드 수: {thread_count}")
    threads = []
    
    def password_generator():
        try:
            for pwd in itertools.product(base_pwd, repeat=6):
                if success or stop_flag.is_set() or instant_exit:
                    break
                password_queue.put(''.join(str(x) for x in pwd))
        except:
            pass
    
    generator_thread = threading.Thread(target=password_generator)
    generator_thread.daemon = True
    generator_thread.start()
    
    try:
        for i in range(thread_count):
            t = threading.Thread(target=password_worker, args=(password_queue, i+1))
            t.daemon = True
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
            
    except KeyboardInterrupt:
        print_status("\n프로그램이 강제 종료 되었습니다")
        success = True
        stop_flag.set()
        instant_exit = True
        
    finally:
        if not success:
            print_status("\n비밀번호를 찾지 못했습니다.")
        print_status("프로그램을 종료합니다.")

if __name__ == "__main__":
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    print("Ctrl+C로 즉시 종료할 수 있습니다.")
    try:
        unlock_zip()
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
        sys.exit(0)


