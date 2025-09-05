# import zipfile
# import itertools
# import time
# import string
# from multiprocessing import Pool, cpu_count
# import numpy as np
# import os

# def try_password(args):
#     zip_file_path, password = args
#     try:
#         with zipfile.ZipFile(zip_file_path) as zip_file:
#             zip_file.extractall(pwd=password.encode())
#         return password
#     except:
#         return None

# def chunk_passwords(chars, length, chunks):
#     # 가능한 모든 조합 생성
#     total_combinations = len(chars) ** length
#     chunk_size = total_combinations // chunks
    
#     # 각 청크의 시작과 끝 인덱스 계산
#     for i in range(chunks):
#         start = i * chunk_size
#         end = start + chunk_size if i < chunks - 1 else total_combinations
#         yield (start, end)

# def index_to_password(index, chars, length):
#     # 인덱스를 비밀번호로 변환
#     password = ''
#     base = len(chars)
#     for _ in range(length):
#         password = chars[index % base] + password
#         index //= base
#     return password

# def process_chunk(args):
#     zip_file_path, start_idx, end_idx, chars, length = args
    
#     for idx in range(start_idx, end_idx):
#         password = index_to_password(idx, chars, length)
#         try:
#             with zipfile.ZipFile(zip_file_path) as zip_file:
#                 zip_file.extractall(pwd=password.encode())
#             return password, idx
#         except:
#             if idx % 10000 == 0:  # 진행상황 출력
#                 print(f"Process ID: {os.getpid()} - Trying: {password}")
#     return None

# def unlock_zip_parallel(zip_file_path="emergency_storage_key.zip", password_length=6):
# #def unlock_zip_parallel(zip_file_path="input_log_1.zip", password_length=6):
#     start_time = time.time()
#     chars = string.digits + string.ascii_lowercase
    
#     # CPU 코어 수 확인
#     num_processes = cpu_count()
#     print(f"Using {num_processes} CPU cores")
    
#     # 작업 청크 생성
#     chunks = list(chunk_passwords(chars, password_length, num_processes))
    
#     # 각 프로세스에 전달할 인자 생성
#     args = [(zip_file_path, chunk[0], chunk[1], chars, password_length) 
#             for chunk in chunks]
    
#     # 멀티프로세싱 실행
#     with Pool(processes=num_processes) as pool:
#         for result in pool.imap_unordered(process_chunk, args):
#             if result is not None:
#                 password, attempts = result
#                 elapsed_time = time.time() - start_time
                
#                 print("\n비밀번호 찾음!")
#                 print(f"비밀번호: {password}")
#                 print(f"시도 횟수: {attempts}")
#                 print(f"소요 시간: {elapsed_time:.2f}초")
                
#                 # 비밀번호를 파일에 저장
#                 with open("password.txt", "w") as f:
#                     f.write(password)
                
#                 return password
    
#     print("비밀번호를 찾지 못했습니다.")
#     return None

# if __name__ == "__main__":
#     import os
#     print("ZIP 파일 비밀번호 해킹을 시작합니다...")
#     print("비밀번호는 숫자와 소문자 알파벳으로 구성된 6자리입니다.")
#     print(f"사용 가능한 CPU 코어 수: {cpu_count()}")
#     result = unlock_zip_parallel()



import multiprocessing as mp
import time
from datetime import datetime
from io import BytesIO
import os

import pyzipper

PWD_LEN = 6
ALPHANUM = 'abcdefghijklmnopqrstuvwxyz0123456789'
NUMALPHA = '0123456789abcdefghijklmnopqrstuvwxyz'
BASE = len(NUMALPHA)
TOTAL_CASE = BASE**PWD_LEN  # 36^6
file_dir= os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_dir,"emergency_storage_key.zip")
output_file = os.path.join(file_dir,"password.txt")



