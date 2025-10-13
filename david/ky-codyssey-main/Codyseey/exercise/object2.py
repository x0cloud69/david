import os
import re
import datetime

def read_log():
      file_dir   = os.path.dirname(os.path.abspath(__file__))
      file_src   = 'mission_computer_main.log'
      file_path = os.path.join(file_dir,file_src)
      with open(file_path,'r',encoding='utf-8') as f:
             return f.read()

def conver_log_tuple(log_data):
     log_data = log_data.strip()
     log_data = log_data.split("\n")
     return log_data

def validate_date(timestamp):
     timestamp = timestamp.strip()
     pattern      = r'^\d{4}-\d{2}-\d{2} \d{2}\d{2}\d{2}$'
     if not re.match(timestamp,pattern):
        return False
     try:
        datetime.datetime.striptime(timestamp,'%Y-%m-%d %H-%M-%S')
        return True
     except ValueError:
        return False

def conver_without_event_tuple(log_data):
     head=[]
     wo_event_tuple=[]
     log_data = log.strip()
     log_data = log.split("\n")
     if len(log_data) <= 1:
        raise ValueError("파일이 비어있습니다.")
     header = log_data[0].split(",")
     if head[0].strip() != 'timestamp' or head[1].strip !='event' or head[2].strip != 'message':
        raise ValueError("헤더가 올바르지 않습니다.")

     for i in range(1,len(log_data)):
        parts = log_data[i].split(',',2)
        if len(parts) >=3 :
           timestamp = parts[0].strip()
           message    = parts[2].strip()
           # 형식점검 함수 호출
           if not validate_date(timestamp):
              raise ValueError(f"Timestamp 형식오류: {timestamp}")
        wo_event_tuple.append([timestamp,message])
     return wo_event_tuple
        


# main 호출
if __name__ == ("__main__"):
   # 1. 파일 그대로 읽기
     try:
        log_data = read_log()
        print(log_data)
     except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
     except PermissionError:
        print("권한이 없습니다.")
     except IsADirectoryError:
        print("파일경로 오류")
     except UnicodeDecodeError:
        print("UniCode 변환 에러")
     except Exception as e:
        print(f"오류 발생 : {e}")

   # 2.리스트를 튜플로 변환
     log_tuple = conver_log_tuple(log_data)
     print(log_tuple)

   #3. event 없이 리스트 로 변환
     try:
        without_event_tuple = conver_without_event_tuple(log_data)
        print(without_event_tuple)
     except Exception as e:
        print(f"오류가 발생 했습니다. :{e}")
     
     
   

