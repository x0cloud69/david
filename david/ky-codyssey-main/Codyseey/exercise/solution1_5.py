from codecs import raw_unicode_escape_decode


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
   except ValueError:
       raise
   except Exception:
       raise
      

def main():
   path = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log"
   try:
      f_log = read_log(path)
      print(f_log)
      f_tuple = f_log.strip().splitlines()
      f_header = f_tuple[0].split(',',2)
      
      if not f_tuple:
        raise ValueError    
      if len(f_header) != 3:
         raise ValueError
      if f_header != ['timestamp','event','message']:
         raise ValueError
       
      result = []
      for str in f_tuple[1:]:
          timestamp,_,message = str.split(',',2)
          if len(timestamp) != 19:
             raise ValueError
          result.append((timestamp,message))
      print(result)
      sorted_result = sorted(result,key=lambda  x:x[0] , reverse=True)
      print(sorted_result)
      dict_result = dict(sorted_result)
      print(dict_result) 
      
    
   except FileNotFoundError:
     print("File Not Found Error : ")
     return
   except UnicodeDecodeError:
     print("UniCodeDecode Error : ")
     return
   except (PermissionError,IsADirectoryError):
     print("Permision Error or Directory Error")
     return
   except ValueError:
     print("Invalid log format")
     return 
   except Exception:
     print("Process Error")
     return

if __name__ == '__main__':
   main()