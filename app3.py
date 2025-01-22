from ultralytics import YOLO
import cv2
import yt_dlp
from datetime import datetime
import os

model = YOLO('best_n.pt')

# 영상 파일 로드
youtube_url ="https://www.youtube.com/watch?v=DfnMZDL6aVU"

ydl_opts = {
    "format": "best[ext=mp4][protocol=https]/best",
    "quiet": True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(youtube_url, download=False)
    video_url = info["url"]

cap = cv2.VideoCapture(video_url)

# 추적할 클래스 (0: 'person', 1: 'car', 3: 'motorcycle' 등)
class_0 = 0  # 클래스 0
class_1 = 1  # 클래스 1
class_3 = 3  # 클래스 3

# 초기 상태 설정
is_recording = False
tracking_lost = False
current_folder = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame)  # 추적 결과 얻기
    
    # 클래스 0, 1, 3에 해당하는 박스 찾기
    class_0_boxes = []
    class_1_boxes = []
    class_3_boxes = []
    
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        classes = boxes.cls  # 클래스 정보는 boxes.cls로 접근
        
        # 클래스 0, 1, 3에 해당하는 박스들 분리
        for i, box in enumerate(boxes):
            if classes[i] == class_0:
                class_0_boxes.append(box)
            elif classes[i] == class_1:
                class_1_boxes.append(box)
            elif classes[i] == class_3:
                class_3_boxes.append(box)

    # 클래스 0 박스가 존재할 때, 1번과 3번 클래스가 모두 그 안에 있는지 확인
    class_1_in_0 = False
    class_3_in_0 = False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for box_0 in class_0_boxes:
        x1_0, y1_0, x2_0, y2_0 = box_0.xyxy[0].tolist()  # 클래스 0 박스 좌표

        # 클래스 0 박스에 사각형 그리기
        cv2.rectangle(frame, (int(x1_0), int(y1_0)), (int(x2_0), int(y2_0)), (255, 0, 0), 2)  # 클래스 0은 파란색
        
        # 클래스 1과 3이 클래스 0 박스 안에 있는지 확인
        class_1_in_0 = any(
            x1_0 <= x1_1 <= x2_0 and y1_0 <= y1_1 <= y2_0
            for box_1 in class_1_boxes
            for x1_1, y1_1, x2_1, y2_1 in [box_1.xyxy[0].tolist()]
        )
        class_3_in_0 = any(
            x1_0 <= x1_3 <= x2_0 and y1_0 <= y1_3 <= y2_0
            for box_3 in class_3_boxes
            for x1_3, y1_3, x2_3, y2_3 in [box_3.xyxy[0].tolist()]
        )
        
        # 클래스 1과 3이 모두 클래스 0 박스 내에 있을 경우
        if class_1_in_0 and class_3_in_0:
            if not is_recording:
                # 트래킹 시작 (새로운 폴더 생성)
                # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                current_folder = os.path.join("tracking_output", timestamp)
                os.makedirs(current_folder, exist_ok=True)
                is_recording = True
                tracking_lost = False
                print(f"Tracking started. Saving to folder: {current_folder}")

            # 클래스 0 영역을 크롭
            cropped_frame = frame[int(y1_0):int(y2_0), int(x1_0):int(x2_0)]
            
            # 스크린샷 파일명 생성
            screenshot_filename = os.path.join(current_folder, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.png")

            
            # 크롭된 이미지 저장
            cv2.imwrite(screenshot_filename, cropped_frame)
            print(f"Screenshot saved: {screenshot_filename}")
        
    # 트래킹 상태를 체크하고 트래킹을 놓친 경우 새로운 폴더 생성
    if not class_1_in_0 or not class_3_in_0:
        if is_recording:
            is_recording = False
            tracking_lost = True
            print("Tracking lost. Waiting for new tracking.")
    
    # 화면에 결과 출력
    cv2.imshow('frame', frame)

    # 'q' 키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
