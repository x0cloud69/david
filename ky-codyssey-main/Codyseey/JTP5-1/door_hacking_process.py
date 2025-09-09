import zipfile
import itertools
import time
import string
from multiprocessing import Pool, cpu_count
import numpy as np

def try_password(args):
    zip_file_path, password = args
    try:
        with zipfile.ZipFile(zip_file_path) as zip_file:
            zip_file.extractall(pwd=password.encode())
        return password
    except:
        return None

def chunk_passwords(chars, length, chunks):
    # 가능한 모든 조합 생성
    total_combinations = len(chars) ** length
    chunk_size = total_combinations // chunks
    
    # 각 청크의 시작과 끝 인덱스 계산
    for i in range(chunks):
        start = i * chunk_size
        end = start + chunk_size if i < chunks - 1 else total_combinations
        yield (start, end)

def index_to_password(index, chars, length):
    # 인덱스를 비밀번호로 변환
    password = ''
    base = len(chars)
    for _ in range(length):
        password = chars[index % base] + password
        index //= base
    return password

def process_chunk(args):
    zip_file_path, start_idx, end_idx, chars, length = args
    
    for idx in range(start_idx, end_idx):
        password = index_to_password(idx, chars, length)
        try:
            with zipfile.ZipFile(zip_file_path) as zip_file:
                zip_file.extractall(pwd=password.encode())
            return password, idx
        except:
            if idx % 10000 == 0:  # 진행상황 출력
                print(f"Process ID: {os.getpid()} - Trying: {password}")
    return None

def unlock_zip_parallel(zip_file_path="emergency_storage_key.zip", password_length=6):
    start_time = time.time()
    chars = string.ascii_lowercase + string.digits
    
    # CPU 코어 수 확인
    num_processes = cpu_count()
    print(f"Using {num_processes} CPU cores")
    
    # 작업 청크 생성
    chunks = list(chunk_passwords(chars, password_length, num_processes))
    
    # 각 프로세스에 전달할 인자 생성
    args = [(zip_file_path, chunk[0], chunk[1], chars, password_length) 
            for chunk in chunks]
    
    # 멀티프로세싱 실행
    with Pool(processes=num_processes) as pool:
        for result in pool.imap_unordered(process_chunk, args):
            if result is not None:
                password, attempts = result
                elapsed_time = time.time() - start_time
                
                print("\n비밀번호 찾음!")
                print(f"비밀번호: {password}")
                print(f"시도 횟수: {attempts}")
                print(f"소요 시간: {elapsed_time:.2f}초")
                
                # 비밀번호를 파일에 저장
                with open("password.txt", "w") as f:
                    f.write(password)
                
                return password
    
    print("비밀번호를 찾지 못했습니다.")
    return None

if __name__ == "__main__":
    import os
    print("ZIP 파일 비밀번호 해킹을 시작합니다...")
    print("비밀번호는 숫자와 소문자 알파벳으로 구성된 6자리입니다.")
    print(f"사용 가능한 CPU 코어 수: {cpu_count()}")
    result = unlock_zip_parallel()
