import pandas as pd
import os

file_path = os.path.join(os.path.dirname("__file__"))
file_name = os.path.join(file_path,'spaceship_titanic','train.csv')

df = pd.read_csv(file_name)

df_test = df.copy()
df_test['Transported1'] = 'ABC'
df_test['Transported_Num'] = df_test['Transported'].astype(int)
print(df_test.head())

# 나이대 그룹 추가 
print("==== 나이대 그룹 추가 ====")
df_test['AgeGroup']=df_test['Age'].apply(lambda age: 0 if pd.isna(age) else  float(age//10) * 10)
df_test['AgeGroup'] = df_test['AgeGroup'].astype(int)

print(df_test.head())


#
df_test_value = df_test['Destination'].value_counts()

print(df_test_value)
collec_list = []
correlations = {}
correlations['VRDeck'] = df_test['VRDeck'].corr(df_test['Transported_Num'])
correlations['Spa'] = df_test['Spa'].corr(df_test['Transported_Num'])
correlations['FoodCourt'] = df_test['FoodCourt'].corr(df_test['Transported_Num'])
correlations['RoomService'] = df_test['RoomService'].corr(df_test['Transported_Num'])
correlations['Age'] = df_test['Age'].corr(df_test['Transported_Num'])

collec_list.append(correlations)

correlations['Transported_Num'] = df_test['Transported_Num'].corr(df_test['VRDeck'])
correlations['Spa'] = df_test['Spa'].corr(df_test['VRDeck'])
correlations['FoodCourt'] = df_test['FoodCourt'].corr(df_test['VRDeck'])
correlations['RoomService'] = df_test['RoomService'].corr(df_test['VRDeck'])
correlations['Age'] = df_test['Age'].corr(df_test['VRDeck'])

collec_list.append(correlations)
print(collec_list)
for idx in range(len(collec_list)):
  for key, value in collec_list[idx].items():
      print(f"key:{key}, Value : {value:.4f}")
      
print('-'*60)
# 범주형 상관 관계
cate_collect_list = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP']

cate_list = []
cross_tab = pd.crosstab(df_test['HomePlanet'],df_test['Transported_Num'],normalize='index')
print(cross_tab)



