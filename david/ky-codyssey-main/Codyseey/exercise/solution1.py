path = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log"

def read_log(path) -> str:
      try:
         with open(path,"r",encoding='utf-8') as f:
                return f.read()
      except FileNotFoundError:
           raise 
      except UnicodeDecodeError:
          raise
      except PermissionError:
          raise
      except IsADirectoryError:  
          raise
      except Exception:
          raise Exception("File 읽는 중 오류가 발생 했습니다")
  

def main():
# 1. log Data 읽기
   try:
      f_log = read_log(path)
      print(f_log)
# 2: Event 컬럼 제외, Timestamp, 헤더 길이 check, >> 튜플 로 출력
      f_list = f_log.strip().splitlines()
      f_header = f_list[0].split(',',2)
 
      if f_header != ['timestamp','event','message']:
         raise Exception
      if len(f_header) != 3:
         raise Exception
      
      f_tuple = []
      for str in f_list[1:]:
         try:
            timestamp,_,message = str.strip().split(',',2)
         except ValueError:
            raise ValueError
        #  print(timestamp,message)
         if len(timestamp) != 19:
            raise ValueError
         f_tuple.append((timestamp,message))
      print(f_tuple)
# 3. Sort 
      try:
        f_sorted = sorted(f_tuple, key=lambda x:x[0],reverse=True)
        print(f_sorted)
        f_dict     = dict(f_sorted)
        print(f_dict)
      except Exception:
        raise Exception("Process Error.")
   except FileNotFoundError:
     print("File Not Found Error : ")
     return
   except UnicodeDecodeError:
     print("UnicodeDecodeError : ")
     return
   except (PermissionError, IsADirectoryError):
     print("Permission Error or Directory Error")
     return
   except ValueError:
     print("invalid log format")
     return
   except Exception as e:
     print(e)
     return
   


if __name__=='__main__':
   main()