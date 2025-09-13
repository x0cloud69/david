########################################
# ZIP 파일 열기 (암호 없는것)
########################################

import zipfile
import os
from datetime import datetime

def open_zip_file(zip_path):
    try:
        with zipfile.ZipFile(zip_path,'r') as zip_file:
            print("\n[ZIP 파일 정보]")
            print(f"파일 개수 : {len(zip_file.filelist)} 개" )

            # 파일 목록과 정보 출력
            print("\n[포함된 파일 목록]")
            print(f"{'파일명' :<30} {'크기':>10} {'압축크기':>10} {'수정일자' :<20}")
            print("-" * 72)

            for file_info in zip_file.filelist:
                file_name = file_info.filename
                file_size = file_info.file_size
                file_compress = file_info.compress_size
                file_date     = datetime(*file_info.date_time)

            print (f"{file_name :<30}"
                   f"{file_size :>10,d}"
                   f"{file_compress :>10,d}"
                   f"{file_date.strftime('%Y-%m-%d %H:%M:%S') :<20}")
        
        #압축 해제 여부 확인
        while True:
            response = input('\n 파일을 압축 해제 하시겠습니까 ? (y/n)')
            if response.lower() in ['y','n']:
                break
            print("'y' 또는 'n'으로 답해 주세요")
        
        if response.lower() == 'y':
            extract_folder = input("\n 압축 해제할 폴더명을 입력하세요 ")
            if not extract_folder:
                extract_folder = "extracted_files"

            os.makedirs(extract_folder,exist_ok=True)

            print(f"\n{extract_folder} 폴더에 파일 추출 중 ...")
            zip_file.extractall(path=extract_folder)
            print("압축 해제가 완료되었습니다.")

            #압축 해재된 파일 목록 출력
            print("\n [압축 해제된 파일 목록]")
            for root, dirs, files in os.walk(extract_folder):
                for file in files:
                    full_path = os.path.join(root,file)
                    print(f" - {full_path}")
        else:
            print("\n 압축 해제를 취소 했습니다.")
    except Exception as e:
        print(f"\에러 발생 {str(e)}")

if __name__ == "__main__":
    print("ZIP 파일 열기 프로그램")
    print("=" * 30)

    while True:
        zip_path = input("\n Zip 파일 입력하세요")
        if os.path.exists(zip_path):
            break
        print("파일이 존재 하지 않습니다, 다시 입력하세요")

    open_zip_file(zip_path)
    