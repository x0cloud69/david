import os
import zipfile
import csv

file_dir = os.path.dirname(os.path.abspath(__file__))
file_src = 'Mars_Base_Inventory_List.csv'
zip_src = 'mars_base.zip'

file_path = os.path.join(file_dir,file_src)
zip_path = os.path.join(file_dir,zip_src)

# zip 파일 풀기

with zipfile.ZipFile(zip_path,'r') as zf:
	zf.extractall()



# file 읽기
# list 로 변환
mars_list = []
above_07_list = []
with open(file_path,'r',encoding='utf-8') as fd:
  str_strip = fd.read().strip()
  for str in str_strip.split('\n'):
      str_csv = str.split(',')
      mars_list.append(str_csv)
  print(mars_list)
  mars_list.sort(key=lambda x:x[4], reverse=False)
  print("-----sort -----")
  print(mars_list)
  print("----- Flammablity ------")
  for str in mars_list:
    if str[4] != 'Flammability':
      if float(str[4]) >= 0.7:
        above_07_list.append(str)
  print(above_07_list)

### 파일로 저장 ###
file_src = 'Mars_Base_Inventory_dangerous.csv'
file_bin = 'Mars_Base_Inventory_dangerous.bin'

file_name = os.path.join(file_dir,file_src)
with open(file_name,'w',newline='',encoding='utf-8') as fd:
   writer=csv.writer(fd)
   writer.writerows(above_07_list)

#### bin  파일로 저장 (읽을때는 load)
import pickle
file_name = os.path.join(file_dir,file_bin)
with open(file_name,'wb') as fd:
    pickle.dump(above_07_list,fd)
   
### Byte 파일로 저장 
# 데이터 준비
data = b"Hello, this is byte data."

# byte 파일로 저장
with open("data.bytes", "wb") as file:
    file.write(data)

# 파일 읽기 및 이진수로 출력
with open("data.bytes", "rb") as file:
    byte_data = file.read()
    binary_representation = ' '.join(format(byte, '08b') for byte in byte_data)
    print(binary_representation)  # 출력: 각 바이트의 이진수 표현
  
