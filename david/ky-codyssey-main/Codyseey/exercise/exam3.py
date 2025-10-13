import os

def read_log():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_src = 'mission_computer_main.log'
    file_path = os.path.join(file_dir,file_src)
    with open(file_path,'r',encoding='utf-8') as f:
        return f.read()


if __name__ == ("__main__"):
    log_list = read_log()
    # 1. 로그 파일 그대로 출력
    print(log_list)
    # 2. 로그 파일을 튜플 객체로 변환
    log_list_1 = log_list.strip().splitlines()
    log_tuples = []
    print(log_list_1)
    
    for line in log_list_1:
      if line:
        log_parts = line.split(',')
        log_tuple = tuple(log_parts)
        log_tuples.append(log_tuple)
    print(log_tuples)
    
# 3. 튜플 리스트 객체를 시간 역순으로 출력
    log_tuples.sort(key=lambda x:x[0],reverse=True)
    print(log_tuples)
    
########################################################
# 4. 튜플 리스트 객체를 딕셔너리 객체로 변환
########################################################
# 단계 : 1. 빈 사전객체 생성  
#        2. for in range(len(log_tuples)) 순회  
#        3. 딕셔너리[i]=리스트[i]
########################################################
    # log_dict = {}
    
    # for idx in range(len(log_tuples)):
    #   log_dict[idx] = log_tuples[idx]
    
    # print(log_dict)
    
########################################################
# 4-1. zip 함수 사용
########################################################
    log_dict_list = []
    
    keys = ['timestamp','event','message']
    
    for log_tuple in log_tuples:
      log_dict_zip = dict(zip(keys,log_tuple))
      log_dict_list.append(log_dict_zip)
    print("\n")
    print("======= Dictionary List ========")
    print("\n")
    print(log_dict_list)
    