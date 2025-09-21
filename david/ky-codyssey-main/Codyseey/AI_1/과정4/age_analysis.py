import zipfile
import os
import pandas as ps
import matplotlib.pyplot as plt
import numpy as np

# 데이터 불러오기
zip_path = os.path.join(os.path.dirname(__file__))
zip_file = os.path.join(zip_path,'spaceship-titanic.zip')
with zipfile.ZipFile(zip_file) as zf:
  zf.extractall('spaceship_titanic')

f_train = ps.read_csv(os.path.join(zip_path,'spaceship_titanic','train.csv'))

print("=== 나이대별 Transported 비율 분석 ===")

# 나이대 그룹 생성 함수
def get_age_group(age):
    if ps.isna(age):  # NaN 값 처리
        return 'Unknown'
    elif age < 20:
        return '10대'
    elif age < 30:
        return '20대'
    elif age < 40:
        return '30대'
    elif age < 50:
        return '40대'
    elif age < 60:
        return '50대'
    elif age < 70:
        return '60대'
    else:
        return '70대+'

# 나이대 그룹 컬럼 추가
f_train_age = f_train.copy()
f_train_age['AgeGroup'] = f_train_age['Age'].apply(get_age_group)

print("처음 5개 데이터 확인:")
print(f_train_age[['Age', 'AgeGroup', 'Transported']].head(10))

# 나이대별 Transported 비율 계산
age_transport_analysis = f_train_age.groupby(['AgeGroup', 'Transported']).size().unstack(fill_value=0)
age_transport_percentage = age_transport_analysis.div(age_transport_analysis.sum(axis=1), axis=0) * 100

print("\n나이대별 Transported 비율:")
print(age_transport_percentage.round(1))

print("\n나이대별 총 인원수:")
print(age_transport_analysis.sum(axis=1))

# 그래프 생성
plt.figure(figsize=(12, 8))

# 나이대 순서 정의
age_order = ['10대', '20대', '30대', '40대', '50대', '60대', '70대+']
# Unknown이 있다면 마지막에 추가
if 'Unknown' in age_transport_percentage.index:
    age_order.append('Unknown')

# 실제 데이터에 있는 나이대만 필터링
available_ages = [age for age in age_order if age in age_transport_percentage.index]

# 데이터 준비
transported_rates = [age_transport_percentage.loc[age, True] for age in available_ages]
not_transported_rates = [age_transport_percentage.loc[age, False] for age in available_ages]

# 막대그래프 생성
x = np.arange(len(available_ages))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width/2, not_transported_rates, width, label='Not Transported', color='skyblue', alpha=0.8)
bars2 = ax.bar(x + width/2, transported_rates, width, label='Transported', color='salmon', alpha=0.8)

# 그래프 꾸미기
ax.set_xlabel('Age Group', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_title('Transported Rate by Age Group', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(available_ages, rotation=45)
ax.legend()

# 막대 위에 퍼센트 표시
def add_value_labels(bars, values):
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=10)

add_value_labels(bars1, not_transported_rates)
add_value_labels(bars2, transported_rates)

plt.tight_layout()
plt.grid(axis='y', alpha=0.3)
plt.show()

print(f"\n그래프가 생성되었습니다!")

# 나이대별 주요 통계
print("\n=== 나이대별 주요 발견사항 ===")
for age in available_ages:
    transported_pct = age_transport_percentage.loc[age, True]
    total_count = age_transport_analysis.sum(axis=1)[age]
    print(f"{age}: {transported_pct:.1f}% 전송됨 (총 {total_count}명)")

# 가장 위험한 나이대와 안전한 나이대 찾기
max_transport_age = age_transport_percentage[True].idxmax()
min_transport_age = age_transport_percentage[True].idxmin()
max_rate = age_transport_percentage.loc[max_transport_age, True]
min_rate = age_transport_percentage.loc[min_transport_age, True]

print(f"\n🔴 가장 위험한 나이대: {max_transport_age} ({max_rate:.1f}% 전송)")
print(f"🟢 가장 안전한 나이대: {min_transport_age} ({min_rate:.1f}% 전송)")
print(f"📊 차이: {max_rate - min_rate:.1f}%포인트")

