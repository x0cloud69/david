import pandas as pd
import os

file_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_dir,"성__연령_및_가구주와의_관계별_인구__시군구_20250924183417.csv")

# 다운로드 받은 CSV 파일을 DataFrame 객체로 읽어들인다.
with open(file_path,"r",encoding='cp949') as file:
	df = pd.read_csv(file)

print(df)

#컬럼들 중에서 일반가구원을 제외한 나머지 컬럼들을 모두 삭제한다.
df_copy = df.copy()

# headers = df_copy.columns
# print(headers)

keep_list = ['시점','성별','연령별','일반가구원']

df_copy=df_copy[keep_list]
headers=df_copy.columns                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
print(headers)
print(df_copy)

unique_age = df_copy['연령별'].unique()
print(unique_age)

except_row = ['계','합계','15~64세' ,'65세이상']
df_copy=df_copy[~df_copy['성별'].isin(except_row)]
df_copy=df_copy[~df_copy['연령별'].isin(except_row)]
print(df_copy)

df_copy_sum = df_copy.groupby(['시점','성별'])[['일반가구원']].sum()
print(df_copy_sum)

df_copy_age = df_copy.groupby(['연령별'])[['일반가구원']].sum()
print(df_copy_age)


#### 최대기간의 성별/연령별 일반가구수 구하기
df_copy_gender_age = df_copy.groupby(['성별','연령별'])[['일반가구원']].sum()
print(df_copy_gender_age)

## Graph 로 

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

plt.figure(figsize=(12,8))
sns.lineplot(data=df_copy_gender_age,x='연령별',y='일반가구원',hue='성별',marker='o',linestyle='-',color='b')
plt.title('최대기간의 성별/연령별 일반가구수',fontsize=14,fontweight='bold')
plt.xlabel('연령별',fontsize=12)
plt.ylabel('일반가구원',fontsize=12)
plt.legend(title='성별',fontsize=12)
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.show()