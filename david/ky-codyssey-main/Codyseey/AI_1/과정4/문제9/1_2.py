import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 개선
def setup_korean_font():
    """한글 폰트 설정"""
    try:
        # Windows의 경우
        font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕
        font_prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
    except:
        try:
            # 다른 한글 폰트 시도
            plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'Noto Sans CJK KR', 'DejaVu Sans']
        except:
            print("⚠️ 한글 폰트 설정에 실패했습니다. 영어로 표시됩니다.")
            plt.rcParams['font.family'] = ['DejaVu Sans']
    
    plt.rcParams['axes.unicode_minus'] = False
    print("✅ 폰트 설정 완료!")

# 폰트 설정 실행
setup_korean_font()

def create_dataframe():
    with open(r'C:\codyssey\david\ky-codyssey-main\Codyseey\AI_1\과정4\문제9\abalone_attributes.txt',encoding='utf-8') as f:
        attribute = f.read().strip().split('\n')
        
    column_names = [attr.strip() for attr in attribute]
    
    df = pd.read_csv(r'C:\codyssey\david\ky-codyssey-main\Codyseey\AI_1\과정4\문제9\abalone.txt',header=None,names=column_names)    
    
    df_label = df.copy()
    df_label['label'] = df_label['Sex']
    df_label['Sex'] = ''
    
    numeric_data = df_label.select_dtypes(include=['float64','int64']).columns
    
    # 기존 코드
    _min_max_ = pd.DataFrame(
        {
            'Min' : df[numeric_data].min(),
            'Max' : df[numeric_data].max(),
            'Range'   : df[numeric_data].max() - df[numeric_data].min()
        }
    )
    
    print("📊 Basic Statistics")
    print("=" * 50)
    print(_min_max_)
    
    # 새로 추가된 편차 분석 함수들
    variance_analysis = calculate_variance_metrics(df, numeric_data)
    
    return df, numeric_data, _min_max_, variance_analysis

def calculate_variance_metrics(df, numeric_columns):
    """변동계수, 범위대비 평균 비율, 사분위수 범위 계수 계산"""
    
    variance_metrics = pd.DataFrame()
    
    for col in numeric_columns:
        # 기본 통계값들
        mean_val = df[col].mean()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        median_val = df[col].median()
        
        # 1. 변동계수 (CV) = (표준편차 / 평균) × 100
        cv = calculate_cv(std_val, mean_val)
        
        # 2. 범위대비 평균 비율 = (최댓값 - 최솟값) / 평균
        range_ratio = calculate_range_ratio(min_val, max_val, mean_val)
        
        # 3. 사분위수 범위 계수 = IQR / 중위수
        iqr_coefficient = calculate_iqr_coefficient(q1, q3, median_val)
        
        # 무한대값 처리
        cv = handle_infinite_values(cv)
        range_ratio = handle_infinite_values(range_ratio)
        iqr_coefficient = handle_infinite_values(iqr_coefficient)
        
        # 결과 저장
        variance_metrics[col] = {
            'Mean': mean_val,
            'Std': std_val,
            'CV(%)': cv,
            'Range_Ratio': range_ratio,
            'IQR_Coeff': iqr_coefficient,
            'CV_Grade': classify_cv(cv),
            'Range_Grade': classify_range_ratio(range_ratio),
            'IQR_Grade': classify_iqr_coefficient(iqr_coefficient)
        }
    
    variance_df = pd.DataFrame(variance_metrics).T
    
    print("\n🔍 Variance Analysis Results")
    print("=" * 80)
    print(variance_df.round(3))
    
    # 편차 순위 출력
    print_variance_ranking(variance_df)
    
    return variance_df

def handle_infinite_values(value):
    """무한대값과 NaN 처리"""
    if np.isinf(value) or np.isnan(value):
        return 0.0
    return float(value)

def calculate_cv(std_val, mean_val):
    """변동계수 계산: CV = (표준편차 / 평균) × 100"""
    if mean_val == 0 or np.isclose(mean_val, 0):
        return 0.0
    return (std_val / mean_val) * 100

