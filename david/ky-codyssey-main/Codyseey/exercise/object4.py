def read_log():
    try:
       with open("C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log", "r", encoding="utf-8") as f:
           return f.read()
    except FileNotFoundError:
         print("File Not Found")
         return None
    except PermissionError:
        print("Permission Error")
        return None
    except IsADirectoryError:
        print("Directory Not Found")
        return None
    except UnicodeDecodeError:
        print("UniCode Error")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None



###############################################
# 2. 원본 >> 튜플로 변환, 
# chk 1. title 3개 미만, timestamp, event, message 점검
# chk 2. event 제외 , 
# chk 3. datetime format 점검
# chk 4. Error Check
###############################################

def validate_header(header):
     if len(header) != 3:
        raise ValueError("Header Meassage 가 3개가 아닙니다.")
     if header[0] != 'timestamp':
        raise ValueError("Title 의 timestamp 제목이 다릅니다.")
     if header[1] != 'event':
        raise ValueError("Title 의 event 제목이 다릅니다.")
     if header[2] != 'message':
        raise ValueError("Title의 message 제목이 다릅니다.")
     return True

import datetime 

def f_list_without_event(f_list):
     f_list_final=[]
     for idx in range(len(f_list)):
          try:
             f_list_item = f_list[idx].strip().split(',')
             # timestamp, message만 저장 (event 제외)
             f_list_final.append([f_list_item[0],f_list_item[2]])
          except (Exception,IndexError):
             raise ValueError("Append Error")
          
          try:
            # f_list_item[0]이 timestamp이므로 이를 검증
            datetime.datetime.strptime(f_list_item[0],'%Y-%m-%d %H:%M:%S')
          except Exception:
            raise ValueError("DateTime Conversion Error")
             
     return f_list_final
     
      
def convert_log_to_tuple(f_raw):
     f_list = f_raw.strip().split('\n')
     header = f_list[0].strip().split(',')
     validate_header(header)
     # event title 제외
     f_list_final = f_list_without_event(f_list[1:])
     return f_list_final

################################   
# 3. 튜플 객체를 시간 순으로 정렬
################################
def sorted_tuple(f_list):
    try:
     f_list_sorted =  tuple(sorted(f_list,key=lambda x:x[0], reverse=False))
     return f_list_sorted
    except Exception:
       raise ValueError("Sorted Error")
    
################################
# 4. 튜플 객체를 딕셔너리 객체로 변환
################################

def convert_log_dict(f_list):
    dict_key = ['timestamp','message']
    f_list_dict = []

    try:
       for i in range(len(f_list)):
            f_list_lines = dict(zip(dict_key,f_list[i]))
            f_list_dict.append(f_list_lines)
    except Exception:
       raise ValueError("Invalid Convert to tuple")
    return f_list_dict
    
if __name__ == "__main__":     
   f_raw = read_log()
   # 1. 원본 그대로 출력 , Error 처리 
   if f_raw is not None:
      print(f_raw)

   try:
      f_list = tuple(convert_log_to_tuple(f_raw))
      if not f_list:
         raise ValueError("Conversion Event Error")
      print(f_list)
      f_list_sorted =sorted_tuple(f_list)
      print(f_list_sorted)
      f_list_dict = convert_log_dict(f_list)
      print(f_list_dict)
   except ValueError as e:
      print(f"{e}")
         


   

