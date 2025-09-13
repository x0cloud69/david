# print("Hello Mars")
import sys
import json
import pandas as pd
import datetime
import csv

""" 
############################################################
# mission_computer_main.log 파일을 읽어 전체 내용을 화면에 출력
# 예외 상황(파일 없음, 디코딩 오류 등)에 대비한 예외 처리 구현  
###########################################################

print("=" * 100)
print("mission_computer_main.log 파일을 읽어 전체 내용을 화면에 출력합니다.")
print("예외사항 : 파일없음, 디코딩 오류")
print("=" * 100) 

try:
    with open("c:\codyssey\david\ky-codyssey-main\Codyseey\PJT4\mission_computer_main.log","r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Error: mission_computer_main.log 파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("Error: 파일을 디코딩하는 중 오류가 발생했습니다. 파일 인코딩을 확인하세요.")
except Exception as e:
    print(f"Error: 파일을 읽는 중 오류가 발생 했습니다.{str(e)}")

print("=" * 100)
print("2. 로그 분석 log 파일 출력을 종료 합니다")
print("=" * 100)
print("\n\n" * 2)


 """


######################################################
# 로그 파일 내용을 콤마(,)를 기준으로 날짜/시간과 메시지를 분리하여 Python의 리스트(List) 객체로 전환
# 리스트 객체를 화면에 출력
# 리스트 객체를 시간 역순으로 정렬하여 출력 #
######################################################

log_list = []

try:
    with open("c:\codyssey\david\ky-codyssey-main\Codyseey\PJT4\mission_computer_main.log","r",encoding="utf-8") as file:
        next(file)
#        for line in file:
#            log_list.append(line.strip().split(","))
        log_list = list(csv.reader(file))
except FileNotFoundError:
    print("Error: mission_computer_main.log 파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    print("Error: 파일을 디코딩하는 중 오류가 발생했습니다. 파일 인코딩을 확인하세요.")
except Exception as e:
    print(f"Error: 파일을 읽는 중 오류가 발생 했습니다.{str(e)}")

print("=" * 100)
print("2. 로그 분석 log CSV 파일을 리스트 객체로 변환 ")
print("=" * 100)
print("\n\n" )   
  

print(log_list)
print("=" * 100)
print("2. 로그 분석 log 파일 출력을 종료 합니다")
print("=" * 100)
print("\n\n" * 2)

#for log in log_list:
#    print(log)

#########################################################################################
# 리스트를 sort() 메서드를 사용하여 시간 역순으로 정렬
# 정렬된 리스트를 화면에 출력
#########################################################################################    

log_list.sort(key=lambda x: x[0], reverse=True)
print("=" * 100)
print("3. 로그 분석 log 리스트 객체를 시간 역순으로 정렬 ")
print("=" * 100)
print(log_list)
print("=" * 100)


#######################################################
# 리스트 객체를 딕셔너리(Dictionary) 객체로 변환
# 딕셔너리 객체를 화면에 출력
#######################################################
log_dict = {}

#idx = 1
#for log in log_list:
#    print(log)
#    date_time, info, content = log
#    log_dict[idx]= {'date_time' : date_time,'info' : info, 'content':content}
#    idx += 1

# 딕셔너리 컴프리헨션
log_dict = {
    idx: {'date_time':date_time, 'info':info, 'content':content}
    for idx, (date_time, info,content) in enumerate(log_list, start=1)
}

""" # zip 함수 사용
keys = ['date_time', 'info','content']
log_dict = {
    idx: dict(zip(keys, log_list))
    for idx, log_list in enumerate(log_list, start=1)
} """

print("=" * 100)
print(log_dict)
print("=" * 100)

#######################################################
# log_dict를 JSON 파일로 저장   
#######################################################
with open("c:\codyssey\david\ky-codyssey-main\Codyseey\PJT4\mission_computer_main.json ", "w", encoding="utf-8") as file:
    json.dump(log_dict, file, ensure_ascii=False, indent=4)

#######################################################
# 1. 로그 파일을 분석하여 사고원인을 추론
#    1-1. 전체 step 몇개인지 확인
#    1-2. 각 step별로 어떤 내용인지 확인
#    1-3. 사고가 발생한 step을 확인
#######################################################

accident_item = ['explosion', 'mission', 'Oxygen', 'powered down', 'error', 'failure', 'malfunction', 'shutdown', 'emergency', 'anomaly']

with open("c:\codyssey\david\ky-codyssey-main\Codyseey\PJT4\mission_computer_main.json", "r", encoding="utf-8") as file:
    logs_data = json.load(file)
#log_data = sorted(logs_data, key=lambda x:x['date_time'],reverse=False)
# DataFrome 생성
df=pd.DataFrame.from_dict(logs_data, orient='index',columns=['date_time','content']).reset_index()
df = df.sort_values(by='date_time',ascending=False)

                     

# 로그 시작시간, 종료시간, 전체 step 수
start_time = df['date_time'].min()
start_time_content = df[df['date_time'] == start_time]['content'].iloc[0]
print(f"시작시간: {start_time}, 내용: {start_time_content}")
end_time = df['date_time'].max()
end_time_content = df[df['date_time'] == end_time]['content'].iloc[0]
print(f"종료시간: {end_time}, 내용: {end_time_content}")
total_steps = len(df)
print(f"전체 step 수: {total_steps}")
print("=" * 100)

expected_risk = df[df['content'].str.contains('|'.join(accident_item))]

print(f"사고 원인으로 추정되는 로그 항목: \n {expected_risk}")

today = datetime.date.today().strftime("%Y-%m-%d")

with open("c:\codyssey\david\ky-codyssey-main\Codyseey\PJT4\log_analysis.md", "w", encoding="utf-8") as file:
    file.write('<center>\n\n')
    file.write('# 제목 : 로그 분석 결과\n')
    file.write('## 부제목 : 사고 원인 추론\n\n\n\n')
    file.write('### 작성자 : 송근영 \n')
    file.write(f'### 날짜 : {today}\n')   
    file.write('<center>\n\n')
    file.write('\n<div style="page-break-after: always;"></div>\n\n')

    # 목차
    file.write('## 목차 \n\n')
    file.write('1. 개요 \n')
    file.write('2. 로그 분석 결과 \n')
    
    file.write('\n<div style="page-break-after: always;"></div>\n\n')


    # 개요
    file.write('## 1. 개요 \n\n')
    file.write('| 항목 |\n')  # 테이블 헤더
    file.write('|:---|\n')  # 왼쪽 정렬 지정
    file.write(f'|로그 시작시간: {start_time},     내용: {start_time_content}|\n')
    file.write(f'|로그 종료시간: {end_time},     내용: {end_time_content}|\n')
    file.write(f'|전체 step 수: {total_steps}|\n')
    file.write('\n<div style="page-break-after: always;"></div>\n\n')


    # 예상 위험 요소


    file.write('## 2.로그 분석 결과 \n\n')
    file.write('| 사고 원인으로 추정되는 로그 항목 |\n')  # 컬럼 헤더
    file.write('|:---|\n')  # 가운데 정렬 지정
    file.write(f'|{expected_risk}|\n')  # 내용




    


