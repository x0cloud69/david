import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

# 간단한 테스트용 스크립트
file_path = os.path.dirname(os.path.abspath(__file__))
cctv_folder = os.path.join(file_path, "CCTV")
image_files = sorted(glob.glob(os.path.join(cctv_folder, "*.jpg")))
current_index = 0

def show_image(index):
    """이미지 표시"""
    if 0 <= index < len(image_files):
        img = mpimg.imread(image_files[index])
        plt.clf()
        plt.imshow(img)
        plt.title(f"이미지 {index + 1}/{len(image_files)}")
        plt.axis('off')
        plt.draw()

def on_key(event):
    """키보드 이벤트 - 디버깅용"""
    global current_index
    
    # 여기에 중단점 설정해보세요!
    print(f"키 입력: {event.key}")
    print(f"현재 인덱스: {current_index}")
    
    if event.key == 'right':
        current_index = (current_index + 1) % len(image_files)
        print(f"다음 이미지: {current_index}")
        show_image(current_index)
    elif event.key == 'left':
        current_index = (current_index - 1) % len(image_files)
        print(f"이전 이미지: {current_index}")
        show_image(current_index)
    elif event.key == 'escape':
        plt.close()

# 메인 실행
plt.rcParams['font.family'] = 'Malgun Gothic'
fig, ax = plt.subplots(figsize=(8, 6))
show_image(current_index)
fig.canvas.mpl_connect('key_press_event', on_key)

print("테스트 시작 - 화살표 키를 눌러보세요!")
plt.show()
