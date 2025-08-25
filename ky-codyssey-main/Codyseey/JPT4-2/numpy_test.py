import numpy as np
import os


arr1 = []
arr2 = []
arr3 = []

file_path_1 = 'C:/codyssey/david/ky-codyssey-main/Codyseey/JPT4-2/mars_base/mars_base_main_parts-001.csv'
file_path_2 = 'C:/codyssey/david/ky-codyssey-main/Codyseey/JPT4-2/mars_base/mars_base_main_parts-002.csv'
file_path_3 = 'C:/codyssey/david/ky-codyssey-main/Codyseey/JPT4-2/mars_base/mars_base_main_parts-003.csv'

arr1 = np.loadtxt(file_path_1, delimiter=',', skiprows =1, dtype=[('parts', 'U20'), ('strength', 'f8')])
arr2 = np.loadtxt(file_path_2, delimiter=',', skiprows = 1, dtype = [('parts','U20'), ('strength','f8')])
arr3 = np.loadtxt(file_path_3, delimiter=',', skiprows = 1, dtype = [('parts','U20'), ('strength','f8')])

print("Numpy Arr1")
print("-" * 100)
print(arr1)
print("-" * 100)

print("Numpy Arr2")
print("-" * 100)
print(arr2)
print("-" * 100)

print("Numpy Arr3")
print("-" * 100)
print(arr3)
print("-" * 100)

##################################################################################
# parts 필드만 합쳐서 새로운 배열 생성
##################################################################################

parts = np.concatenate((arr1,arr2,arr3))

print("병합된 parts 배열 : ")
print("-" * 100)
print(parts)
print("-" * 100)
                       
##################################################################################
# 각 parts  별 strength 의 평균값 계산
##################################################################################

unique_parts = np.unique(parts['parts'])

print("각 parts  별 strength 의 평균값 계산 : ")
print("-" * 100)
for part in unique_parts:
    part_data = parts[parts['parts']==part]
    average_strength = np.mean(part_data['strength'])
    print(f"{part} : {average_strength:.2f}")
print("-" * 100)


##################################################################################
# 평균값이 50보다 작은 항목만 필터링하여 parts_to_work_on.csv로 저장
##################################################################################
print("평균값이 50보다 작은 항목만 필터링하여 parts_to_work_on.csv로 저장")
print("-" * 100)

try:
    merged_array = np.concatenate((arr1,arr2,arr3))

    unique_parts = np.unique(merged_array['parts'])

    filtered_parts = []
    filtered_strength = []

    for part in unique_parts:
        # 해당 부품의 모든 데이터 찾기
        part_data = merged_array[merged_array['parts']==part]
        #평균 강도 계산
        average_strength = np.mean(part_data['strength'])

        #평균이 50보다 작은 경우만 저장
        if average_strength < 50:
            filtered_parts.append(part)
            filtered_strength.append(average_strength)
    
    if not filtered_parts:
        raise ValueError('50보다 작은 평균값을 가진 부품이 없습니다.')
    
    # 결과를 구조화된 배열로 변환
    output_data = np.array(list(zip(filtered_parts,filtered_strength)),dtype=[('parts','U20'),('average_strength','f8')])

    # 파일 저장 전 디렉토리 접근 권한 확인

    file_path = os.path.join('C:', 'codyssey', 'david', 'ky-codyssey-main','Codyseey', 'JPT4-2', 'mars_base', 'parts_to_work_on.csv')
   # output_dir = os.path.dirname(file_path) or '.'

   # if not os.path.exists(output_dir):
   #     raise FileNotFoundError(f"디렉토리가 존재하지 않습니다 : {output_dir}")
    
    if not os.path.exists(file_path):
        if not os.access(file_path,os.W_OK):
            raise PermissionError(f"파일에 쓰기 권한이 없습니다 : {file_path}")
    
    # csv 파일로 저장
    np.savetxt(file_path,output_data,delimiter=',',
               fmt=['%s','%.2f'],
               header='part,average_strength',
               comments='')
    
    print(f"파일이 성공적으로 저장되었습니다 : {file_path}")
    print(f"필더링된 항목 수 : {len(filtered_parts)}")

    # 저장된 데이터 확인 및 출력
    print("\n 저장된 데이터 :")
    for part,strength in output_data:
        print(f"{part}: {strength: .2f}")

except FileNotFoundError as e:
    print(f"파일경로 오류 : {e}")
except PermissionError as e:
    print(f"권한오류 : {e}")
except ValueError as e:
    print(f"데이타 처리중 오류 발생 : {e}")
except Exception as e:
    print(f"예상치 못한 오류가 발생 했습니다 : {e}")
finally:
    print("\n 작업이 완료되었습니다.")



                                   
                                   