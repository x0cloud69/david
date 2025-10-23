def read_log(path: str = 'mission_computer_main.log') -> str:
    try:
        # with open(path, 'r', encoding='utf-8') as f:
        with open("C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log", "r", encoding="utf-8") as f:
           return f.read()
    except FileNotFoundError:
            raise
    except UnicodeDecodeError:
            raise
    except PermissionError:
            raise
    except Exception:
           raise

def main():
# 1. log 파일 출력
  try:
     f_log = read_log()
     print(f_log)
# 2. event 제외, 리스트 객체로 변환
     f_part = f_log.strip().splitlines()
     f_list = list()
     header= f_part[0].strip().split(',',2) #헤더 검증
     if len(header) != 3 or header != ['timestamp','event','message']:
       raise ValueError
     for line in f_part[1:]:
       parts=line.strip().split(',',2)
       timestamp,_,message = parts
       if len(timestamp) != 19:
         raise ValueError
       f_list.append((timestamp,message))
     print(f_list)
# 3. timestamp 기준 정렬
     try: 
       f_sorted = sorted(f_list,key=lambda x:x[0],reverse=True)
       print(f_sorted)
     except (ValueError,IndexError):
       raise
     except Exception:
       raise
# 4. 딕셔너리 객체로 변환
     try:
       f_dict = dict(f_sorted)
       print(f_dict)
     except Exception:
       raise
  except FileNotFoundError:
    print("File open error")
    return
  except UnicodeDecodeError:
    print("UnicodeDecodeError")
    return
  except PermissionError:
    print("Permission error")
    return
  except IsADirectoryError:
    print("Directory not found")
    return
  except (ValueError,IndexError):
    print("invalid log format")
    return
  except Exception:
    print("Processing Error")
    return
     
if __name__ == "__main__":
    main()