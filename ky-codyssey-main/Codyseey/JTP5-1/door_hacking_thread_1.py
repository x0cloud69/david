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

class PasswordChunk:
    def __init__(self, start_char, worker_id):
        self.start_char = start_char
        self.worker_id = worker_id
        self.current_combinations = itertools.product(base_pwd, repeat=5)  # 5자리 조합 (첫 글자 제외)

    def get_next_password(self):
        try:
            combination = next(self.current_combinations)
            return str(self.start_char) + ''.join(str(x) for x in combination)
        except StopIteration:
            return None

class ZipCracker:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.success = False
        self.temp_pwd = ''
        self.seq = 0
        self.start_time = datetime.now()
        self.seq_lock = threading.Lock()
        self.result_lock = threading.Lock()
        self.print_lock = threading.Lock()
        
    def print_status(self, message):
        with self.print_lock:
            print(message)

    def try_password(self, password, chunk_id):
        with self.seq_lock:
            self.seq += 1
            current_seq = self.seq

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
                try:
                    zip_file.extractall(pwd=password.encode())
                    return True
                except (zipfile.BadZipFile, RuntimeError):
                    if current_seq % 1000 == 0:
                        elapsed = datetime.now() - self.start_time
                        self.print_status(f"청크 {chunk_id} | 시도 횟수: {current_seq:,} | 진행시간: {elapsed} | 현재: {password}")
                    return False
        except Exception as e:
            self.print_status(f"Error: {str(e)}")
            return False

    def password_worker(self, chunk):
        chunk_id = chunk.worker_id
        self.print_status(f"작업자 {chunk_id} 시작 (첫 글자: {chunk.start_char})")

        while not self.success:
            password = chunk.get_next_password()
            if password is None:
                break

            if self.try_password(password, chunk_id):
                with self.result_lock:
                    if not self.success:
                        self.success = True
                        self.temp_pwd = password
                        end_time = datetime.now()
                        elapsed = end_time - self.start_time
                        
                        self.print_status(f"\n암호를 찾았습니다!")
                        self.print_status("="*30)
                        self.print_status(f"암호: {password}")
                        self.print_status(f"시도 횟수: {self.seq:,}")
                        self.print_status(f"소요 시간: {elapsed}")
                        self.print_status("="*30)
                        
                        with open("password.txt", "w", encoding="utf-8") as f:
                            f.write(password)
                break

        self.print_status(f"작업자 {chunk_id} 종료")

    def run(self):
        self.print_status(f"비밀번호 해독 시작... ({self.start_time})")
        
        # 첫 글자별로 청크 생성 (예: 6개의 청크)
        chunks = [
            PasswordChunk(base_pwd[i], i+1) 
            for i in range(0, len(base_pwd), len(base_pwd)//6)
        ]
        
        threads = []
        for chunk in chunks:
            t = threading.Thread(target=self.password_worker, args=(chunk,))
            t.daemon = True
            threads.append(t)

        # 모든 스레드 시작
        for t in threads:
            t.start()

        try:
            # 모든 스레드 완료 대기
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            self.print_status("\n프로그램이 중단되었습니다.")
            self.success = True
            sys.exit(0)

        if not self.success:
            self.print_status("\n비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'emergency_storage_key.zip')
    
    if not os.path.exists(zip_path):
        print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
        sys.exit(1)
        
    cracker = ZipCracker(zip_path)
    try:
        cracker.run()
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
        sys.exit(0)
