"""
🗺 2단계: 지도 시각화 (map_draw.py, map.png)
✔ 수행 내용
분석된 데이터를 기반으로 지역 지도를 시각화합니다.
지도는 좌측 상단이 (1, 1), 우측 하단이 가장 큰 좌표가 되도록 시각화해야 합니다.
가로/세로 방향의 그리드 라인을 그리고,
아파트와 빌딩은 갈색 원형,
반달곰 커피점 위치는 녹색 사각형,
내 집의 위치는 녹색 삼각형,
건설 현장은 회색 사각형으로 표현합니다.
건설 현장을 나타내는 회색 사각형은 바로 옆 좌표와 살짝 겹쳐도 됩니다.
건설 현장과 기타 구조물(아파트, 빌딩)과 겹치면 건설 현장으로 판단한다.
이미지로 map.png 파일로 저장합니다.
시각화 코드는 map_draw.py로 저장합니다.
(보너스) 아파트, 빌딩, 반달곰 커피 등의 범례를 지도에 함께 표현한다.
"""

import pandas as pd

import matplotlib.pyplot as plt
########################################################################################
#matplotlib.pyplot : 그래프를 그리는 모듈
#plt.subplots : 그래프를 그리는 함수
#figsize : 그래프의 크기를 지정하는 튜플 (가로, 세로)
#figsize=(8, 8) : 그래프의 크기를 8x8로 설정 (단위 : 인치)
#ax : 그래프 영역을 나타내는 Axes 객체
#fig: Figure 객체(전체 캔버스  )
#fig, ax = plt.subplots(figsize=(8, 8)) : 그래프 캔버스와 영역을 생성
########################################################################################

import matplotlib.patches as patches
########################################################################################
#matplotlib.patches : 그래프에 도형을 그리는 모듈
#patches.Rectangle : 사각형 도형을 그리는 클래스
#patches.Circle : 원형 도형을 그리는 클래스
#patches.Polygon : 다각형 도형을 그리는 클래스
########################################################################################


from mas_map import load_and_analyze_data

# 한글 깨지는 문제 및 음수 표현 해결
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """mas_map.py에서 분석된 데이터를 불러오는 함수"""
    try:
       
        
        # DataFrame 가져오기
        area1_data, merged_data = load_and_analyze_data()
        
        print("✅ mas_map.py에서 DataFrame을 성공적으로 가져왔습니다.")
        print(f"   - merged_data: {len(merged_data)}개 행")
        print(f"   - area1_data: {len(area1_data)}개 행")
        
        return merged_data, area1_data
        
    except Exception as e:
        print(f"❌ DataFrame을 가져오는 중 오류가 발생했습니다: {e}")
        return None, None

def process_data(merged_data):
    """이미 처리된 데이터를 사용하는 함수"""
    if merged_data is None or area1_data is None:
        return None
    
    print("✅ 이미 분석된 데이터를 사용합니다.")
    return merged_data

def create_map_visualization(data):
    """지도 시각화를 생성하는 함수"""
    #ply.sublots() : matplotlib에서 그래프를 그릴 수 있는 Figure(캔버스)와 Axes(그래프 영역)를 생성하는 함수
    #figsize : 그래프의 크기를 지정하는 튜플 (가로, 세로)
    #figsize=(8, 8) : 그래프의 크기를 8x8로 설정 (단위 : 인치)
    #ax : 그래프 영역을 나타내는 Axes 객체
    #fig: Figure 객체(전체 캔버스  )
    #fig, ax = plt.subplots(figsize=(8, 8)) : 그래프 캔버스와 영역을 생성
    fig, ax = plt.subplots(figsize=(8, 8))
    
    
    # 좌표 범위 설정
    #DataFrame의 x,y 좌표의 최소/최대값을 가져옴 (여기서 DataFrame은 merged_data)
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()
    
    
    # 좌표범위 설정 하는것 (좌표범위 설정 하는것은 그래프 그릴때 중요)
    # 시작점은 좌표의 최소값에서 1을 빼고 끝점은 좌표의 최대값에서 1을 더한다.
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    ax.invert_yaxis()  # 좌측 상단이 (1,1) 되도록

    # 그리드 라인
    # axvline : x축 선 그리기
    # axhline : y축 선 그리기
    # color : 선의 색상
    # linestyle : 선의 스타일
    # linewidth : 선의 두께
    for x in range(int(min_x), int(max_x) + 2):
        ax.axvline(x, color='lightgray', linestyle='--', linewidth=0.5)
    for y in range(int(min_y), int(max_y) + 2):
        ax.axhline(y, color='lightgray', linestyle='--', linewidth=0.5)

    # 구조물 시각화
    # iterrows() : DataFrame의 각 행을 순회하는 이터레이터 반환
    # _ : 인덱스 번호
    # row : 현재 행의 데이터 (pd.Series 타입)
    # for _, row in ...: 인덱스는 무시하고, 각 행(row)만 사용
    #        row: 한 행의 데이터(Series), 컬럼명으로 값 접근 가능
    for _, row in data.iterrows():
        x, y = row['x'], row['y']
        struct_name = str(row.get('struct_name', '')).strip()
        construction_site = row.get('ConstructionSite', 0)

        # 건설 현장 우선 표시
        if construction_site == 1:
            rect = patches.Rectangle((x-0.6, y-0.6), 1.2, 1.2, facecolor='#666666', alpha=0.9, edgecolor='#333333', linewidth=2)
            ax.add_patch(rect)
        elif struct_name.lower() == 'apartment':
            circle = patches.Circle((x, y), 0.4, facecolor='#8B4513', alpha=1.0, edgecolor='#654321', linewidth=2)
            ax.add_patch(circle)
        elif struct_name.lower() == 'building':
            circle = patches.Circle((x, y), 0.4, facecolor='#A0522D', alpha=1.0, edgecolor='#654321', linewidth=2)
            ax.add_patch(circle)
        elif struct_name.lower() == 'bandalgomcoffee':
            rect = patches.Rectangle((x-0.4, y-0.4), 0.8, 0.8, facecolor='#228B22', alpha=1.0, edgecolor='#006400', linewidth=2)
            ax.add_patch(rect)
        elif struct_name.lower() == 'myhome':
            triangle = patches.Polygon([[x, y+0.4], [x-0.4, y-0.4], [x+0.4, y-0.4]], facecolor='#32CD32', alpha=1.0, edgecolor='#228B22', linewidth=2)
            ax.add_patch(triangle)

    # 범례 추가 (보너스)
    legend_elements = [
        patches.Circle((0, 0), 0.4, facecolor='#8B4513', edgecolor='#654321', label='아파트'),
        patches.Circle((0, 0), 0.4, facecolor='#A0522D', edgecolor='#654321', label='빌딩'),
        patches.Rectangle((0, 0), 0.8, 0.8, facecolor='#228B22', edgecolor='#006400', label='반달곰 커피'),
        patches.Polygon([[0, 0.4], [-0.4, -0.4], [0.4, -0.4]], facecolor='#32CD32', edgecolor='#228B22', label='내 집'),
        patches.Rectangle((0, 0), 1.2, 1.2, facecolor='#666666', edgecolor='#333333', label='건설 현장')
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    ax.set_title('반달곰 커피 지도')
    plt.savefig('map.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print("반달곰 커피 지도 시각화 프로그램")
    
    merged_data, area1_data = load_data()
    if merged_data is not None:
        data = process_data(merged_data)
        if data is not None:
            create_map_visualization(data)
        else:
            print("❌ 데이터 처리 중 오류가 발생했습니다.")
    else:
        print("❌ 데이터를 불러올 수 없습니다.")