"""
📂 1단계: 데이터 수집 및 분석 (mas_map.py)
✔ 수행 내용
area_map.csv, area_struct.csv, area_category.csv 파일을 불러와 내용을 출력하고 분석합니다.
구조물 ID를 area_category.csv 기준으로 이름으로 변환합니다.
세 데이터를 하나의 DataFrame으로 병합하고, area 기준으로 정렬합니다.
확인된 데이터에는 여러 지역의 정보가 들어 있지만 반달곰 커피는 area 1에 집중되어 있는 것을 알게 되어 있습니다. 
따라서 전체 지역의 정보는 불필요하기 때문에 area 1에 대한 데이터만 필터링 해서 출력한다.
결과 코드는 mas_map.py로 저장합니다.
(보너스) 구조물 종류별 요약 통계를 리포트로 출력합니다.
"""
###################################################
# area_map.csv
###################################################
# x,y : 좌표
# ConstructionSite : 건설 현장 여부 (0: 없음, 1: 있음)
#-------------------------------------------------#
# 예시 데이터
#-------------------------------------------------#
# x,y,ConstructionSite
# 1,1,0
# 1,2,0
# 1,3,0
###################################################

###################################################
# area_struct.csv
###################################################
# x,y : 좌표
# category : 구조물 종류 (ID)
# area : 지역 (1, 2, 3 등)
#-------------------------------------------------#
# 예시 데이터
#-------------------------------------------------#
# x,y,category,area
# 1,1,0,0
# 1,2,0,0
###################################################

###################################################
# area_category.csv
###################################################
# x,y : 좌표
# category : 구조물 종류 (ID)
# area : 지역 (1, 2, 3 등)
#-------------------------------------------------#
# 예시 데이터
#-------------------------------------------------#
# category,struct
# 1,       Apartment
# 2,       Building
# 3,       MyHome
# 4,       BandalgomCoffee
###################################################

###################################################
# 처리 절차 
###################################################
# 1. area_struct + area_category 
# >> area_struct + area_struct 
# >> merged_data 
# >> merged_data 를 area 로 정렬
# >> area1_data : merged_data 에서 area = 1 인 값만 추출해서 저장
###################################################


import pandas as pd

