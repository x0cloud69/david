import zipfile
import os

zip_path = input("Zip File 경로를 입력 하세요 : ")
zip_passwd = input("Zip File 의 암호를 입력 하세요 : ")

try:
    with zipfile.ZipFile(zip_path,'r') as zip_file:
        extrator_folder = "extracted_files"
        os.makedirs(extrator_folder,exist_ok=True)

        #암호가 입력된 경우 bytes 로 변환
        encode_pwd = zip_passwd.encode() if zip_passwd else None

        try:
            zip_file.extractall(extrator_folder,pwd=encode_pwd)
            print(f"파일이 {extrator_folder}에 압축 해제 되었습니다.")
        except Exception as e:
            if "Bad Password" in str(e):
                print("잘못된 암호입니다")
            else:
                print(f"암축 해제중 오류 발생 : {str(e)}")

except Exception as e:
    print(f"에러 발생 : {str(e)}")