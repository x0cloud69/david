import os
import zipfile
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import matplotlib.patches as patches
#import glob
import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time


file_path = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(file_path,"cctv.zip")
# with zipfile.ZipFile(zip_path) as zip_file:
#   zip_file.extractall("CCTV")
#   print("CCTV.ZIP 파일이 압축 해제 되었습니다.")

# CCTV 폴더의 모든 이미지 파일 가져오기
cctv_folder = os.path.join(file_path, "CCTV")
#image_files = sorted(glob.glob(os.path.join(cctv_folder, "*.jpg")))
current_index = 0

class MasImageHelper:
    def __init__(self):
      #  self.image_files = sorted(glob.glob(os.path.join(cctv_folder, "*.jpg")))
        self.current_index = 0
        
    def show_image(self, index):
        """지정된 인덱스의 이미지를 표시"""
        if 0 <= index < len(self.image_files):
            img = mpimg.imread(self.image_files[index])
            
            plt.clf()  # 이전 이미지 지우기
            plt.imshow(img)
            plt.title(f"CCTV 이미지 ({index + 1}/{len(self.image_files)}) - {os.path.basename(self.image_files[index])}")
            plt.axis('off')
          #  plt.draw()

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
            
    def get_image_files(self,directory):
        # 허용할 이미지 확장자 
        allowed_extensions = ['.jpg','.png','.jpeg','bmp']
        
        image_files = []
        
        for file in os.listdir(directory):
            # 파일의 확장자 추출
            ext = os.path.splitext(file)[1].lower()
            if ext in allowed_extensions:
                image_files.append(os.path.join(directory,file))
                
        return image_files
    
    def create_onnx_model(self):
        """YOLOv8 모델을 ONNX 형식으로 변환"""
        ONNX_MODEL_PATH = os.path.join(file_path, 'yolov8n.onnx')
        
        if not os.path.exists(ONNX_MODEL_PATH):
            print("ONNX 모델을 생성 중...")
            model = YOLO('yolov8n.pt')
            model.export(format='onnx', imgsz=640)
            print(f"ONNX 모델이 생성되었습니다: {ONNX_MODEL_PATH}")
        
        return ONNX_MODEL_PATH
    
            
    def detect_face_multi_params(self, image):
        # ONNX 모델 생성 또는 로드
        ONNX_MODEL_PATH = self.create_onnx_model()
        PERSON_CLASS_ID = 0 # 사람 클래스 ID COCO 데이터셋에서 0번 인덱스
        
        # 1. 모델 및 원본 이미지 로드
        net = cv2.dnn.readNetFromONNX(ONNX_MODEL_PATH)
        original_height, original_width = image.shape[:2] 
        
        # 2. 여러 파라미터로 검출 시도 (ONNX 모델은 640x640 고정 크기만 지원)
        param_combinations = [
            {"imgsz": 640, "conf": 0.25, "iou": 0.45},  # YOLOv8 기본값 (가장 균형 잡힘)
            {"imgsz": 640, "conf": 0.1, "iou": 0.5},    # 낮은 신뢰도 (숨어있는 객체 찾기)
            {"imgsz": 640, "conf": 0.4, "iou": 0.6},    # 높은 신뢰도 (빠른 속도, 명확한 객체만)
            {"imgsz": 640, "conf": 0.05, "iou": 0.3},   # 매우 낮은 신뢰도 (작은 객체 찾기)
        ]
    
        best_detections = []
        best_count = 0
        
        for i, params in enumerate(param_combinations):
            print(f"\n--- 파라미터 조합 {i+1}: {params} ---")
            imgsz = params["imgsz"]
            conf_threshold = params["conf"]
            iou_threshold = params["iou"] 
            
            # 3. 이미지 전처리
            blob = cv2.dnn.blobFromImage(image, 1/255.0, (imgsz, imgsz),swapRB=True, crop=False)
            
            # 4. 추론 실행 
            net.setInput(blob)
            final_layer = net.getUnconnectedOutLayersNames()
            outputs = net.forward(net.getUnconnectedOutLayersNames())
            

            # 5. 추론 결과 후처리
            output_data = outputs[0].T
            
            boxes, confidences, class_ids = [], [], []
            
            # 비율계산 : 원본 이미지 크기와 모델 입력 크기의 비율
            x_factor = original_width / imgsz
            y_factor = original_height / imgsz
            
            for row in output_data:
                # 가장 높은 클래스 점수를 신뢰도로 사용
                class_score = row[4:]
                confidence = np.max(class_score)
             
                
                if confidence > conf_threshold:
                    class_id = np.argmax(class_score)
                    print("class_id:", class_id)
                    print("confidence:", confidence)
                    print("class_score:", class_score)
                    if class_id == PERSON_CLASS_ID:
                        # 박스 좌표를 원본 이미지 크기에 맞게 변환 
                        cx, cy, w, h = row[:4]
                        x = int((float(cx) - float(w)/2) * x_factor)
                        y = int((float(cy) - float(h)/2) * y_factor)
                        width = int(float(w) * x_factor)
                        height = int(float(h) * y_factor)
                        
                        boxes.append([x, y, width, height])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        
            # 6. 겹치는 박스 제거 (NMS 를 통과한 박스들의 인덱스를 반환)
            indices = cv2.dnn.NMSBoxes(boxes,confidences,conf_threshold,iou_threshold)
            
            current_detections = []
            
            if len(indices) > 0:
                for idx in indices.flatten():
                    x, y, w, h = boxes[idx]
                    conf       = confidences[idx]
                    # 최종 결과를 (x1, y1, x2, y2, 신뢰도) 형태로 저장
                    current_detections.append((x, y, x+w, y+h,conf))
            
            print(f"검출된 사람 수: {len(current_detections)}")
            
            if len(current_detections) > best_count:
                best_detections = current_detections
                best_count = len(current_detections)
                print(f"새로운 최고 결과! ({best_count}명)")
        
        print(f"\n최종 선택된 검출 수: {len(best_detections)}")
        return best_detections
    
