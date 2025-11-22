"""
제공되는 abalone.txt, abalone_attributes.txt 두 개의 파일을 읽어 들여서 DataFrame 객체로 만든다.  
전복은 유아기 때는 성별이 정해지지 않다가 성장하면서 성별이 정해지는 특성이 있다. 
따라서 성별 데이터를 Sex 컬럼에서 가지고 와서 따로 label이라는 항목으로 가져온다.
기존의 DataFrame에 있는 성별 데이터는 삭제해 준다.
준비된 데이터를 가져와서 살펴보면 각각의 항목의 크기의 편차가 큰 것을 알 수 있다.
각각의 항목의 크기의 편차가 클 경우에 추후 데이터처리에서 문제가 될 수 있기 때문에 Min-Max Scaling을 해준다.
Min-Max Scaling은 직접 수식을 구현해서 만들어보는 것과 sklearn.preprocessing에 있는 패키지로 구현하는 것 두 가지 방법을 모두 사용해 본다.
"""
import pandas as pd


def create_dataframe():
    with open(r'C:\codyssey\david\ky-codyssey-main\Codyseey\AI_1\과정4\문제9\abalone_attributes.txt',encoding='utf-8') as f:
        attribute = f.read().strip().split('\n')
        
    column_names = [attr.strip() for attr in attribute]
    # print(column_names) 
    
    df = pd.read_csv(r'C:\codyssey\david\ky-codyssey-main\Codyseey\AI_1\과정4\문제9\abalone.txt',header=None,names=column_names)    
    # print(df)
    
    df_label = df.copy()
    df_label['label'] = df_label['Sex']
    # print(df_label)
    df_label['Sex'] = ''
    # print(df_label)
    
    numeric_data = df_label.select_dtypes(include=['float64','int64']).columns
    
    
    _min_max_ = pd.DataFrame(
        {
            '최소값' : df[numeric_data].min(),
            '최대값' : df[numeric_data].max(),
            '범위'   : df[numeric_data].max() - df[numeric_data].min()
        }
    )
    
    print(_min_max_)
    
    
def main():
    create_dataframe()
    
if __name__ == '__main__':
    main()