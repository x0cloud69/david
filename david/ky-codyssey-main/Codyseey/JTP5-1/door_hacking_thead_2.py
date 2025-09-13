import itertools
import multiprocessing
from datetime import datetime
import os
import zipfile
from typing import List, Generator
import time

def get_chunk_passwords(start_idx: int, chunk_size: int, base_pwd: List) -> List[str]:
    """청크 단위로 비밀번호 생성"""
    passwords = []
    for i in range(chunk_size):
        current = start_idx + i
        pwd = []
        remaining = current
        for _ in range(6):
            pwd.append(base_pwd[remaining % len(base_pwd)])
            remaining //= len(base_pwd)
        passwords.append(''.join(str(x) for x in reversed(pwd)))
    return passwords

def try_password_chunk(args):
    """비밀번호 청크를 시도"""
    start_idx, chunk_size, zip_path, process_id, base_pwd = args
    passwords = get_chunk_passwords(start_idx, chunk_size, base_pwd)
    
    for pwd in passwords:
        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(pwd=pwd.encode())
                return pwd, start_idx
        except:
            continue
    return None

def unlock_zip():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'emergency_storage_key.zip')
    
    if not os.path.exists(zip_path):
        print(f"오류: 파일을 찾을 수 없습니다: {zip_path}")
        return

    start_time = datetime.now()
    print(f"비밀번호 해독 시작... ({start_time})")
    
    cpu_count = multiprocessing.cpu_count()
    print(f"사용 가능한 CPU 코어 수: {cpu_count}")
    
    base_pwd = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    pwd_space_size = len(base_pwd) ** 6
    chunk_size = 1000
    
    with multiprocessing.Pool(processes=cpu_count) as pool:
        total_checked = 0
        last_print_time = time.time()
        
        # 청크 단위로 작업 생성
        tasks = (
            (i * chunk_size, chunk_size, zip_path, i % cpu_count, base_pwd)
            for i in range(0, pwd_space_size // chunk_size + 1)
        )
        
        for result in pool.imap_unordered(try_password_chunk, tasks):
            total_checked += chunk_size
            
            # 1초마다 진행상황 출력
            current_time = time.time()
            if current_time - last_print_time >= 1:
                elapsed = datetime.now() - start_time
                print(f"진행 중... 시도 횟수: {total_checked:,} | 경과 시간: {elapsed} {result}")
                last_print_time = current_time
            
            if result:
                pwd, position = result
                print(f"\n비밀번호 찾음: {pwd}")
                print(f"위치: {position}")
                print(f"총 소요 시간: {datetime.now() - start_time}")
                return pwd
    
    print("비밀번호를 찾지 못했습니다.")
    return None

if __name__ == '__main__':
    unlock_zip()