if __name__ == "__main__":
    try:
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기본 한글 폰트
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
        
        # 이미지 헬퍼 객체 생성
        image_helper = MasImageHelper()

        result = image_helper.get_image_files(cctv_folder)
        print(f"총 {len(result)}개의 CCTV 이미지를 찾았습니다.")
        image_file = result[0]
        
        
        # 모든 이미지 처리
        for i, image_file in enumerate(result):
            print(f"\n=== 이미지 {i+1}/{len(result)} 처리 중 ===")
            
            # 이미지 로드
            img = cv2.imread(image_file)
            if img is None:
                print(f"이미지를 로드할 수 없습니다: {image_file}")
                continue
                    
            # 사람 검출
            final_result = image_helper.detect_face_multi_params(img)
                
            # 검출 결과를 이미지에 그리기
            for j, (x1, y1, x2, y2, conf) in enumerate(final_result):
                # 사각형 그리기 (BGR 색상 순서: 빨간색 = (0, 0, 255))
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # 텍스트 쓰기
                label = f"Person {j+1}: {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # 결과 표시
            cv2.namedWindow("Final Detection Result", cv2.WINDOW_NORMAL)
            cv2.imshow("Final Detection Result", img)
                
            print(f"검출된 사람 수: {len(final_result)}")
            print("이미지를 보려면 아무 키나 누르세요...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
                
            # 사용자 입력 대기 (다음 이미지로 넘어가려면 Enter)
            if i < len(result) - 1:  # 마지막 이미지가 아닌 경우
                input("다음 이미지를 보려면 Enter를 누르세요...")
                
        
        
    except ImportError:
        print("matplotlib이 설치되지 않았습니다. pip install matplotlib로 설치하세요.")
