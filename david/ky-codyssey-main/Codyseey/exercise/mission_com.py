import os
import pandas as pd


file_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_dir,'mission_computer_main.log')

try:
  with open(file_name,'r',encoding='utf-8') as fp:
    file_content = fp.read()
    print(file_content)
except FileNotFoundError:
    print(f"File Not Found : {file_name}")
except UnicodeDecodeError:
    print(f"Un-Code Error : {file_name}")
except Exception as e:
    print(f"Error {e}")
    
print("=== 리스트 객체로 전환 ===")

file_list = []

with open(file_name,'r',encoding='utf-8') as fp:
	for clean_file in fp:
		clean_file = clean_file.strip()
		delimeter_file = clean_file.split(',')
		file_list.append(delimeter_file)
	file_list.sort(key=lambda x:x[0],reverse=True)
	print(file_list)
 
print("---- 리스트 객체를 사전객체로 전환 -----")

file_dict = []
keys = ['timestamp','Info','message']

for item in file_list:
	dict_content = dict(zip(keys,item))
	file_dict.append(dict_content)
print(file_dict) 

print("----저장된 사전객체를 json 파일로 저장----")

import json
file_src    = "mission_computer_main.json"
file_name = os.path.join(file_dir,file_src)

with open(file_name,'w',encoding = 'utf-8') as fp:
		json.dump(file_dict,fp,ensure_ascii=False,indent=4)
 
 
print("------로그 파일을 분석하여 사고원인을 추론 -----")

json_log = []
try: 
	with open(file_name,'r',encoding='utf-8') as fp:
		json_log = json.load(fp)
except FileNotFoundError:
	print("해당 파일이 존재 하지 않습니다.")
except Exception as e:
	print(f"오류가 발생하였습니다. : {e}")

sorted_log = sorted(json_log, key=lambda x:x['timestamp'], reverse = False)

print(sorted_log)

without_header_log = []
for i,log in enumerate(sorted_log):
	if log['timestamp'] != 'timestamp':
		without_header_log.append(log)

critical_keyword = ['unstable','explosion','powered down']

critical_log = []
for i,log in enumerate(without_header_log):
	for critical_word in critical_keyword:
		if(critical_word in log['message']):
			critical_log.append(log)

print("############# Critical Log #############")
print(critical_log)
############# md 파일로 최종 보고서 작성 #####################

file_source = "anlysis_report.md"
file_name   = os.path.join(file_dir,file_source)
with open(file_name,'w',encoding='utf-8') as fd:
	fd.write("##  최종보고서\n")
	fd.write("------- 작성자 : 송근영 ----------\n")
	for i,item in enumerate(critical_log):
		fd.write(f"{item['timestamp']},{item['message']}\n")
