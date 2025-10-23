path = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log"


def read_log(path) -> str:
   try:
      with open(path,"r",encoding='utf-8') as f:
             return f.read()
   except FileNotFoundError:
         raise
   except PermissionError:
         raise
   except IsADirectoryError:
         raise
   except ValueError:
         raise
   except Exception:
         raise

def main():
   try:
# 1. log Data 출력
      f_log = read_log(path)
      print(f_log)

# 2. header , timetamp , 길이 , check,  event 제외 f_tuple 로 자장
      f_data = f_log.strip().splitlines()
      f_header = f_data[0].split(',',2)
      if len(f_header) != 3:
         raise ValueError
      if f_header != ['timestamp','event','message']:
         raise ValueError
      
      f_tuple = []
      for str in f_data[1:]:
         timestamp,_,message = str.strip().split(',',2)
         if len(timestamp) != 19:
            raise ValueError

         try:
            f_tuple.append((timestamp,message))
         except Exception:
            print("Process Error")
            return
      print(f_tuple)
      try: 
         f_sorted = sorted(f_tuple,key=lambda x:x[0], reverse = True)
         print(f_sorted)
         f_dict     = dict(f_sorted)
         print(f_dict)
      except Exception:
         print("Process Error")
         return
   except FileNotFoundError:
      print("File Not FoundError")
      return
   except (PermissionError, IsADirectoryError):
      print("Persmission Error")
      return 
   except ValueError:
      print("invalid log Format Error")
      return
   except Exception as e:
      print(e)
      return
   

if __name__ == '__main__':
   main()