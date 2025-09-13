import numpy as np
import os
import csv


arr1 = []
arr2 = []
arr3 = []

# 현재 스크립트 파일의 디렉토리를 기준으로 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
mars_base_dir = os.path.join(script_dir, 'mars_base')

file_path_1 = os.path.join(mars_base_dir, 'mars_base_main_parts-001.csv')
file_path_2 = os.path.join(mars_base_dir, 'mars_base_main_parts-002.csv')
file_path_3 = os.path.join(mars_base_dir, 'mars_base_main_parts-003.csv')

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

    # 현재 스크립트 위치 기준으로 출력 파일 경로 설정
    output_file = os.path.join(mars_base_dir, 'parts_to_work_on.csv')
    
    # 디렉토리 존재 확인 및 생성
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"디렉토리가 생성되었습니다: {output_dir}")
    
    # 디렉토리 쓰기 권한 확인
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"디렉토리에 쓰기 권한이 없습니다: {output_dir}")
    
    # csv 모듈을 사용하여 빈 줄 없이 저장
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 헤더 작성
        writer.writerow(['part', 'average_strength'])
        # 데이터 작성
        for part, strength in output_data:
            writer.writerow([part, f"{strength:.2f}"])
    
    print(f"파일이 성공적으로 저장되었습니다: {output_file}")
    print(f"필터링된 항목 수: {len(filtered_parts)}")

    # 저장된 데이터 확인 및 출력
    print("\n저장된 데이터:")
    for part, strength in output_data:
        print(f"{part}: {strength:.2f}")

except FileNotFoundError as e:
    print(f"파일경로 오류: {e}")
except PermissionError as e:
    print(f"권한오류: {e}")
except ValueError as e:
    print(f"데이터 처리중 오류 발생: {e}")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")
finally:
    print("\n작업이 완료되었습니다.")



                                   
                                   