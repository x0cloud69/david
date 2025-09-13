import multiprocessing
import threading
import itertools
import zipfile
from datetime import datetime
import os
import sys
from queue import Queue
import time
import signal

class PasswordCracker:
    def __init__(self, zip_path, start_char, process_id):
        self.zip_path = zip_path
        self.start_char = start_char
        self.process_id = process_id
        self.found = False
        self.base_pwd = 'abcdefghijklmnopqrstuvwxyz0123456789'
        self.lock = threading.Lock()
        self.counter = 0
        self.start_time = datetime.now()
        self.stop_flag = threading.Event()

    def generate_passwords(self, thread_id, num_threads):
        """메모리 효율적인 비밀번호 생성"""
        # 5자리 조합을 직접 생성 (메모리에 저장하지 않음)
        for combo in itertools.product(self.base_pwd, repeat=5):
            if self.found or self.stop_flag.is_set():
                break
            password = self.start_char + ''.join(combo)
            self.try_password(password, thread_id)

    def try_password(self, password, thread_id):
        if self.found or self.stop_flag.is_set():
            return

        with self.lock:
            self.counter += 1
            if self.counter % 1000 == 0:
                elapsed = datetime.now() - self.start_time
                print(f"프로세스 {self.process_id}, 스레드 {thread_id}: {self.counter:,} 시도 | {elapsed} | {password}")

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
                try:
                    zip_file.extractall(pwd=password.encode())
                    self.found = True
                    print(f"\n암호 발견! 프로세스 {self.process_id}, 스레드 {thread_id}")
                    print(f"암호: {password}")
                    print(f"시도 횟수: {self.counter:,}")
                    print(f"소요 시간: {datetime.now() - self.start_time}")
                    
                    # 결과 파일 저장
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, f"password_found_{self.process_id}.txt")
                    with open(file_path, "w") as f:
                        f.write(password)
                    return True
                except (zipfile.BadZipFile, RuntimeError):
                    pass
        except Exception as e:
            if not self.stop_flag.is_set():
                print(f"Error: {str(e)}")
        return False

    def run_with_threads(self, num_threads=4):  # 스레드 수 감소
        threads = []
        print(f"프로세스 {self.process_id} 시작 (첫 글자: {self.start_char}), {num_threads}개 스레드 사용")
        
        for i in range(num_threads):
            t = threading.Thread(target=self.generate_passwords, args=(i, num_threads))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

def signal_handler(signum, frame):
    print('\n\n[즉시 종료] Ctrl+C 감지! 모든 프로세스를 종료합니다...')
    # 모든 프로세스 종료
    for process in multiprocessing.active_children():
        process.terminate()
    sys.exit(0)

def run_process(zip_path, start_char, process_id):
    cracker = PasswordCracker(zip_path, start_char, process_id)
    cracker.run_with_threads(4)  # 스레드 수 감소

def main():
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    
    # 상대 경로로 파일 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'emergency_storage_key.zip')
    
    if not os.path.exists(zip_path):
        print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
        return

    base_pwd = 'abcdefghijklmnopqrstuvwxyz0123456789'
    num_processes = min(multiprocessing.cpu_count(), 8)  # 최대 8개 프로세스로 제한
    chunk_size = len(base_pwd) // num_processes

    processes = []
    start_time = datetime.now()
    print(f"전체 크래킹 시작: {start_time}")
    print(f"사용할 프로세스 수: {num_processes}")
    print("Ctrl+C로 언제든지 종료할 수 있습니다.")

    try:
        for i in range(num_processes):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < num_processes - 1 else len(base_pwd)
            start_chars = base_pwd[start_idx:end_idx]
            
            for char in start_chars:
                p = multiprocessing.Process(target=run_process, args=(zip_path, char, i))
                processes.append(p)
                p.start()

        for p in processes:
            p.join()
            
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Windows 지원
    main()
