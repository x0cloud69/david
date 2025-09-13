import zipfile
import os
from datetime import datetime 

base_pwd = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

pwd_list_1 = base_pwd
pwd_list_2 = base_pwd
pwd_list_3 = base_pwd
pwd_list_4 = base_pwd
pwd_list_5 = base_pwd
pwd_list_6 = base_pwd

temp_pwd = ''

seq = 0
success = False
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
start_time_period = datetime.now()

file_path = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(file_path,"emergency_storage_key.zip")
write_path = os.path.join(file_path,"password.txt")
extract_folder = os.path.join(file_path,"extracted_files")

#zip_path = 'C:\codyssey\emergency_storage_key.zip'
#zip_path = 'C:\codyssey\input_log_1.zip'


def result(temp_pwd,seq,start_time,end_time,elapsed):
    with open(write_path,"w",encoding="utf-8") as file:
        file.write("="*30+"\n")
        file.write(f"암호 : {temp_pwd}\n")
        file.write(f"시도횟수 : {seq}\n")
        file.write(f"시작시간 : {start_time}\n")
        file.write(f"종료시간 : {end_time}\n")
        file.write(f"총 소요시간 : {elapsed}\n")
        file.write("="*30+"\n")



def unlock_zip():
    global success,seq,temp_pwd,end_time,elapsed,start_time_period
    try:
        for i1 in range(len(pwd_list_1)):
            if success:
                break
            for i2 in range(len(pwd_list_2)):
                if success:
                    break
                for i3 in range(len(pwd_list_3)):
                    if success:
                        break
                    for i4 in range(len(pwd_list_4)):
                        if success:
                            break
                        for i5 in range(len(pwd_list_5)):
                            if success:
                                break
                            for i6 in range(len(pwd_list_6)):
                                temp_pwd = str(pwd_list_1[i1])+str(pwd_list_2[i2])+str(pwd_list_3[i3])+str(pwd_list_4[i4])+str(pwd_list_5[i5])+str(pwd_list_6[i6])
 
                                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                end_time_period = datetime.now()
                                elapsed = end_time_period - start_time_period                               
                                with zipfile.ZipFile(zip_path,'r') as zip_file:
                                    #extract_folder = "extracted_files"
                                    os.makedirs(extract_folder,exist_ok=True)

                                    encode_pwd = temp_pwd.encode() if temp_pwd else None
                                    try:
                                        zip_file.extractall(extract_folder,pwd=encode_pwd)
                                        print(f"암축이 해제 되었습니다.")
                                        success = True
                                        # end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        # end_time_period = datetime.now()
                                        # elapsed = end_time_period - start_time_period
                                        result(temp_pwd,seq,start_time,end_time,elapsed)
                                        break
                                    except:
                                        seq += 1
                                        print(f"시작시간 : {start_time} 반복횟수 : {seq} 진행시간 : {str(elapsed)} Password : {temp_pwd}")
                                        continue
    except KeyboardInterrupt:
        print("\n 프로그램이 강제 종료 되었습니다")
    finally:
        if success:
            print(f"\n 암호를 찾았습니다.")
            print("="*30)
            print(f"암호 : {temp_pwd}")
            print(f"시도 횟수 : {seq}")
            print(f"시작시간 : {start_time}")
            print(f"종료시간 : {end_time}")
            print(f"총 소요시간 : {elapsed}")
            print("="*30)

if __name__ == "__main__":
    unlock_zip()

