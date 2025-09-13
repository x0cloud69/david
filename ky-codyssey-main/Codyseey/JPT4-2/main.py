import csv
import sys

file_path = 'C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_List.csv'

###########################################################
# CSV 피일을 List Comprehension 사용 (parsing)
###########################################################
comprehension_list = [line.split(',') for line in open(file_path,'r',encoding='utf-8')]
print("-" * 100)
print("Comprehension 사용하여 List 객체로 변환")
print("-" * 100)
for row in comprehension_list:
    print(row)


###########################################################
# CSV 파일을 LIST 객체로 읽기
###########################################################
with open(file_path,'r',encoding='utf-8') as file:
    csv_reader = list(csv.reader(file))
    print("-" * 100)
    print("CSV File Reader Basic Type")
    print("-" * 100)
    for row in csv_reader:
        print(row) 

###########################################################
# CSV 파일을 Dictionary 객체로 읽기
###########################################################    
with open(file_path, 'r',encoding='utf-8') as file:
    dict_reader = list(csv.DictReader(file))
    print("-" * 100)
    print("Dictionary File Read")
    print("-" * 100)
    for row in dict_reader:
        print(row)

#########################################################################################

###########################################################
# List 객체를 Sorting
###########################################################  

csv_header = csv_reader[0]
csv_data   = csv_reader[1:]

csv_sorted_data = sorted(csv_data, key=lambda x: float(x[4]), reverse=True)

print("-" * 100)
print("List 객체를 Sorting ")
print("-" * 100)

for row in csv_sorted_data:
    print(row)


###########################################################
# Dictionary 객체를 Sorting
###########################################################  
# with open(file_path, 'r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
#     data = list(reader)
#     for row in data:
#         row['Flammability'] = float(row['Flammability'])



print("=" * 100)
print("Dictionary 객체 Sorting : 내림차순")
print("=" * 100)
sort_dict_data = sorted(dict_reader, key=lambda x:float(x['Flammability']), reverse=True)
for row in sort_dict_data:
    print(row) 


###########################################################
# List 객체에서 인화성 지수가 0.7 > 인것을 Filtering
###########################################################  

print("=" * 100)
print("List 객체에서 인화성 지수가 0.7 > 인것을 Filtering")
print("=" * 100)

filter_csv_data = list(filter(lambda x: float(x[4]) > 0.7, csv_sorted_data))
for row in filter_csv_data:
    print(row)


###########################################################
# Dictionary 객체에서 인화성 지수가 0.7 > 인것을 Filtering
###########################################################  
filter_dict_data = list(filter(lambda x:float(x['Flammability']) > 0.7,sort_dict_data))

print("="*100)
print("Dictionary 객체에서 인화성 지수가 0.7 > 인것을 Filtering")
print("="*100)

for row in filter_dict_data:
    print(row)


####################################################################
# List 형태를 CSV 파일로 저장
####################################################################

file_path = 'C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_danger.csv'
with open(file_path,'w',newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(filter_csv_data)


####################################################################
# Dictionary 형태를 CSV 파일로 저장
####################################################################
file_path = 'C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_danger_dict.csv'
with open(file_path,'w', newline='',encoding='utf-8') as file:
     fieldnames = ['Substance','Weight (g/cm³)','Specific Gravity','Strength','Flammability']
     writer = csv.DictWriter(file,fieldnames=fieldnames)
     writer.writeheader()
     writer.writerows(filter_dict_data)

####################################################################
# Bin 파일로 저장
####################################################################
import pickle

# 데이타를 이진 파일로 저장
def save_binary_pickle(data,filename):
    with open(filename,'wb') as file:
        pickle.dump(data,file)
    print(f"데이타가 {filename}에 저장되었습니다.")

# 이진파일 읽기
def load_binary_pickle(filename):
    with open(filename,'rb') as file:
        data = pickle.load(file)
        print(f"{filename}에서 데이타를 읽었습니다.")
    return data

#저장하기

file_path = 'C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_danger.bin'
save_binary_pickle(list(filter_csv_data),file_path)

#읽기
loaded_data = load_binary_pickle(file_path)
print("-" * 100)
print("Binary File 읽기")
print("-" * 100)
for row in loaded_data:
    print(row)