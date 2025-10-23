import zipfile
import os

# 1. zip file 풀기
def extract_zip(path):
   zip_folder = os.path.dirname(path)
   with zipfile.ZipFile(path,"r") as zp:
      zp.extractall(zip_folder)

# 2. File 읽기
def read_log(file):
    with open(file,"r",encoding='utf-8') as f:
         return f.read()

# 3. List 객체로 변환
def convert_log_list(file):
     file_list = []
     file = file.strip().split('\n')
     for i in range(len(file)):
         file_src = list(file[i].split(','))
         file_list.append(file_src)
     return file_list

# 4. Flammability 값으로 sorting
def sorted_list(file_list):
    file_sorted = sorted(file_list[1:], key=lambda x:x[4], reverse = True)
    return file_sorted

         
     
if __name__ == "__main__":
    zip_path = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\mars_base.zip"
    file     = "C:\\codyssey\\david\\ky-codyssey-main\\Codyseey\\exercise\\Mars_Base_Inventory_List.csv"

    try:
      extract_zip(zip_path)
      f_log = read_log(file)
      print(f_log)
      file_list = convert_log_list(f_log)
      print(file_list)
      file_sorted = sorted_list(file_list)
      print("====Sorted====")
      print(file_sorted)
    except FileNotFoundError:
      print("File NotFoundError")


   