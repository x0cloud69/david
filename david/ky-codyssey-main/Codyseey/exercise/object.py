import os
import re
import datetime
import json

def read_log():
      file_dir   = os.path.dirname(os.path.abspath(__file__))
      file_src   = 'mission_computer_main.log'
      file_path = os.path.join(file_dir,file_src)
      with open(file_path,'r',encoding='utf-8') as f:
             return f.read()
def validate_timestamp(timestamp):
  pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
  if not re.match(pattern, timestamp):
    return False
  try:
    datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
    return True
  except ValueError:
    return False
  
def parse_log_without_event(log_text):
     lines = log_text.strip().split('\n')
     result = []
     
     if not lines or len(lines) <= 1:
       raise ValueError("파일이 비어있습니다")
     header = lines[0].split(',')
     if len(header) < 3 or header[0] != 'timestamp' or header[1] != 'event' or header[2] != 'message':
       raise ValueError("헤더가 올바르지 않습니다.")
     
     for i in range(1,len(lines)): # 헤더제외
         parts = lines[i].split(',',2)
         if len(parts) >=3:
            timestamp = parts[0].strip()
            message   = parts[2].strip()

            if not validate_timestamp(timestamp):
              raise ValueError(f"Timestamp 형식이 올바르지 않습니다 : {timestamp}")
            result.append([timestamp,message])
     return result

def convert_tuple_to_dictionary(result_tuple):
   result_dict_list = []
   dict_key = ['timestamp','message']
   for item in result_tuple:
      result_dict = dict(zip(dict_key,item))
      result_dict_list.append(result_dict)
   result_json1 = json.dumps(result_dict_list,ensure_ascii=False,indent=4)
   return result_json1

if __name__ == "__main__":
    result = None  # result 변수를 미리 초기화
    
    try:
      src_list = read_log()
      print(src_list)
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
       print("파싱 결과:")
       print(result)
    except Exception as e:
       print(f"파싱 오류가 발생했습니다. : {e}")
       
    if result:  # result가 존재할 때만 실행
        try:
           result_tuple = tuple(result)
           print("Tuple 변환 결과:")
           print(result_tuple)
        except Exception as e:
           print(f"Tuple 변환오류가 발생 했습니다, {e}")
           
        # 리스트를 시간 역순으로 출력
        try:
           result.sort(key=lambda x:x[0],reverse=True)
           print("시간 역순 정렬 결과:")
           print(result)
        except Exception as e:
           print(f"시간 역순 정렬 오류가 발생 했습니다. {e}")

        # 튜플을 딕셔너리로 변환
        try:
           result_json = convert_tuple_to_dictionary(result_tuple)
           print("딕셔너리 변환 결과:")
           print(result_json)
        except Exception as e:
           print(f"딕셔너리 변환 오류가 발생 했습니다. {e}")
       
