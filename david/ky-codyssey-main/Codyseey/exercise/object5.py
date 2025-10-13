def read_log():

    try:
       f = open("C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mission_computer_main.log", "r", encoding="utf-8") 
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
        print({e})
        return None

f_raw = read_log()

if f_raw is not None:
  print(f_raw)
