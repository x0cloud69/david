import zipfile
import os

zip_path = input("Zip File 경로를 입력 하세요 : ")

try:
    with zipfile.ZipFile(zip_path,'r') as zip_file:
        extrator_folder = "extracted_files"
        os.makedirs(extrator_folder,exist_ok=True)
        zip_file.extractall(extrator_folder)
        print(f"파일이 {extrator_folder}에 압축 해제 되었습니다.")
except Exception as e:
    print(f"에러 발생 : {str(e)}")