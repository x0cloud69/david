"""
📂 1단계: 데이터 수집 및 분석
반달곰 커피 데이터 분석 프로그램
area_map 구조
    x: x 좌표
    y: y 좌표
    ConstructionSite: 건설 현장 여부 (0 또는 1) 0 = 건설 중이 아님(아파트,빌딩,), 1= 건설 중(회색) 
                      건설중인 종류 : 1. Apartment,  2, Building, 3, MyHome  4, BandalgomCoffee
area_struct 구조
    x: x 좌표
    y: y 좌표       
    category: 구조물 종류
    area: 구조물 면적 (????)
area_category 구조
    category: 구조물 종류
    struct: 구조물 이름

        
"""

import pandas as pd
import numpy as np

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
       
       # 1단계: 원본 데이터 저장
       print("💾 1단계: 원본 CSV 파일들 저장...")
       area_map.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/step1_area_map.csv', index=False, encoding='utf-8-sig')
       area_struct.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/step1_area_struct.csv', index=False, encoding='utf-8-sig')
       area_category.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/step1_area_category.csv', index=False, encoding='utf-8-sig')
       print("✅ 1단계: 원본 데이터 저장 완료!")
       
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
    category_dict = dict(zip(area_category['category'], area_category['struct']))
    print("\n Category_dict: ", category_dict) # 딕셔너리 확인
    
    # area_struct에 구조물 이름 추가 (area_struct에 필드값이 있으면 덥어쓰기 없으면 추가가)
    area_struct['struct_name'] = area_struct['category'].map(category_dict)
    print("\n Area_struct: ", area_struct) # 데이터프레임 확인
    
    print("✅ 구조물 ID를 이름으로 변환 완료")
    print("\n   변환된 area_struct (처음 5행):")
    print(area_struct.head())
    
    # 3단계: 변환된 데이터 저장
    print("💾 3단계: 구조물 이름 변환된 데이터 저장...")
    area_struct.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/step3_area_struct_with_names.csv', index=False, encoding='utf-8-sig')
    print("✅ 3단계: 변환된 데이터 저장 완료!")
    
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
    
    # 4단계: 병합된 데이터 저장
    print("💾 4단계: 병합된 데이터 저장...")
    merged_data.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/step4_merged_data.csv', index=False, encoding='utf-8-sig')
    print("✅ 4단계: 병합된 데이터 저장 완료!")
    
    # 5. area별 데이터 분석
    print("\n5️⃣ area별 데이터 분석...")
    
    # area별 개수 확인
    print("\n📊 area별 데이터 개수:")
    area_counts = merged_data['area'].value_counts().sort_index()
    for area, count in area_counts.items():
        print(f"   - area {area}: {count}개")
    
    # 각 area별 데이터 필터링 및 저장
    area_data_dict = {}
    for area in sorted(merged_data['area'].unique()):
        area_data = merged_data[merged_data['area'] == area]
        area_data_dict[area] = area_data
        
        print(f"\n📊 area {area} 데이터:")
        print(f"   - 행 수: {len(area_data)}")
        print(f"   - 구조물 분포:")
        struct_counts = area_data['struct_name'].value_counts()
        for struct, count in struct_counts.items():
            if pd.notna(struct):
                print(f"     * {struct}: {count}개")
        
        # 건설 현장 개수
        construction_count = (area_data['ConstructionSite'] == 1).sum()
        print(f"   - 건설 현장: {construction_count}개")
        
        # 각 area별 데이터 저장
        filename = f'C:/codyssey/ky-codyssey-main/Codyseey/step5_area{area}_data.csv'
        area_data.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"   💾 area {area} 데이터 저장: {filename}")
    
    # area 1 데이터 (기존 코드와 호환)
    area1_data = area_data_dict[1]
    
    print(f"\n✅ area별 데이터 분석 완료")
    print(f"   - 총 {len(area_data_dict)}개 area 분석")
    print(f"   - 각 area별 데이터 파일 저장 완료")
    
    # 6. 보너스: 구조물 종류별 요약 통계
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
    print("\n📊 구조물별 상세 통계:")
    struct_detailed = merged_data.groupby('struct_name').agg({
        'area': ['count', 'nunique'],
        'x': ['mean', 'min', 'max'],
        'y': ['mean', 'min', 'max']
    }).round(2)
    print(struct_detailed)
    
    # 데이터를 파일로 저장해서 확인
    print("\n💾 데이터를 파일로 저장 중...")
    try:
        merged_data.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/merged_data.csv', index=False, encoding='utf-8-sig')
        area1_data.to_csv('C:/codyssey/ky-codyssey-main/Codyseey/area1_data.csv', index=False, encoding='utf-8-sig')
        print("✅ 데이터가 CSV 파일로 저장되었습니다!")
        print("   - merged_data.csv: 전체 병합 데이터")
        print("   - area1_data.csv: area 1 필터링 데이터")
        
        # Excel 파일 저장 시도 (openpyxl 모듈이 있는 경우에만)
        try:
            merged_data.to_excel('C:/codyssey/ky-codyssey-main/Codyseey/merged_data.xlsx', index=False)
            print("   - merged_data.xlsx: 엑셀 형식 데이터")
        except ImportError:
            print("   ⚠️ Excel 파일 저장을 위해 'pip install openpyxl' 명령어를 실행하세요")
        except Exception as e:
            print(f"   ⚠️ Excel 파일 저장 실패: {e}")
            
    except Exception as e:
        print(f"❌ 파일 저장 중 오류: {e}")
    
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