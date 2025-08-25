import csv
import sys

with open('C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = list(reader)
    for row in data:
        row['Flammability'] = float(row['Flammability'])

print("Data Load: ", data)
data_sort = sorted(data, key=lambda x:x['Flammability'], reverse=True)
print("="*100)
print("Data Sort: ", data_sort)

data_filter = list(filter(lambda x:x['Flammability'] > 0.7,data))

print("="*100)
print("Flammability 0.7 Over Data : \n")
print("="*100)

print(data_filter)

####################################################################
# CSV 파일로 저장
####################################################################
with open('C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_danger.csv','w', newline='',encoding='utf-8') as file:
     fieldnames = ['Substance','Weight (g/cm³)','Specific Gravity','Strength','Flammability']
     writer = csv.DictWriter(file,fieldnames=fieldnames)
     writer.writeheader()
     writer.writerows(data_filter)

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

file_name = 'C:\codyssey\david\ky-codyssey-main\Codyseey\JPT4-2\mars_base\Mars_Base_Inventory_danger1.pkl'
save_binary_pickle(data_filter,file_name)

#읽기
loaded_data = load_binary_pickle(file_name)
print("불러온 데이타 : \n",loaded_data)
      