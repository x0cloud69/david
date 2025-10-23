import pandas as pd
import os

file_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_dir,"성__연령_및_가구주와의_관계별_인구__시군구_20250924183417.csv")

with open(file_path,"r",encoding='cp949') as file:
   df = pd.read_csv(file)

# 1. csv file 으로 pandas 로 읽어서 출력
print(df)

# 2. 컬럼중 일반가구원 만 살리기
df_house = df[['시점','성별','연령별','일반가구원']]
# 3. 행 중에 : 계,합계,15~64세,65세이상 은 제외하기
# df_columns = df_house["연령별"].unique()
# print(df_columns)


df_house = df_house[~df_house['성별'].isin(['계'])]
df_house = df_house[~df_house['연령별'].isin(['합계','15~64세','65세이상'])]

# 연령별 순서 정의 (실제 연령 순서대로)
age_order = ['15세미만', '15~19세', '20~24세', '25~29세', '30~34세', 
             '35~39세', '40~44세', '45~49세', '50~54세', '55~59세', 
             '60~64세', '65~69세', '70~74세', '75~79세', '80~84세', '85세이상']

# Categorical 타입으로 변환하여 순서 지정
df_house['연령별'] = pd.Categorical(df_house['연령별'], categories=age_order, ordered=True)

print("연령별 순서 확인:")
print(df_house['연령별'].cat.categories)
print(df_house)

# 3. 2015년 이후 남여의 연도별 일반가구원 데이타 통계
df_house_gender_year = df_house.groupby(['시점','성별']).sum('일반가구원')
print(df_house_gender_year)

# 4.2015년 이후 연령별 일반가구원 데이타 통계
df_house_age = df_house.groupby(['시점','연령별']).sum('일반가구원')
print(df_house_age)

# 5. 2015년 이후 남여의 연령별 일반가구원 통계 꺽은선 graph 그리기
df_house_gender_age_year = df_house.groupby(['성별','연령별']).sum('일반가구원')
print(df_house_gender_age_year)
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 8

sns.lineplot(data=df_house_gender_age_year,x='연령별',y='일반가구원',hue='성별',marker='o',linestyle='-',color='b')
plt.show()

