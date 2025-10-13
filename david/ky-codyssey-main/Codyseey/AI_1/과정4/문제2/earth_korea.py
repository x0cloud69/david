import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

file_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_dir, '성__연령_및_가구주와의_관계별_인구__시군구_20250924183417.csv')

file = pd.read_csv(file_path,encoding='cp949')
print(file)

df = pd.DataFrame(file)
print(df)

#가구주의 배우자        자녀 자녀의 배우자  ... 외손자녀·그 배우자 증손자녀·그 배우자    조부모 형제자매· 그 배우자 형제자매의 자녀·그 배우자 부모의 형제자매·그 배우자 기타 친·인척  기타 동거인
drop_columns = ['가구주의 배우자', '자녀', '자녀의 배우자', '가구주의 부모', '배우자의 부모', '손자녀 그 배우자',  '증손자녀·그 배우자', '조부모', '형제자매·그 배우자', '형제자매의 자녀·그 배우자', '부모의 형제자매·그 배우자', '기타 친·인척', '기타 동거인','가구주','친손자녀·그 배우자','외손자녀·그 배우자']
df2 = df.drop(drop_columns, axis=1)
print(df2)
df3 = df2.groupby(['시점','성별','연령별'], as_index=False).sum('일반가구원')
print(df3)
df4 = df2.groupby(['시점','연령별'], as_index=False).sum('일반가구원')
print(df4)

# 한글 폰트 설정
font_list = ['Malgun Gothic', 'NanumGothic', 'AppleGothic', 'Batang', 'Gulim']
for font_name in font_list:
    try:
        font_path = fm.findfont(fm.FontProperties(family=font_name))
        if font_path:
            plt.rcParams['font.family'] = font_name
            break
    except:
        continue
        
plt.rcParams['axes.unicode_minus'] = False

# 성별로 구분된 데이터 준비 (합계 제외)
df_gender = df3[df3['성별'] != '계'].copy()
df_gender_year = df_gender.groupby(['시점', '성별'], as_index=False)['일반가구원'].sum()

# 피벗 테이블로 남/여 데이터 분리
df_pivot = df_gender_year.pivot(index='시점', columns='성별', values='일반가구원')

#plt.figure(figsize=(10,6))
fig, ax = plt.subplots(figsize=(12,8))

# 남/여 구분하여 꺾은선 그래프 그리기
df_pivot.plot(kind='line', ax=ax, color=['blue', 'red'], marker='o', linewidth=2, markersize=6)
ax.set_title('연도별 성별 일반가구원 수', fontsize=15)
ax.set_xlabel('연도', fontsize=12)
ax.set_ylabel('일반가구원 수', fontsize=12)
ax.legend(['남자', '여자'], fontsize=10)
ax.grid(True, alpha=0.3)   

plt.tight_layout()
plt.show() 

##시점 행정구역별(시군구)  성별     연령별     일반가구원
# df3 = df['시점'] + df['행정구역별(시군구)'] + df['성별'] + df['연령별'] + df['일반가구원']
# print(df3)