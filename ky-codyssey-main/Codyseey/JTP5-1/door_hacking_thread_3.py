import multiprocessing
import threading
import itertools
import zipfile
from datetime import datetime
import os
import sys
from queue import Queue
import time

class PasswordCracker:
    def __init__(self, zip_path, start_char, process_id):
        self.zip_path = zip_path
        self.start_char = start_char
        self.process_id = process_id
        self.found = False
        self.password_queue = Queue()
        self.base_pwd = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.lock = threading.Lock()
        self.counter = 0
        self.start_time = datetime.now()

    def generate_passwords(self, thread_id, num_threads):
        # 각 스레드가 담당할 부분 계산
        combinations = list(itertools.product(self.base_pwd, repeat=5))
        chunk_size = len(combinations) // num_threads
        start_idx = thread_id * chunk_size
        end_idx = start_idx + chunk_size if thread_id < num_threads - 1 else len(combinations)

        # 해당 스레드가 담당하는 부분만 생성
        for combo in combinations[start_idx:end_idx]:
            if self.found:
                break
            password = self.start_char + ''.join(combo)
            self.try_password(password, thread_id)

    def try_password(self, password, thread_id):
        if self.found:
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
                    with open(f"password_found_{self.process_id}.txt", "w") as f:
                        f.write(password)
                except:
                    pass
        except Exception as e:
            print(f"Error: {str(e)}")

    def run_with_threads(self, num_threads=6):
        threads = []
        print(f"프로세스 {self.process_id} 시작 (첫 글자: {self.start_char}), {num_threads}개 스레드 사용")
        
        for i in range(num_threads):
            t = threading.Thread(target=self.generate_passwords, args=(i, num_threads))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

def run_process(zip_path, start_char, process_id):
    cracker = PasswordCracker(zip_path, start_char, process_id)
    cracker.run_with_threads(6)  # 각 프로세스당 6개 스레드

def main():
    zip_path = 'emergency_storage_key.zip'
    if not os.path.exists(zip_path):
        print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
        return

    base_pwd = '0123456789abcdefghijklmnopqrstuvwxyz'
    num_processes = 16  # CPU 코어 수
    chunk_size = len(base_pwd) // num_processes

    processes = []
    start_time = datetime.now()
    print(f"전체 크래킹 시작: {start_time}")

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

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Windows 지원
    main()
