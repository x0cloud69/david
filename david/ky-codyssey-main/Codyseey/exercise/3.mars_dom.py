import os
import zipfile
import pandas as pd

# zip 파일해제

file_dir = os.path.dirname(os.path.abspath(__file__))
zip_file = os.path.join(file_dir,'mars_base.zip')

with zipfile.ZipFile(zip_file) as zf:
  zf.extractall(file_dir)

########################
# CSV 파일 읽기
########################

file_path = os.path.join(file_dir,'Mars_Base_Inventory_List.csv')

with open(file_path,'r',encoding = 'utf-8') as fp:
  file_content = pd.read_csv(fp)

print(file_content)
