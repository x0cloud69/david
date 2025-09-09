import zipfile
import itertools
import time
import string
from multiprocessing import Pool, cpu_count, Queue, Process, Manager
from threading import Thread
from queue import Empty
import os
from concurrent.futures import ThreadPoolExecutor
import numpy as np

class PasswordCracker:
    def __init__(self, zip_file_path="emergency_storage_key.zip", password_length=6, 
                 n_processes=None, n_threads_per_process=4):
        self.zip_file_path = zip_file_path
        self.password_length = password_length
        self.chars = string.digits + string.ascii_lowercase
        self.n_processes = n_processes or cpu_count()
        self.n_threads_per_process = n_threads_per_process
        self.found_password = None
        self.start_time = None

    def generate_password_chunks(self):
        """비밀번호 조합을 청크 단위로 생성"""
        total_combinations = len(self.chars) ** self.password_length
        chunk_size = total_combinations // (self.n_processes * self.n_threads_per_process)
        
        for i in range(self.n_processes * self.n_threads_per_process):
            start = i * chunk_size
            end = start + chunk_size if i < (self.n_processes * self.n_threads_per_process - 1) else total_combinations
            yield (start, end)

    def index_to_password(self, index):
        """인덱스를 비밀번호 문자열로 변환"""
        password = ''
        base = len(self.chars)
        remaining = index
        for _ in range(self.password_length):
            password = self.chars[remaining % base] + password
            remaining //= base
        return password

    def try_password(self, password):
        """단일 비밀번호 시도"""
        try:
            with zipfile.ZipFile(self.zip_file_path) as zf:
                zf.extractall(pwd=password.encode())
            return True
        except:
            return False

    def password_tester_thread(self, password_queue, result_queue, thread_id):
        """비밀번호 테스트를 수행하는 스레드"""
        while True:
            try:
                password = password_queue.get(timeout=1)
                if password is None:
                    break
                
                if self.try_password(password):
                    result_queue.put(password)
                    return
                
                if thread_id % self.n_threads_per_process == 0 and password_queue.qsize() % 1000 == 0:
                    elapsed = time.time() - self.start_time
                    print(f"Thread {thread_id}: Trying {password}, "
                          f"Elapsed: {elapsed:.2f}s")
                
            except Empty:
                break
            except Exception as e:
                print(f"Error in thread {thread_id}: {e}")

    def password_generator_process(self, start_idx, end_idx, password_queue, result_queue, process_id):
        """비밀번호를 생성하고 테스트하는 프로세스"""
        threads = []
        
        # 스레드 풀 생성
        for i in range(self.n_threads_per_process):
            thread = Thread(target=self.password_tester_thread,
                          args=(password_queue, result_queue, process_id * self.n_threads_per_process + i))
            thread.start()
            threads.append(thread)

        # 비밀번호 생성 및 큐에 추가
        for idx in range(start_idx, end_idx):
            if not result_queue.empty():  # 다른 프로세스가 비밀번호를 찾은 경우
                break
            password = self.index_to_password(idx)
            password_queue.put(password)

        # 종료 신호 전송
        for _ in range(self.n_threads_per_process):
            password_queue.put(None)

        # 모든 스레드 종료 대기
        for thread in threads:
            thread.join()

    def crack(self):
        """비밀번호 크래킹 실행"""
        self.start_time = time.time()
        print(f"Starting password cracking with {self.n_processes} processes "
              f"and {self.n_threads_per_process} threads per process")

        with Manager() as manager:
            result_queue = manager.Queue()
            processes = []
            
            chunks = list(self.generate_password_chunks())
            
            # 각 프로세스별로 작업 시작
            for i, (start, end) in enumerate(chunks):
                password_queue = manager.Queue(maxsize=10000)  # 큐 크기 제한
                
                p = Process(target=self.password_generator_process,
                          args=(start, end, password_queue, result_queue, i))
                p.start()
                processes.append(p)

            # 결과 대기
            found_password = None
            while any(p.is_alive() for p in processes):
                try:
                    found_password = result_queue.get(timeout=0.1)
                    break
                except Empty:
                    continue

            # 모든 프로세스 종료
            for p in processes:
                p.terminate()
                p.join()

            if found_password:
                elapsed_time = time.time() - self.start_time
                print(f"\n비밀번호 찾음: {found_password}")
                print(f"소요 시간: {elapsed_time:.2f}초")
                
                # 비밀번호 저장
                with open("password.txt", "w") as f:
                    f.write(found_password)
                
                return found_password
            
            print("비밀번호를 찾지 못했습니다.")
            return None

if __name__ == "__main__":
    # 시스템의 CPU 코어 수 확인
    cpu_cores = cpu_count()
    print(f"시스템의 CPU 코어 수: {cpu_cores}")
    
    # 크래커 인스턴스 생성 및 실행
    cracker = PasswordCracker(
        n_processes=cpu_cores,  # CPU 코어 수만큼 프로세스 생성
        n_threads_per_process=4  # 각 프로세스당 4개의 스레드 사용
    )
    
    print("ZIP 파일 비밀번호 해킹을 시작합니다...")
    print("비밀번호는 숫자와 소문자 알파벳으로 구성된 6자리입니다.")
    
    result = cracker.crack()
