import zipfile
import itertools
import time
import string

def unlock_zip(zip_file_path="emergency_storage_key.zip"):
    # 시작 시간 기록
    start_time = time.time()
    
    # 사용할 문자 집합 정의 (숫자와 소문자 알파벳)
    chars = string.digits + string.ascii_lowercase
    
    # ZIP 파일 열기
    zip_file = zipfile.ZipFile(zip_file_path)
    
    # 시도 횟수를 추적하기 위한 카운터
    attempt_count = 0
    
    # 6자리 모든 가능한 조합에 대해 시도
    for password_length in [6]:  # 6자리로 고정
        for guess in itertools.product(chars, repeat=password_length):
            attempt_count += 1
            guess = ''.join(guess)
            
            # 현재 진행 상황 출력 (1000번 시도마다)
            if attempt_count % 1000 == 0:
                elapsed_time = time.time() - start_time
                print(f"시도 횟수: {attempt_count}, 현재 비밀번호: {guess}, "
                      f"경과 시간: {elapsed_time:.2f}초")
            
            try:
                # ZIP 파일의 비밀번호 시도
                zip_file.extractall(pwd=guess.encode())
                
                # 성공한 경우
                elapsed_time = time.time() - start_time
                print("\n비밀번호 찾음!")
                print(f"비밀번호: {guess}")
                print(f"시도 횟수: {attempt_count}")
                print(f"소요 시간: {elapsed_time:.2f}초")
                
                # 비밀번호를 파일에 저장
                with open("password.txt", "w") as f:
                    f.write(guess)
                
                return guess
            
            except:
                continue
    
    # 비밀번호를 찾지 못한 경우
    print("비밀번호를 찾지 못했습니다.")
    return None

if __name__ == "__main__":
    print("ZIP 파일 비밀번호 해킹을 시작합니다...")
    print("비밀번호는 숫자와 소문자 알파벳으로 구성된 6자리입니다.")
    result = unlock_zip()
