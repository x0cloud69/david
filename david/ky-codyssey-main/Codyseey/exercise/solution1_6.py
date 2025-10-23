def read_log(path):
   try:
      with open(path,"r",encoding = 'utf-8') as f:
           return f.read()
   except FileNotFoundError:
      raise
   except UnicodeDecodeError:
      raise
   except (PermissionError, IsADirectoryError):
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
    if len(f_header) != 3:
       raise ValueError
    if f_header != ['timestamp','event','message']:
      raise ValueError
    f_pairs=[]
    for str in f_tuple[1:]:
      timestamp,_,message = str.strip().split(',',2)
      if len(timestamp) != 19:
         raise ValueError
      f_pair = ((timestamp,message))
      f_pairs.append(f_pair)
    print(f_pairs) 
    f_sorted = sorted(f_pairs, key=lambda x:x[0], reverse=True)
    print(f_sorted)
    f_dict = dict(f_sorted)
    print(f_dict)
   
    
  except FileNotFoundError:
    print("File Not Found.")
    return
  except UnicodeDecodeError:
    print("Uncode Error")
    return
  except ValueError:
    print("Invalid log Format")
    return
  except (PermissionError, IsADirectoryError):
    print("Permission Error")
    return
  except Exception:
    print("Processing Error")
    return

if __name__ == '__main__':
    main()
    

    