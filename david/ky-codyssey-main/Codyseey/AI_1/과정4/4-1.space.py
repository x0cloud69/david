#
import zipfile
import os
import pandas as ps


zip_path = os.path.join(os.path.dirname(__file__))
zip_file = os.path.join(zip_path,'spaceship-titanic.zip')
with zipfile.ZipFile(zip_file) as zf:
  zf.extractall('spaceship_titanic')


f_test = ps.read_csv(os.path.join(zip_path,'spaceship_titanic','test.csv'))
f_train = ps.read_csv(os.path.join(zip_path,'spaceship_titanic','train.csv'))
f_test['Transported'] = None

f_merged = ps.concat([f_test,f_train],ignore_index=True)

print(f_merged.head())

# f_merged 저장 (파일이 열려있으면 건너뜀)
try:
    f_merged.to_csv(os.path.join(zip_path,'spaceship_titanic','f_merged.csv'),index=False)
    print("f_merged.csv 파일 저장 완료")
except PermissionError:
    print("f_merged.csv 파일이 열려있어서 저장을 건너뜁니다.")

print("전체 데이터 개수:", len(f_merged))
print("테스트 데이터 개수:", len(f_test))
print("훈련 데이터 개수:", len(f_train))

# 1단계: 데이터 구조 확인
print("\n=== 데이터 구조 확인 ===")
print("컬럼 정보:")
print(f_merged.info())

# 2단계: Transported 분포 확인
print("\n=== Transported 분포 ===")
transported_counts = f_train['Transported'].value_counts()
print("Transported 값 분포:")
print(transported_counts)
print(f"전송된 비율: {transported_counts[True] / len(f_train) * 100:.1f}%")

# 3단계: 숫자형 변수들과 Transported의 상관관계 분석
print("\n=== 기존 숫자형 변수 상관관계 분석 ===")

# 숫자형 컬럼만 선택 (훈련 데이터만 사용 - Transported 값이 있는 데이터)
numeric_columns = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']

# Transported를 숫자로 변환 (True=1, False=0)
f_train_numeric = f_train.copy()
f_train_numeric['Transported'] = f_train_numeric['Transported'].astype(int)

print("각 숫자형 변수와 Transported의 상관계수:")
for col in numeric_columns:
    if col in f_train_numeric.columns:
        correlation = f_train_numeric[col].corr(f_train_numeric['Transported'])
        print(f"{col:15}: {correlation:.4f}")

#%% 4단계: 범주형 변수들과 Transported의 관계 분석 (올바른 방법)
print("\n=== 범주형 변수 관계 분석 ===")

categorical_columns = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']  # HomePlanet 다시 포함

for col in categorical_columns:
    if col in f_train.columns:
        print(f"\n--- {col} ---")
        # 각 카테고리별 Transported 비율 계산
        cross_tab = ps.crosstab(f_train[col], f_train['Transported'], normalize='index') * 100
        print(f"{col}별 Transported 비율:")
        print(cross_tab.round(1))

#%% 5단계: 가장 중요한 변수들 정리
print("\n=== 결론: Transported와 가장 관련성이 높은 변수들 ===")

# 숫자형 변수의 절댓값 상관계수 정리
print("\n1. 숫자형 변수 중요도 (상관계수 절댓값 기준):")
correlations = {}
for col in numeric_columns:
    if col in f_train_numeric.columns:
        correlation = abs(f_train_numeric[col].corr(f_train_numeric['Transported']))
        correlations[col] = correlation

# 상관계수 크기순으로 정렬
sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
for i, (col, corr) in enumerate(sorted_correlations, 1):
    print(f"{i}. {col:15}: {corr:.4f}")

print("\n2. 범주형 변수 중요도 (비율 차이 기준):")
print("- CryoSleep: True(81.8%) vs False(32.9%) - 약 49% 차이!")
print("- HomePlanet: Europa(65.9%) vs Earth(42.4%) - 약 23% 차이")
print("- Destination: 55 Cancri e(61.0%) vs TRAPPIST-1e(47.1%) - 약 14% 차이")
print("- VIP: 일반(50.6%) vs VIP(38.2%) - 약 12% 차이")

