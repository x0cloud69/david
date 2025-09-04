import zipfile
import os

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
zip_path = 'C:\codyssey\emergency_storage_key.zip'
#zip_path = 'C:\codyssey\input_log.zip'
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
                            
                            with zipfile.ZipFile(zip_path,'r') as zip_file:
                                extract_folder = "extracted_files"
                                os.makedirs(extract_folder,exist_ok=True)

                                encode_pwd = temp_pwd.encode() if temp_pwd else None
                                try:
                                    zip_file.extractall(extract_folder,pwd=encode_pwd)
                                    print(f"암축이 해제 되었습니다.")
                                    success = True
                                    break
                                except:
                                    seq += 1
                                    print(f"반복횟수 : {seq}  Password : {temp_pwd}")
                                    continue
except KeyboardInterrupt:
    print("\n 프로그램이 강제 종료 되었습니다")
finally:
    if success:
        print(f"\n 암호를 찾았습니다.")
        print(f"암호 : {temp_pwd}")
        print(f"시도 횟수 : {seq}")


