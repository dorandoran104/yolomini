import cv2
import time
from deep_sort_realtime.deepsort_tracker import DeepSort
import yt_dlp
import torch
from ultralytics import YOLO
from fairmot import FairMOT

# YOLO 모델 로드
model = YOLO("best_n.pt")

# FairMOT 초기화
fairmot_model = FairMOT()

# 유튜브 동영상 로드
# youtube_url = "https://www.youtube.com/watch?v=E1_yVUhqSLw"
# ydl_opts = {
#     "format": "best[ext=mp4][protocol=https]/best",
#     "quiet": True,
# }
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(youtube_url, download=False)
#     video_url = info["url"]

video_url = "video_short.mp4"

cap = cv2.VideoCapture(video_url)
frame_count = 0
update_interval = 7  # 매 7 프레임마다 추적 업데이트

# FPS 계산을 위한 시간 변수
prev_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # YOLO 감지
    results = model(frame, verbose=False)

    # FairMOT 추적 업데이트
    if frame_count % update_interval == 0:
        detections = []
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])  # 클래스 ID
                if cls in [0]:  # 클래스 0(person)만 추적
                    conf = box.conf[0].item()
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))

        # FairMOT 업데이트
        fairmot_tracker = fairmot_model.update(detections, frame)

        # 결과 그리기
        if fairmot_tracker:
            for track in fairmot_tracker:
                x1, y1, x2, y2, track_id = track
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # FPS 계산
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)  # FPS 계산
    prev_time = curr_time

    # FPS 화면에 표시
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 화면 출력
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