print("\n3. 분석 방법 설명:")
print("- 숫자형 변수: 상관계수 (-1~1, 절댓값이 클수록 관련성 높음)")
print("- 범주형 변수: 각 카테고리별 전송 비율 차이 (차이가 클수록 관련성 높음)")
print("- HomePlanet은 순서가 없는 명목형 변수이므로 비율 분석이 올바른 방법")

#%% 6단계: 나이대별 Transported 비율 분석 및 시각화

class space_titanic:
  def __init__(self):
    self.f_train = f_train

  def get_age_group(self,age):
    if age < 20:
      return '10'
    elif age < 30:
      return '20'
    elif age < 40:
      return '30'
    elif age < 50:
      return '40'
    elif age < 60:
      return '50'
    elif age < 70:
      return '60'
    elif age < 80:
      return '70'
    else:
      return '80'
    
print("\n=== 나이대별 Transported 비율 분석 ===")

import matplotlib.pyplot as plt

age_list = ['10','20','30','40','50','60','70']
inst_st = space_titanic()

f_train_age = f_train.copy()
f_train_age['AgeGroup'] = f_train_age['Age'].apply(inst_st.get_age_group)

total_count = len(f_train_age)
group_count = round(f_train_age.groupby(['AgeGroup','Transported']).size()/total_count*100,1)

plot_data = group_count.unstack()
print("------  Plot Data ------")
print(plot_data)
print("------  Plot Data ------")

fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(12,8))

plot_data.plot(kind='bar',ax=ax[0],figsize=(12,8),rot=0)
ax[0].grid(axis='y',linestyle='--',linewidth=0.5)
ax[0].set_xlabel('Age Group',fontsize=12)
ax[0].set_ylabel('Percentage (%)',fontsize=12)
ax[0].set_title('Transported Rate by Age Group',fontsize=14,fontweight='bold')
# y축 범위 설정 (최댓값의 115%까지)
max_value = plot_data.values.max()
ax[0].set_ylim(0, max_value * 1.15)

# 각 막대 위에 값 표시
for i, age_group in enumerate(plot_data.index):
    # False (전송되지 않음) 막대 위에 값 표시
    false_value = plot_data.loc[age_group, False]
    ax[0].text(i - 0.2, false_value + 0.3, f'{false_value:.1f}%', 
               ha='center', va='bottom', fontsize=7, fontweight='bold')
    
    # True (전송됨) 막대 위에 값 표시  
    true_value = plot_data.loc[age_group, True]
    ax[0].text(i + 0.2, true_value + 0.3, f'{true_value:.1f}%', 
               ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()

### 보너스 문제 ###
print("==== 보너스 문제 ====")
f_destination = round(f_train_age.groupby(['Destination','AgeGroup']).size().unstack(fill_value=0)*100 / len(f_train_age),1)
print("Destination별 연령대별 비율:")
print(f_destination)

# f_destination 데이터를 사용해서 그래프 그리기
f_destination.plot(kind='bar', ax=ax[1], figsize=(12,8), rot=45)
ax[1].grid(axis='y', linestyle='--', linewidth=0.5)
ax[1].set_xlabel('Destination', fontsize=10)
ax[1].set_ylabel('Percentage (%)', fontsize=10)
ax[1].set_title('Age Group Distribution by Destination', fontsize=12, fontweight='bold')
ax[1].legend(title='Age Group', bbox_to_anchor=(1.05, 1), loc='upper left')

# 각 막대 위에 값 표시
for i, destination in enumerate(f_destination.index):
    for j, age_group in enumerate(f_destination.columns):
        value = f_destination.loc[destination, age_group]
        if value > 0:  # 0이 아닌 값만 표시
            ax[1].text(i + (j-3)*0.1, value + 0.2, f'{value:.1f}%', 
                      ha='center', va='bottom', fontsize=7, rotation=0)


plt.tight_layout()

plt.show()

