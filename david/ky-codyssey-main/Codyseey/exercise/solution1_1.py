def read_log(path: str = 'mission_computer_main.log') -> str:
     with open(path, "r", encoding="utf-8") as f:
          return f.read()
     
def main():
    path = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log"
    try:
       # 1. log 파일 읽기
       f_log = read_log(path)
       print(f_log)

       # 2. log event 삭제, title 점검, timestamp 점검 , 리스트 객체로 변환
       f_str = f_log.strip().splitlines()
       if not f_str or f_str[0] != 'timestamp,event,message':
          raise ValueError
       f_list = list()
       for parts in f_str[1:]:
            items = parts.strip().split(',',2)
            if len(items) != 3:
               raise ValueError
            timestamp,_,message = items
            if len(timestamp) != 19:
               raise ValueError 
            else:
               f_list.append((timestamp,message.strip()))
       print(f_list)

       # 3. 시간 역순 출력
       try:
          f_sorted = sorted(f_list,key=lambda x:x[0], reverse = True)
          print(f_sorted)
       # 4. Dictionary 변환
          f_dict   = dict(f_sorted)
          print(f_dict)
       except:
            print("Processing Error")
            return
    except FileNotFoundError:
         print("File Not Found")
         return
    except UnicodeDecodeError:
         print("UniCodeError")
         return
    except PermissionError:
         print("Permission Error")
         return
    except IsADirectoryError:
         print("Dircectory Error")
         return 
    except ValueError:
         print("Value Error")
         return
    except Exception as e:
         print(f"{e}")
         return 

if __name__ == ('__main__'):
    main()