def extract_zip_file(file_path, password):
    extract_dir = os.path.splitext(file_path)[0]
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)
    
    try:
        with pyzipper.AESZipFile(file_path, 'r') as zip_file:
            print("\n 압축 파일 내용 : ")
            for file in zip_file.namelist():
                print(f" - {file}")
            zip_file.extractall(extract_dir, pwd=password.encode('utf-8'))
            print(f"\n 파일이 성공적으로 해제 되었습니다.")
            print(f"압축해제 위치 : {extract_dir}")
    except Exception as e:
            print(f"압축 해제 중 오류 발생 : {e}")

def create_password(index: int) -> str:
    tmp = ['a'] * PWD_LEN
    for i in range(PWD_LEN - 1, -1, -1):
        index, r = divmod(index, BASE)
        tmp[i] = ALPHANUM[r]
    return ''.join(tmp)


def search_smallest_file(zf):
    return min(zf.infolist(), key=lambda x: x.file_size).filename


def is_unzipped(zf, file, pwd) -> bool:
    try:
        zf.read(file, pwd=pwd.encode('utf-8'))
        return True
    except Exception:
        return False


def unlock_zip(args):
    file_content, start, end = args
    zf = None
    start_time = time.time()

    try:
        zf = pyzipper.AESZipFile(BytesIO(file_content))
        smallest = search_smallest_file(zf)
        cnt = 0
        for i in range(start, end + 1):
            pwd = create_password(i)

            cnt += 1

            if i % 100000 == 0:
                elapsed_time = time.time() - start_time
                print(
                    f'PID {mp.current_process().pid}: 시도 횟수 {cnt}, 현재 암호 {pwd}, 경과 시간 {elapsed_time:.2f}초'
                )

            if is_unzipped(zf, smallest, pwd):
                elapsed_time = time.time() - start_time
                print(
                    f'PID {mp.current_process().pid}에서 암호 발견: {pwd} (시도 횟수: {cnt}, 경과 시간: {elapsed_time:.2f}초)'
                )
                return pwd
    except KeyboardInterrupt:
        return None
    finally:
        if zf is not None:
            try:
                zf.close()
            except:
                pass
    return None


def calculate_ranges(file_content, workers=6) -> list[tuple]:
    term = TOTAL_CASE // workers
    ranges = []
    for i in range(workers):
        start = term * i
        end = TOTAL_CASE - 1 if i == workers - 1 else term * (i + 1) - 1
        ranges.append((file_content, start, end))
    return ranges


def save_password_to_file(pwd: str, filename: str = 'password.txt'):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pwd)
        print(f'{output_file}에 암호가 저장되었습니다.')
    except Exception as e:
        print(f'암호를 파일로 저장하는데 오류가 발생했습니다: {e}')


def main():
    #file_path = 'Course5/Step1/emergency_storage_key.zip'
    workers = 6

    with open(file_path, 'rb') as f:
        file_content = f.read()

    ranges = calculate_ranges(file_content, workers)

    found = None
    pool = None

    # 시작 시간 기록
    start_time = time.time()
    start_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'암호 해독 시작: {start_datetime}')
    print(f'총 {TOTAL_CASE:,}개의 조합을 {workers}개 프로세스로 시도합니다.')
    print('-' * 50)

    try:
        with mp.Pool(processes=workers) as pool:
            for res in pool.imap_unordered(unlock_zip, ranges):
                if res is not None:
                    found = res
                    pool.terminate()
                    break

        total_elapsed = time.time() - start_time
        end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print('-' * 50)
        print(f'암호 해독 종료: {end_datetime}')
        print(f'총 소요 시간: {total_elapsed:.2f}초')
        print(f'발견된 암호: {found}')

        if found:
            save_password_to_file(found)
            extract_zip_file(file_path, found)
        else:
            print('암호를 찾지 못했습니다.')

    except KeyboardInterrupt:
        total_elapsed = time.time() - start_time
        end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('\n' + '-' * 50)
        print('Keyboard Interrupt Detected')
        print(f'중단 시간: {end_datetime}')
        print(f'진행 시간: {total_elapsed:.2f}초')
        if pool is not None:
            try:
                pool.terminate()
                pool.join()
            except:
                pass


if __name__ == '__main__':
    main()