def calculate_range_ratio(min_val, max_val, mean_val):
    """범위대비 평균 비율 계산: (최댓값 - 최솟값) / 평균"""
    if mean_val == 0 or np.isclose(mean_val, 0):
        return 0.0
    return (max_val - min_val) / mean_val

def calculate_iqr_coefficient(q1, q3, median_val):
    """사분위수 범위 계수 계산: IQR / 중위수"""
    if median_val == 0 or np.isclose(median_val, 0):
        return 0.0
    iqr = q3 - q1
    return iqr / median_val

def classify_cv(cv):
    """변동계수 기준 분류"""
    if cv < 15: return "Very Low"
    elif cv < 25: return "Low"
    elif cv < 35: return "Medium"
    elif cv < 50: return "High"
    else: return "Very High"

def classify_range_ratio(range_ratio):
    """범위비율 기준 분류"""
    if range_ratio < 1.0: return "Very Low"
    elif range_ratio < 2.0: return "Low"
    elif range_ratio < 3.0: return "Medium"
    elif range_ratio < 5.0: return "High"
    else: return "Very High"

def classify_iqr_coefficient(iqr_coeff):
    """IQR계수 기준 분류"""
    if iqr_coeff < 0.2: return "Very Low"
    elif iqr_coeff < 0.4: return "Low"
    elif iqr_coeff < 0.6: return "Medium"
    elif iqr_coeff < 1.0: return "High"
    else: return "Very High"

def print_variance_ranking(variance_df):
    """편차 순위 출력"""
    print("\n📈 Variance Rankings")
    print("=" * 50)
    
    # 1. CV 기준 순위
    print("🔥 Coefficient of Variation (CV) Ranking:")
    cv_ranking = variance_df.sort_values('CV(%)', ascending=False)
    for i, (idx, row) in enumerate(cv_ranking.iterrows(), 1):
        print(f"  {i}. {idx:15s}: {row['CV(%)']:6.1f}% ({row['CV_Grade']})")
    
    # 2. 범위비율 기준 순위
    print("\n📏 Range Ratio Ranking:")
    range_ranking = variance_df.sort_values('Range_Ratio', ascending=False)
    for i, (idx, row) in enumerate(range_ranking.iterrows(), 1):
        print(f"  {i}. {idx:15s}: {row['Range_Ratio']:6.2f} ({row['Range_Grade']})")
    
    # 3. IQR계수 기준 순위
    print("\n📦 IQR Coefficient Ranking:")
    iqr_ranking = variance_df.sort_values('IQR_Coeff', ascending=False)
    for i, (idx, row) in enumerate(iqr_ranking.iterrows(), 1):
        print(f"  {i}. {idx:15s}: {row['IQR_Coeff']:6.3f} ({row['IQR_Grade']})")

# ==================== 수정된 시각화 함수들 ====================

def create_comprehensive_visualizations(df, variance_df, numeric_data):
    """종합적인 편차 분석 시각화"""
    
    # 개별 시각화 함수들 호출
    plot_variance_comparison_bars(variance_df)
    plot_variance_heatmap(variance_df)
    plot_distribution_boxplots(df, numeric_data)
    plot_cv_classification_pie(variance_df)
    plot_variance_correlation(variance_df)
    plot_combined_ranking(variance_df)
    plot_scatter_comparison(variance_df)
    
    plt.show()

