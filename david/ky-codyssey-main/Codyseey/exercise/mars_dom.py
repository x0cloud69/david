import os
import numpy as np

file_dir   = os.path.dirname(os.path.abspath(__file__))
file_001 = 'mars_base_main_parts-001.csv'
file_002 = 'mars_base_main_parts-002.csv'
file_003 = 'mars_base_main_parts-003.csv'

file_name_001 = os.path.join(file_dir,file_001)
file_name_002 = os.path.join(file_dir,file_002)
file_name_003 = os.path.join(file_dir,file_003)


arr1,arr2,arr3 = [],[],[]
parts           = []

arr1 = np.genfromtxt(file_name_001,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')
arr2 = np.genfromtxt(file_name_002,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')
arr3 = np.genfromtxt(file_name_003,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')


parts = np.vstack((arr1,arr2,arr3))
# print('---- parts ---')
# print(parts)

# 1단계 : Unique Item 도출 #
unique_item = np.unique(parts[:,0])
# print("--- 분석할 고유 항목 목록 ---")
# print(unique_item)

# 2단계 : np array 초기화
parts_means = np.zeros((len(unique_item),2),dtype=object)
parts_means[:,0]=unique_item
# print("Parts 초기화")
# print(parts_means)

#3단계 : part_means np array 에 평균값 계산하여 등록 하기
for index, item in enumerate(unique_item):
     matching_parts = parts[parts[:,0]==item]
     
     if matching_parts.size > 0:
           matching_values = matching_parts[:,1].astype(float)
           matching_avg    = np.mean(matching_values)
           print(matching_avg)
           parts_means[index,1]= round(matching_avg,2)

#4단계  평균값이 50 미만만 인 항목만 필터링
filtered_parts = parts_means[parts_means[:,1].astype(float)<50]

print(filtered_parts) 