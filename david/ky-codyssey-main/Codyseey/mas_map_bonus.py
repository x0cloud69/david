"""
(보너스) 구조물 종류별 요약 통계를 리포트로 출력합니다.

이 파일은 반달곰 커피 데이터 분석의 보너스 기능으로,
구조물 종류별 상세한 통계 분석과 리포트를 생성합니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data():
    """데이터 파일들을 불러오는 함수"""
    try:
        area_map = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_map.csv')
        area_struct = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_struct.csv')
        area_category = pd.read_csv('C:/codyssey/ky-codyssey-main/Codyseey/area_category.csv')
        
        print("✅ 데이터 파일들을 성공적으로 불러왔습니다.")
        return area_map, area_struct, area_category
    except FileNotFoundError as e:
        print(f"❌ 파일을 찾을 수 없습니다: {e}")
        return None, None, None

def process_data(area_map, area_struct, area_category):
    """데이터를 처리하는 함수"""
    # 구조물 ID를 이름으로 변환
    category_dict = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_dict)
    
    # 데이터 병합
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
    return merged_data

def generate_structure_statistics_report(data):
    """구조물 종류별 요약 통계 리포트를 생성하는 함수"""
    
    print("=" * 80)
    print("📊 구조물 종류별 요약 통계 리포트")
    print("=" * 80)
    print(f"📅 생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 1. 전체 데이터 개요
    print("\n1️⃣ 전체 데이터 개요")
    print("-" * 40)
    print(f"   📍 총 좌표 수: {len(data):,}개")
    print(f"   🏗️  건설 현장 수: {(data['ConstructionSite'] == 1).sum():,}개")
    print(f"   🏠 구조물이 있는 좌표: {data['struct_name'].notna().sum():,}개")
    print(f"   🗺️  지역 수: {data['area'].nunique()}개")
    
    # 2. 지역별 분석
    print("\n2️⃣ 지역별 분석")
    print("-" * 40)
    area_analysis = data.groupby('area').agg({
        'x': 'count',
        'ConstructionSite': lambda x: (x == 1).sum(),
        'struct_name': lambda x: x.notna().sum()
    }).rename(columns={
        'x': '총 좌표 수',
        'ConstructionSite': '건설 현장 수',
        'struct_name': '구조물 수'
    })
    
    for area, row in area_analysis.iterrows():
        print(f"   🏘️  Area {area}:")
        print(f"      - 총 좌표: {row['총 좌표 수']}개")
        print(f"      - 건설 현장: {row['건설 현장 수']}개")
        print(f"      - 구조물: {row['구조물 수']}개")
        print(f"      - 구조물 비율: {row['구조물 수']/row['총 좌표 수']*100:.1f}%")
    
    # 3. 구조물 종류별 상세 통계
    print("\n3️⃣ 구조물 종류별 상세 통계")
    print("-" * 40)
    
    # 구조물이 있는 데이터만 필터링
    struct_data = data[data['struct_name'].notna()]
    
    if len(struct_data) > 0:
        struct_stats = struct_data.groupby('struct_name').agg({
            'area': ['count', 'nunique'],
            'x': ['mean', 'min', 'max', 'std'],
            'y': ['mean', 'min', 'max', 'std'],
            'ConstructionSite': lambda x: (x == 1).sum()
        }).round(2)
        
        # 컬럼명 정리
        struct_stats.columns = ['총 개수', '분포 지역 수', 'X평균', 'X최소', 'X최대', 'X표준편차', 
                               'Y평균', 'Y최소', 'Y최대', 'Y표준편차', '건설현장 겹침 수']
        
        for struct_name, row in struct_stats.iterrows():
            print(f"   🏢 {struct_name}:")
            print(f"      - 총 개수: {row['총 개수']}개")
            print(f"      - 분포 지역: {row['분포 지역 수']}개")
            print(f"      - X좌표: {row['X평균']:.1f} (범위: {row['X최소']}-{row['X최대']})")
            print(f"      - Y좌표: {row['Y평균']:.1f} (범위: {row['Y최소']}-{row['Y최대']})")
            print(f"      - 건설현장 겹침: {row['건설현장 겹침 수']}개")
            print()
    else:
        print("   ⚠️ 구조물이 있는 데이터가 없습니다.")
    
    # 4. 반달곰 커피 특별 분석
    print("\n4️⃣ 반달곰 커피 특별 분석")
    print("-" * 40)
    
    coffee_data = data[data['struct_name'] == ' BandalgomCoffee']
    if len(coffee_data) > 0:
        print(f"   ☕ 반달곰 커피점 수: {len(coffee_data)}개")
        print(f"   📍 위치:")
        for _, row in coffee_data.iterrows():
            print(f"      - ({row['x']}, {row['y']}) - Area {row['area']}")
        
        # 반달곰 커피 주변 분석
        print(f"\n   🔍 반달곰 커피 주변 분석:")
        coffee_areas = coffee_data['area'].unique()
        for area in coffee_areas:
            area_data = data[data['area'] == area]
            coffee_in_area = area_data[area_data['struct_name'] == ' BandalgomCoffee']
            other_structs = area_data[area_data['struct_name'].notna() & 
                                    (area_data['struct_name'] != ' BandalgomCoffee')]
            
            print(f"      Area {area}:")
            print(f"        - 반달곰 커피: {len(coffee_in_area)}개")
            print(f"        - 다른 구조물: {len(other_structs)}개")
            print(f"        - 건설 현장: {(area_data['ConstructionSite'] == 1).sum()}개")
    else:
        print("   ⚠️ 반달곰 커피점이 없습니다.")
    
    # 5. 건설 현장과 구조물 관계 분석
    print("\n5️⃣ 건설 현장과 구조물 관계 분석")
    print("-" * 40)
    
    construction_sites = data[data['ConstructionSite'] == 1]
    construction_with_struct = construction_sites[construction_sites['struct_name'].notna()]
    
    print(f"   🏗️  총 건설 현장: {len(construction_sites)}개")
    print(f"   🏢 구조물과 겹치는 건설 현장: {len(construction_with_struct)}개")
    print(f"   📊 겹침 비율: {len(construction_with_struct)/len(construction_sites)*100:.1f}%")
    
    if len(construction_with_struct) > 0:
        print(f"   📋 겹치는 구조물 종류:")
        overlap_stats = construction_with_struct['struct_name'].value_counts()
        for struct, count in overlap_stats.items():
            print(f"      - {struct}: {count}개")
    
    # 6. 지역별 구조물 밀도 분석
    print("\n6️⃣ 지역별 구조물 밀도 분석")
    print("-" * 40)
    
    density_analysis = data.groupby('area').agg({
        'x': 'count',
        'struct_name': lambda x: x.notna().sum(),
        'ConstructionSite': lambda x: (x == 1).sum()
    }).rename(columns={
        'x': '총 좌표',
        'struct_name': '구조물 수',
        'ConstructionSite': '건설 현장 수'
    })
    
    density_analysis['구조물 밀도(%)'] = (density_analysis['구조물 수'] / density_analysis['총 좌표'] * 100).round(1)
    density_analysis['건설 현장 밀도(%)'] = (density_analysis['건설 현장 수'] / density_analysis['총 좌표'] * 100).round(1)
    
    for area, row in density_analysis.iterrows():
        print(f"   🏘️  Area {area}:")
        print(f"      - 구조물 밀도: {row['구조물 밀도(%)']}%")
        print(f"      - 건설 현장 밀도: {row['건설 현장 밀도(%)']}%")
        print(f"      - 개발 활성도: {row['구조물 밀도(%)'] + row['건설 현장 밀도(%)']:.1f}%")
    
    # 7. 요약 및 결론
    print("\n7️⃣ 요약 및 결론")
    print("-" * 40)
    
    total_structs = data['struct_name'].notna().sum()
    total_construction = (data['ConstructionSite'] == 1).sum()
    
    print(f"   📈 전체 개발 현황:")
    print(f"      - 구조물 점유율: {total_structs/len(data)*100:.1f}%")
    print(f"      - 건설 현장 점유율: {total_construction/len(data)*100:.1f}%")
    print(f"      - 빈 공간 비율: {(len(data) - total_structs - total_construction)/len(data)*100:.1f}%")
    
    # 가장 활발한 지역
    most_active_area = density_analysis['구조물 밀도(%)'].idxmax()
    print(f"\n   🏆 가장 활발한 지역: Area {most_active_area}")
    print(f"      - 구조물 밀도: {density_analysis.loc[most_active_area, '구조물 밀도(%)']}%")
    
    # 반달곰 커피 집중 지역
    if len(coffee_data) > 0:
        coffee_center_area = coffee_data['area'].mode().iloc[0]
        print(f"\n   ☕ 반달곰 커피 집중 지역: Area {coffee_center_area}")
        print(f"      - 커피점 수: {len(coffee_data[coffee_data['area'] == coffee_center_area])}개")
    
    print("\n" + "=" * 80)
    print("✅ 구조물 종류별 요약 통계 리포트 완료!")
    print("=" * 80)

def save_report_to_file(data):
    """통계 리포트를 파일로 저장하는 함수"""
    try:
        # 구조물 통계를 CSV로 저장
        struct_data = data[data['struct_name'].notna()]
        if len(struct_data) > 0:
            struct_stats = struct_data.groupby('struct_name').agg({
                'area': ['count', 'nunique'],
                'x': ['mean', 'min', 'max'],
                'y': ['mean', 'min', 'max'],
                'ConstructionSite': lambda x: (x == 1).sum()
            }).round(2)
            
            filename = f'C:/codyssey/ky-codyssey-main/Codyseey/structure_statistics_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            struct_stats.to_csv(filename, encoding='utf-8-sig')
            print(f"\n💾 통계 리포트가 저장되었습니다: {filename}")
        
        # 지역별 분석을 CSV로 저장
        area_analysis = data.groupby('area').agg({
            'x': 'count',
            'ConstructionSite': lambda x: (x == 1).sum(),
            'struct_name': lambda x: x.notna().sum()
        }).rename(columns={
            'x': '총 좌표 수',
            'ConstructionSite': '건설 현장 수',
            'struct_name': '구조물 수'
        })
        
        area_filename = f'C:/codyssey/ky-codyssey-main/Codyseey/area_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        area_analysis.to_csv(area_filename, encoding='utf-8-sig')
        print(f"💾 지역별 분석이 저장되었습니다: {area_filename}")
        
    except Exception as e:
        print(f"❌ 파일 저장 중 오류: {e}")

def main():
    """메인 함수"""
    print("📊 구조물 종류별 요약 통계 리포트 생성기")
    print("=" * 60)
    
    # 1. 데이터 불러오기
    area_map, area_struct, area_category = load_data()
    if area_map is None:
        return
    
    # 2. 데이터 처리
    print("\n2️⃣ 데이터 처리 중...")
    merged_data = process_data(area_map, area_struct, area_category)
    
    # 3. 통계 리포트 생성
    print("\n3️⃣ 통계 리포트 생성 중...")
    generate_structure_statistics_report(merged_data)
    
    # 4. 리포트 파일 저장
    print("\n4️⃣ 리포트 파일 저장 중...")
    save_report_to_file(merged_data)
    
    print("\n🎉 보너스 통계 분석이 완료되었습니다!")

if __name__ == "__main__":
    main() 