import os
import json

filename = 'mission_computer_main.log'
file_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(file_dir,filename)

try:
  with open(file_path,'r',encoding='utf-8') as fp:
    file_content = fp.read()
    print(file_content)
except FileNotFoundError:
  print(f"Error : {file_path} 파일을 찾을수 없습니다")
except UnicodeDecodeError:
  print(f"Error : {file_path} 파일을 디코딩하는 중 오류가 발생했습니다")
except Exception as e:
  print(f"Error : {file_path} 파일 오류가 있습니다 {str(e)}")
  
  
  ##########################
  
def read_log(file_path):
  with open(file_path,'r',encoding='utf-8') as fp:
    return fp.read()
  
  
log_list = []
log_list_1 = []
print("=" * 100)
with open(file_path,'r',encoding='utf-8') as fp:
  for line in fp:
   log_list.append(line.strip()) 
log_list=tuple(log_list)
print(log_list)
print("====REVERSE=====")
#og_list.reverse()
#print(log_list)

####################### 객체로 변환 ##################

temp_list = []

for log in log_list:
  date_time,info,content = log.strip().split(",")
  log_entry = {'date_time':date_time,'info':info,'content':content}
  temp_list.append(log_entry)
  temp_list.sort(key=lambda x: x['date_time'],reverse=True)
  # 딕셔너라 생성
  
log_dict = {}
for idx,log in enumerate(temp_list[1:],start=1):
  log_dict[idx] = log
  
print("log dictionary")  
print(log_dict)

file_path_json = os.path.join(file_dir,'mission_computer_main.json')
with open(file_path_json,'w',encoding='utf-8') as fp:
    json.dump(log_dict,fp,ensure_ascii=False,indent=4)
  
json_list = json.dumps(log_dict,ensure_ascii=False,indent=4)
print("Jason List 형태")
print(json_list)

with open(file_path_json,'r',encoding='utf-8') as fp:
  log_dict = json.load(fp)
  print("Jason 형태")
  print(log_dict)

  
####################
# DataFrame 
####################

import pandas as pd

with open(file_path,'r',encoding='utf-8') as fp:
  df = pd.read_csv(fp)
  print(df)
  print("=" * 100)
  
####################
# 시작시간 
####################

start_time = df['timestamp'].min()
end_time   = df['timestamp'].max()
#avg_time   = df['timestamp'].mean()

describe_time = df['timestamp'].describe()

print(f"시작시간: {start_time}")
print(f"종료시간: {end_time}")
#print(f"평균시간: {avg_time}")
print(describe_time)
print(f"전체 step 수: {describe_time['count']}")

decribe_content = df['message'].describe()
print(decribe_content)

print("=" * 100)

####################
# 사고 원인 추론
####################

accident_item = 'explosion|shutdown|failure|anomaly|down|emergency'

expected_risk = df['message'].str.contains(accident_item)
print("############# Expected Risk #############")
print(df[expected_risk])
print("################ Expected Risk End #############")

a_content = df[['timestamp','message']]

print(a_content)

####################
# .loc 사용(이름 기반 선택)
############################

print(".loc 사용")
b_content = df.loc[30:31,['timestamp','message']]
print(b_content)

#######################
# .loc 조건 
#######################

print(".loc 조건 사용")
b_content = df.loc[df['message'].str.contains('unstable'),['timestamp','message']]
print(b_content)

print("=" * 100)

######################
# .iloc 사용(위치 기반 선택)
######################
print(".iloc 사용")
b_content = df.iloc[:,[1,2]]
print(b_content)

path_file = os.path.join(file_dir,'accident_report.md')
with open(path_file,'w',encoding='utf-8') as fp:
  fp.write(f"# 사고 보고서 \n\n")
  fp.write(f"## 사고 원인 추론 \n\n")
  fp.write(f"{b_content}")
  