def plot_variance_comparison_bars(variance_df):
    """1. 편차 지표 비교 막대 그래프"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('📊 Variance Metrics Comparison', fontsize=16, fontweight='bold')
    
    # 색상 팔레트
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
    
    # 1-1. 변동계수 (CV)
    cv_data = variance_df.sort_values('CV(%)', ascending=True)
    bars1 = axes[0,0].barh(cv_data.index, cv_data['CV(%)'], color=colors[:len(cv_data)])
    axes[0,0].set_title('🔥 Coefficient of Variation (CV%)', fontsize=12, fontweight='bold')
    axes[0,0].set_xlabel('CV (%)')
    axes[0,0].grid(axis='x', alpha=0.3)
    
    # CV 기준선 추가
    axes[0,0].axvline(15, color='green', linestyle='--', alpha=0.7, label='Low (15%)')
    axes[0,0].axvline(25, color='orange', linestyle='--', alpha=0.7, label='Medium (25%)')
    axes[0,0].axvline(50, color='red', linestyle='--', alpha=0.7, label='High (50%)')
    axes[0,0].legend(fontsize=8)
    
    # 1-2. 범위대비 평균 비율
    range_data = variance_df.sort_values('Range_Ratio', ascending=True)
    bars2 = axes[0,1].barh(range_data.index, range_data['Range_Ratio'], color=colors[:len(range_data)])
    axes[0,1].set_title('📏 Range to Mean Ratio', fontsize=12, fontweight='bold')
    axes[0,1].set_xlabel('Range / Mean')
    axes[0,1].grid(axis='x', alpha=0.3)
    
    # 1-3. 사분위수 범위 계수
    iqr_data = variance_df.sort_values('IQR_Coeff', ascending=True)
    bars3 = axes[1,0].barh(iqr_data.index, iqr_data['IQR_Coeff'], color=colors[:len(iqr_data)])
    axes[1,0].set_title('📦 IQR Coefficient', fontsize=12, fontweight='bold')
    axes[1,0].set_xlabel('IQR / Median')
    axes[1,0].grid(axis='x', alpha=0.3)
    
    # 1-4. 표준편차
    std_data = variance_df.sort_values('Std', ascending=True)
    bars4 = axes[1,1].barh(std_data.index, std_data['Std'], color=colors[:len(std_data)])
    axes[1,1].set_title('📈 Standard Deviation', fontsize=12, fontweight='bold')
    axes[1,1].set_xlabel('Standard Deviation')
    axes[1,1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_variance_heatmap(variance_df):
    """2. 편차 지표 히트맵 (수정됨)"""
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('🌡️ Variance Metrics Heatmap Analysis', fontsize=16, fontweight='bold')
    
    # 2-1. 수치 히트맵 (숫자 데이터만 사용)
    variance_numeric = variance_df[['CV(%)', 'Range_Ratio', 'IQR_Coeff']].T
    
    # 데이터 타입 확인 및 변환
    variance_numeric = variance_numeric.astype(float)
    
    sns.heatmap(variance_numeric, annot=True, cmap='YlOrRd', fmt='.2f', 
                cbar_kws={'label': 'Value'}, ax=axes[0])
    axes[0].set_title('📊 Variance Metrics Values', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Variables')
    axes[0].set_ylabel('Metrics')
    
    # 2-2. 등급 히트맵
    grade_mapping = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
    
    grade_data = pd.DataFrame({
        'CV_Grade': variance_df['CV_Grade'].map(grade_mapping),
        'Range_Grade': variance_df['Range_Grade'].map(grade_mapping),
        'IQR_Grade': variance_df['IQR_Grade'].map(grade_mapping)
    }).T
    
    sns.heatmap(grade_data, annot=True, cmap='RdYlBu_r', fmt='.0f',
                cbar_kws={'label': 'Grade (1:Very Low ~ 5:Very High)'}, ax=axes[1])
    axes[1].set_title('🎯 Variance Grade Comparison', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Variables')
    axes[1].set_ylabel('Grade')
    
    plt.tight_layout()
    plt.show()

def plot_distribution_boxplots(df, numeric_data):
    """3. 데이터 분포 박스플롯"""
    
    n_cols = len(numeric_data)
    n_rows = (n_cols + 3) // 4
    
    fig, axes = plt.subplots(n_rows, 4, figsize=(16, 4*n_rows))
    fig.suptitle('📦 Data Distribution (Box Plots)', fontsize=16, fontweight='bold')
    
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
    
    for i, col in enumerate(numeric_data):
        row = i // 4
        col_idx = i % 4
        
        box_plot = axes[row, col_idx].boxplot(df[col], patch_artist=True, 
                                             boxprops=dict(facecolor=colors[i % len(colors)]))
        axes[row, col_idx].set_title(f'{col}', fontsize=10, fontweight='bold')
        axes[row, col_idx].grid(True, alpha=0.3)
        
        # 통계 정보 추가
        mean_val = df[col].mean()
        median_val = df[col].median()
        axes[row, col_idx].axhline(mean_val, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean_val:.3f}')
        axes[row, col_idx].axhline(median_val, color='blue', linestyle='--', alpha=0.7, label=f'Median: {median_val:.3f}')
        axes[row, col_idx].legend(fontsize=7)
    
    # 빈 서브플롯 제거
    for i in range(len(numeric_data), n_rows * 4):
        row = i // 4
        col_idx = i % 4
        fig.delaxes(axes[row, col_idx])
    
    plt.tight_layout()
    plt.show()

def plot_cv_classification_pie(variance_df):
    """4. CV 등급별 파이 차트"""
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('🥧 Variance Grade Distribution', fontsize=16, fontweight='bold')
    
    # 색상 설정
    colors = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C', '#9B59B6']
    grade_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    
    # 4-1. CV 등급 분포
    cv_counts = variance_df['CV_Grade'].value_counts()
    cv_counts = cv_counts.reindex(grade_order, fill_value=0)
    
    wedges1, texts1, autotexts1 = axes[0].pie(cv_counts.values, labels=cv_counts.index, 
                                              autopct='%1.1f%%', colors=colors[:len(cv_counts)],
                                              startangle=90, explode=[0.1 if x > 0 else 0 for x in cv_counts.values])
    axes[0].set_title('🔥 CV Grade Distribution', fontsize=12, fontweight='bold')
    
    # 4-2. 범위비율 등급 분포
    range_counts = variance_df['Range_Grade'].value_counts()
    range_counts = range_counts.reindex(grade_order, fill_value=0)
    
    wedges2, texts2, autotexts2 = axes[1].pie(range_counts.values, labels=range_counts.index,
                                              autopct='%1.1f%%', colors=colors[:len(range_counts)],
                                              startangle=90, explode=[0.1 if x > 0 else 0 for x in range_counts.values])
    axes[1].set_title('📏 Range Ratio Grade Distribution', fontsize=12, fontweight='bold')
    
    # 4-3. IQR계수 등급 분포
    iqr_counts = variance_df['IQR_Grade'].value_counts()
    iqr_counts = iqr_counts.reindex(grade_order, fill_value=0)
    
    wedges3, texts3, autotexts3 = axes[2].pie(iqr_counts.values, labels=iqr_counts.index,
                                              autopct='%1.1f%%', colors=colors[:len(iqr_counts)],
                                              startangle=90, explode=[0.1 if x > 0 else 0 for x in iqr_counts.values])
    axes[2].set_title('📦 IQR Coefficient Grade Distribution', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def plot_variance_correlation(variance_df):
    """5. 편차 지표간 상관관계"""
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('🔗 Correlation Analysis Between Variance Metrics', fontsize=16, fontweight='bold')
    
    # 5-1. 상관계수 히트맵
    correlation_data = variance_df[['CV(%)', 'Range_Ratio', 'IQR_Coeff']].corr()
    
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0,
                square=True, fmt='.3f', ax=axes[0])
    axes[0].set_title('📊 Correlation Coefficients', fontsize=12, fontweight='bold')
    
    # 5-2. 산점도
    axes[1].scatter(variance_df['CV(%)'], variance_df['Range_Ratio'], 
                   s=100, alpha=0.7, c='red', label='CV vs Range Ratio')
    
    # 선형 회귀선 추가
    z = np.polyfit(variance_df['CV(%)'], variance_df['Range_Ratio'], 1)
    p = np.poly1d(z)
    axes[1].plot(variance_df['CV(%)'], p(variance_df['CV(%)']), "r--", alpha=0.8)
    
    axes[1].set_xlabel('CV (%)')
    axes[1].set_ylabel('Range Ratio')
    axes[1].set_title('🎯 CV vs Range Ratio Correlation', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # 각 점에 변수명 라벨링
    for i, txt in enumerate(variance_df.index):
        axes[1].annotate(txt, (variance_df['CV(%)'].iloc[i], variance_df['Range_Ratio'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)
    
    plt.tight_layout()
    plt.show()

def plot_combined_ranking(variance_df):
    """6. 종합 순위 비교"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('🏆 Comprehensive Ranking Comparison', fontsize=16, fontweight='bold')
    
    # 순위 데이터 생성
    cv_rank = variance_df['CV(%)'].rank(ascending=False)
    range_rank = variance_df['Range_Ratio'].rank(ascending=False)
    iqr_rank = variance_df['IQR_Coeff'].rank(ascending=False)
    
    # 6-1. 순위 비교 선 그래프
    x_pos = range(len(variance_df))
    
    axes[0,0].plot(x_pos, cv_rank, 'o-', label='CV Rank', linewidth=2, markersize=8)
    axes[0,0].plot(x_pos, range_rank, 's-', label='Range Ratio Rank', linewidth=2, markersize=8)
    axes[0,0].plot(x_pos, iqr_rank, '^-', label='IQR Coeff Rank', linewidth=2, markersize=8)
    
    axes[0,0].set_xticks(x_pos)
    axes[0,0].set_xticklabels(variance_df.index, rotation=45, ha='right')
    axes[0,0].set_ylabel('Rank (Lower = Higher Variance)')
    axes[0,0].set_title('📈 Ranking Changes by Metrics', fontsize=12, fontweight='bold')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].invert_yaxis()  # 순위는 낮을수록 좋으므로
    
    # 6-2. 순위 차이 히트맵
    rank_diff = pd.DataFrame({
        'CV_Rank': cv_rank,
        'Range_Rank': range_rank,
        'IQR_Rank': iqr_rank
    })
    
    sns.heatmap(rank_diff.T, annot=True, cmap='RdYlBu_r', fmt='.0f', ax=axes[0,1])
    axes[0,1].set_title('🎯 Ranking Heatmap', fontsize=12, fontweight='bold')
    
    # 6-3. 평균 순위
    avg_rank = (cv_rank + range_rank + iqr_rank) / 3
    avg_rank_sorted = avg_rank.sort_values()
    
    bars = axes[1,0].bar(range(len(avg_rank_sorted)), avg_rank_sorted.values, 
                        color=plt.cm.viridis(np.linspace(0, 1, len(avg_rank_sorted))))
    axes[1,0].set_xticks(range(len(avg_rank_sorted)))
    axes[1,0].set_xticklabels(avg_rank_sorted.index, rotation=45, ha='right')
    axes[1,0].set_ylabel('Average Rank')
    axes[1,0].set_title('🏅 Overall Variance Ranking (Average)', fontsize=12, fontweight='bold')
    axes[1,0].grid(axis='y', alpha=0.3)
    
    # 값 표시
    for i, bar in enumerate(bars):
        height = bar.get_height()
        axes[1,0].text(bar.get_x() + bar.get_width()/2., height + 0.05,
                      f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    # 6-4. 순위 일치도
    rank_consistency = pd.DataFrame({
        'CV-Range': np.abs(cv_rank - range_rank),
        'CV-IQR': np.abs(cv_rank - iqr_rank),
        'Range-IQR': np.abs(range_rank - iqr_rank)
    })
    
    rank_consistency.plot(kind='bar', ax=axes[1,1], color=['skyblue', 'orange', 'lightgreen'])
    axes[1,1].set_title('📊 Ranking Consistency', fontsize=12, fontweight='bold')
    axes[1,1].set_ylabel('Rank Difference')
    axes[1,1].set_xlabel('Variables')
    axes[1,1].legend(fontsize=8)
    axes[1,1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_scatter_comparison(variance_df):
    """7. 산점도 비교 분석"""
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('🎯 Scatter Plot Comparison Between Metrics', fontsize=16, fontweight='bold')
    
    # 7-1. CV vs 범위비율
    axes[0].scatter(variance_df['CV(%)'], variance_df['Range_Ratio'], 
                   s=150, alpha=0.7, c='red', edgecolors='black', linewidths=1)
    
    for i, txt in enumerate(variance_df.index):
        axes[0].annotate(txt, (variance_df['CV(%)'].iloc[i], variance_df['Range_Ratio'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
    
    axes[0].set_xlabel('CV (%)')
    axes[0].set_ylabel('Range Ratio')
    axes[0].set_title('CV vs Range Ratio', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # 7-2. CV vs IQR계수
    axes[1].scatter(variance_df['CV(%)'], variance_df['IQR_Coeff'], 
                   s=150, alpha=0.7, c='blue', edgecolors='black', linewidths=1)
    
    for i, txt in enumerate(variance_df.index):
        axes[1].annotate(txt, (variance_df['CV(%)'].iloc[i], variance_df['IQR_Coeff'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
    
    axes[1].set_xlabel('CV (%)')
    axes[1].set_ylabel('IQR Coefficient')
    axes[1].set_title('CV vs IQR Coefficient', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # 7-3. 범위비율 vs IQR계수
    axes[2].scatter(variance_df['Range_Ratio'], variance_df['IQR_Coeff'], 
                   s=150, alpha=0.7, c='green', edgecolors='black', linewidths=1)
    
    for i, txt in enumerate(variance_df.index):
        axes[2].annotate(txt, (variance_df['Range_Ratio'].iloc[i], variance_df['IQR_Coeff'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
    
    axes[2].set_xlabel('Range Ratio')
    axes[2].set_ylabel('IQR Coefficient')
    axes[2].set_title('Range Ratio vs IQR Coefficient', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def create_summary_dashboard(df, variance_df):
    """8. 종합 대시보드"""
    
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('📊 Abalone Data Variance Analysis Dashboard', fontsize=18, fontweight='bold')
    
    # 그리드 설정 (4x4)
    gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
    
    # 1. 상위 편차 변수들 (왼쪽 상단)
    ax1 = fig.add_subplot(gs[0, :2])
    top_cv = variance_df.nlargest(5, 'CV(%)')
    bars1 = ax1.bar(top_cv.index, top_cv['CV(%)'], color='red', alpha=0.7)
    ax1.set_title('🔥 Top 5 High Variance Variables (CV)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('CV (%)')
    ax1.grid(axis='y', alpha=0.3)
    
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 2. 편차 등급 분포 (오른쪽 상단)
    ax2 = fig.add_subplot(gs[0, 2:])
    cv_counts = variance_df['CV_Grade'].value_counts()
    colors_pie = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C', '#9B59B6']
    wedges, texts, autotexts = ax2.pie(cv_counts.values, labels=cv_counts.index, 
                                      autopct='%1.1f%%', colors=colors_pie, startangle=90)
    ax2.set_title('🥧 CV Grade Distribution', fontsize=12, fontweight='bold')
    
    # 3. 상관관계 히트맵 (왼쪽 중간)
    ax3 = fig.add_subplot(gs[1, :2])
    corr_data = variance_df[['CV(%)', 'Range_Ratio', 'IQR_Coeff']].corr()
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, ax=ax3, fmt='.2f')
    ax3.set_title('🔗 Correlation Between Metrics', fontsize=12, fontweight='bold')
    
    # 4. 산점도 (오른쪽 중간)
    ax4 = fig.add_subplot(gs[1, 2:])
    scatter = ax4.scatter(variance_df['CV(%)'], variance_df['Range_Ratio'], 
                         s=100, alpha=0.7, c='purple')
    ax4.set_xlabel('CV (%)')
    ax4.set_ylabel('Range Ratio')
    ax4.set_title('🎯 CV vs Range Ratio', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. 박스플롯 (아래 전체)
    ax5 = fig.add_subplot(gs[2:, :])
    
    # 편차가 높은 상위 4개 변수의 분포
    high_variance_vars = variance_df.nlargest(4, 'CV(%)').index
    box_data = [df[var].values for var in high_variance_vars]
    
    box_plot = ax5.boxplot(box_data, labels=high_variance_vars, patch_artist=True)
    colors_box = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for patch, color in zip(box_plot['boxes'], colors_box):
        patch.set_facecolor(color)
    
    ax5.set_title('📦 Distribution of High Variance Variables', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Values')
    ax5.grid(True, alpha=0.3)
    
    plt.show()

def main():
    df, numeric_data, min_max_df, variance_df = create_dataframe()
    
    print("\n" + "="*60)
    print("🎨 Starting Visualization Analysis...")
    print("="*60)
    
    # 모든 시각화 실행
    create_comprehensive_visualizations(df, variance_df, numeric_data)
    
    # 종합 대시보드
    create_summary_dashboard(df, variance_df)
    
    return df, variance_df

if __name__ == '__main__':
    df, variance_analysis = main()
