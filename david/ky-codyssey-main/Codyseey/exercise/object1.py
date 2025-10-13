import os
import re
import datetime

def read_log():
      file_dir = os.path.dirname(os.path.abspath(__file__))
      file_src = 'mission_computer_main.log'
      file_path = os.path.join(file_dir, file_src)
      with open(file_path, 'r', encoding='utf-8') as f:
             return f.read()

def validate_timestamp(timestamp):
    # 공백 제거
    timestamp = timestamp.strip()
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    if not re.match(pattern, timestamp):
        return False
    try:
        datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
  
def parse_log_without_event(log_text):
     lines = log_text.strip().split('\n')
     result = []
     
     if not lines or len(lines) <= 1:
       raise ValueError("파일이 비어있습니다")
     
     header = lines[0].split(',')
     if len(header) < 3 or header[0].strip() != 'timestamp' or header[1].strip() != 'event' or header[2].strip() != 'message':
       raise ValueError("헤더가 올바르지 않습니다.")
     
     for i in range(1, len(lines)): # 헤더제외
         parts = lines[i].split(',', 2)
         if len(parts) >= 3:
            timestamp = parts[0].strip()
            message = parts[2].strip()
            
            # 디버깅 출력 추가
            print(f"검증 중인 타임스탬프: '{timestamp}'")
            
            if not validate_timestamp(timestamp):
              raise ValueError(f"Timestamp 형식이 올바르지 않습니다 : {timestamp}")
            result.append([timestamp, message])
     return result

if __name__ == ("__main__"):
    try:
      src_list = read_log()
      print("로그 파일 내용의 처음 부분:")
      print(src_list[:200] + "...")  # 로그 파일의 앞부분만 출력
    except FileNotFoundError:
       print("파일이 존재 하지 않습니다.")
    except PermissionError:
       print("파일접근 권한이 없습니다.")
    except IsADirectoryError:
       print("파일경로 오류 입니다. ")
    except UnicodeDecodeError:
       print("파일 디코딩 오류 입니다. ")
    except Exception as e:
       print(f"오류가 발생하였습니다. : {e}")

    try:
       result = parse_log_without_event(src_list)
       result_tuple = tuple(result)
       print("파싱 결과:")
       print(result[:3])  # 결과의 처음 몇 개만 출력
    except Exception as e:
       print(f"오류가 발생했습니다. : {e}")
