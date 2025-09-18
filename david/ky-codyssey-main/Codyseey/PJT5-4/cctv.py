import os
import zipfile
#from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import glob



file_path = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(file_path,"cctv.zip")
with zipfile.ZipFile(zip_path) as zip_file:
  zip_file.extractall("CCTV")
  print("CCTV.ZIP 파일이 압축 해제 되었습니다.")

# CCTV 폴더의 모든 이미지 파일 가져오기

#image_files = sorted(glob.glob(os.path.join(cctv_folder, "*.jpg")))

        
current_index = 0

class MasImageHelper:
    def __init__(self):
        self.image_files = []
        self.current_index = 0
        
    def get_image_files(self,directory):
        extension = ['.jpg','.png','.jpeg','.bmp']  # 점(.) 추가
        image_files = []
        for file in os.listdir(directory):
            ext = os.path.splitext(file)[1].lower()
            if ext in extension:
                image_files.append(os.path.join(directory,file)) 
        return image_files        
        
        
    def show_image(self, index):
        """지정된 인덱스의 이미지를 표시"""
        if 0 <= index < len(self.image_files):
            img = mpimg.imread(self.image_files[index])
            
            plt.clf()  # 이전 이미지 지우기
            plt.imshow(img)
            plt.title(f"CCTV 이미지 ({index + 1}/{len(self.image_files)}) - {os.path.basename(self.image_files[index])}")
           #plt.axis('off')
            plt.draw()

    def on_key(self, event):
        if event.key == 'right' or event.key == 'd':
            # 오른쪽 화살표 또는 'd' 키
            print("다음 이미지로 이동")
            old_index = self.current_index
            self.current_index = (self.current_index + 1) % len(self.image_files)
            print(f"인덱스 변경: {old_index} → {self.current_index}")
            self.show_image(self.current_index)
        elif event.key == 'left' or event.key == 'a':
            # 왼쪽 화살표 또는 'a' 키
            print("이전 이미지로 이동")
            old_index = self.current_index
            self.current_index = (self.current_index - 1) % len(self.image_files)
            print(f"인덱스 변경: {old_index} → {self.current_index}")
            self.show_image(self.current_index)
        elif event.key == 'escape':
            # ESC 키로 종료
            print("프로그램 종료")
            plt.close()
        else:
            print(f"알 수 없는 키: {event.key}")

# matplotlib을 사용한 이미지 표시
if __name__ == "__main__":
    try:
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기본 한글 폰트
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

        cctv_folder = os.path.join(file_path, "CCTV")
        
        # 이미지 헬퍼 객체 생성
        image_helper = MasImageHelper()
        
        # 첫 번째 이미지 표시
        fig, ax = plt.subplots(figsize=(10, 10))
        image_helper.image_files = image_helper.get_image_files(cctv_folder)
      #  image_helper.image_files = image_files  # self.image_files에 저장
        image_helper.show_image(image_helper.current_index)
        
        # 키보드 이벤트 연결
        fig.canvas.mpl_connect('key_press_event', image_helper.on_key)
        
        # 사용법 안내
        print("키보드 조작법:")
        print("← (왼쪽 화살표) 또는 'a': 이전 이미지")
        print("→ (오른쪽 화살표) 또는 'd': 다음 이미지")
        print("ESC: 종료")
        
        plt.show()
        
    except ImportError:
        print("matplotlib이 설치되지 않았습니다. pip install matplotlib로 설치하세요.")