def load_and_analyze_data():
    """데이터 파일들을 불러와서 분석하는 함수"""
    
    print("=" * 60)
    print("📂 1단계: 데이터 수집 및 분석")
    print("=" * 60)
    
    # 1. CSV 파일들 불러오기
    print("\n1️⃣ CSV 파일 불러오기...")
    try:
        area_map = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_map.csv')
        area_struct = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_struct.csv')
        area_category = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_category.csv')
        
        print("✅ 모든 CSV 파일을 성공적으로 불러왔습니다.")
    except FileNotFoundError as e:
        print(f"❌ 파일을 찾을 수 없습니다: {e}")
        return None
    
    # 2. 각 파일의 내용 출력 및 분석
    print("\n2️⃣ 각 파일 내용 분석...")
    
    print("\n📊 area_map.csv 분석:")
    print(f"   - 행 수: {len(area_map)}")
    print(f"   - 열 수: {len(area_map.columns)}")
    print(f"   - 열 이름: {list(area_map.columns)}")
    print("\n   처음 5행:")
    print(area_map.head())
    
    print("\n📊 area_struct.csv 분석:")
    print(f"   - 행 수: {len(area_struct)}")
    print(f"   - 열 수: {len(area_struct.columns)}")
    print(f"   - 열 이름: {list(area_struct.columns)}")
    print("\n   처음 5행:")
    print(area_struct.head())
    
    print("\n📊 area_category.csv 분석:")
    print(f"   - 행 수: {len(area_category)}")
    print(f"   - 열 수: {len(area_category.columns)}")
    print(f"   - 열 이름: {list(area_category.columns)}")
    print("\n   전체 내용:")
    print(area_category)
    
    # 3. 구조물 ID를 이름으로 변환
    print("\n3️⃣ 구조물 ID를 이름으로 변환...")
    
    # area_category를 딕셔너리로 변환하여 매핑
    # dict : dictionary 생성 (키: category, 값: struct)
    # zip(): 두 시퀀스를 쌍으로 묶어줌
    category_dict = dict(zip(area_category['category'], area_category['struct']))
    
    # area_struct에 구조물 이름 추가
    # map() : 각 category 값을 category_dict에서 대응되는 struct 이름으로 변환
    # area_struct['struct_name'] : 새로운 열을 추가하여 구조물 이름을 저장
    area_struct['struct_name'] = area_struct['category'].map(category_dict)
    
    print("✅ 구조물 ID를 이름으로 변환 완료")
    print("\n   변환된 area_struct (처음 5행):")
    print(area_struct.head())
    
    # 4. 세 데이터를 하나의 DataFrame으로 병합
    print("\n4️⃣ 데이터 병합...")
    
    # area_map과 area_struct를 x, y 좌표 기준으로 병합
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
    # area 기준으로 정렬
    merged_data = merged_data.sort_values('area')
    
    print("✅ 데이터 병합 및 정렬 완료")
    print(f"   - 병합된 데이터 행 수: {len(merged_data)}")
    print(f"   - 병합된 데이터 열 수: {len(merged_data.columns)}")
    print("\n   병합된 데이터 (처음 5행):")
    print(merged_data.head())
    
    # 5. area 1에 대한 데이터만 필터링
    print("\n5️⃣ area 1 데이터 필터링...")
    
    area1_data = merged_data[merged_data['area'] == 1]
    
    print(f"✅ area 1 데이터 필터링 완료")
    print(f"   - area 1 데이터 행 수: {len(area1_data)}")
    print("\n   area 1 데이터:")
    print(area1_data)
    
    # 6. 보너스: 구조물 종류별 요약 통계를 리포트로 출력
    print("\n6️⃣ 보너스: 구조물 종류별 요약 통계...")
    
    # 전체 데이터에서 구조물 종류별 통계
    print("\n📈 전체 지역 구조물 종류별 통계:")
    struct_summary = merged_data['struct_name'].value_counts()
    print(struct_summary)
    
    # area 1에서 구조물 종류별 통계
    print("\n📈 area 1 구조물 종류별 통계:")
    area1_struct_summary = area1_data['struct_name'].value_counts()
    print(area1_struct_summary)
    
    # 구조물별 상세 통계
    # merged_data.groupby('struct_name') : struct_name 별로 그룹화
    # agg() : 그룹화된 데이터에 대해 여러 함수를 적용
    # area : ['count', 'nunique'] : area 열에 대해 count와 nunique 함수 적용
    # x, y : ['mean', 'min', 'max'] : x, y 열에 대해 mean, min, max 함수 적용
    # round(2) : 소수점 2자리까지 표시
    # 'area' 열에 적용:
    # count: 각 구조물별 개수 (총 몇 개 있는지)
    # nunique: 각 구조물이 몇 개의 지역에 있는지 :  nunique = "number of unique"  # 고유한 값의 개수
    # 'x' 좌표에 적용:
    # mean: x 좌표의 평균값
    # min: x 좌표의 최솟값
    # max: x 좌표의 최댓값
    # 'y' 좌표에 적용:
    # mean: y 좌표의 평균값 (python 의 평균값 함수, median : 중앙값...)
    # min: y 좌표의 최솟값
    # max: y 좌표의 최댓값

    print("\n📊 구조물별 상세 통계:")
    struct_detailed = merged_data.groupby('struct_name').agg({
        'area': ['count', 'nunique'],
        'x': ['mean', 'min', 'max'],
        'y': ['mean', 'min', 'max']
    }).round(2)
    print(struct_detailed)
    
    return area1_data, merged_data

def main():
    """메인 함수"""
    print("☕ 반달곰 커피 데이터 분석 프로그램")
    print("=" * 60)
    
    # 데이터 분석 실행
    result = load_and_analyze_data()
    
    if result:
        area1_data, merged_data = result
        print("\n" + "=" * 60)
        print("✅ 1단계 데이터 수집 및 분석 완료!")
        print("=" * 60)
        print(f"📊 분석 결과:")
        print(f"   - 전체 데이터: {len(merged_data)}개 행")
        print(f"   - area 1 데이터: {len(area1_data)}개 행")
        print(f"   - 구조물 종류: {merged_data['struct_name'].nunique()}개")
    else:
        print("\n❌ 데이터 분석 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main() 