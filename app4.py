from ultralytics import YOLO
import cv2
import yt_dlp
from datetime import datetime
import os

# YOLO 모델 로드
model = YOLO('best_n.pt')

# 영상 파일 로드
youtube_url = "https://www.youtube.com/watch?v=E1_yVUhqSLw"
ydl_opts = {
    "format": "best[ext=mp4][protocol=https]/best",
    "quiet": True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(youtube_url, download=False)
    video_url = info["url"]

cap = cv2.VideoCapture(video_url)

# 추적할 클래스 (0: 'person', 1: 'car', 3: 'motorcycle')
class_0 = 0  # 클래스 0 (person)
class_1 = 1  # 클래스 1 (car)
class_3 = 3  # 클래스 3 (motorcycle)

# 트래킹 객체
trackers = {}

# 스크린샷 저장할 디렉토리
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 추적 결과 얻기
    results = model.track(frame, verbose=False)

    # 클래스 0, 1, 3에 해당하는 박스 찾기
    class_0_boxes = []
    class_1_boxes = []
    class_3_boxes = []

    for result in results:
        boxes = result.boxes  # Bounding box 정보
        classes = boxes.cls   # 클래스 정보
        
        for i, box in enumerate(boxes):
            coords = box.xyxy[0].tolist()
            if int(classes[i]) == class_0:
                class_0_boxes.append(coords)
            elif int(classes[i]) == class_1:
                class_1_boxes.append(coords)
            elif int(classes[i]) == class_3:
                class_3_boxes.append(coords)

    # 클래스 0 박스에 대해 처리
    for x1_0, y1_0, x2_0, y2_0 in class_0_boxes:
        x1_0, y1_0, x2_0, y2_0 = map(int, (x1_0, y1_0, x2_0, y2_0))
        cv2.rectangle(frame, (x1_0, y1_0), (x2_0, y2_0), (255, 0, 0), 2)  # 파란색

        # 클래스 1과 3이 클래스 0 박스 내에 있는지 확인
        class_1_in_0 = any(
            x1_0 <= x1_1 <= x2_0 and y1_0 <= y1_1 <= y2_0
            for x1_1, y1_1, x2_1, y2_1 in class_1_boxes
        )
        class_3_in_0 = any(
            x1_0 <= x1_3 <= x2_0 and y1_0 <= y1_3 <= y2_0
            for x1_3, y1_3, x2_3, y2_3 in class_3_boxes
        )

        if class_1_in_0 and class_3_in_0:
            # 트래킹 ID
            tracking_id = f"{x1_0}_{y1_0}"

            # 트래커 생성 및 초기화
            if tracking_id not in trackers:
                tracker = cv2.TrackerCSRT_create()
                trackers[tracking_id] = tracker
                tracker.init(frame, (x1_0, y1_0, x2_0 - x1_0, y2_0 - y1_0))

            # 트래커 업데이트
            success, bbox = trackers[tracking_id].update(frame)
            if success:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 녹색

                # 스크린샷 저장
                tracking_folder = os.path.join(output_dir, tracking_id)
                os.makedirs(tracking_folder, exist_ok=True)

                screenshot_filename = os.path.join(
                    tracking_folder,
                    f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                )
                cv2.imwrite(screenshot_filename, frame)
                print(f"Screenshot saved: {screenshot_filename}")

    # 화면 출력
    cv2.imshow('frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
