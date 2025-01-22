from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
import yt_dlp
import time  # 시간 측정을 위한 모듈

# YOLO 모델 로드
model = YOLO("best_n.pt")

# DeepSORT 초기화
tracker = DeepSort(max_age=10, max_iou_distance=0.9, nn_budget=50)

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
# cap.set(cv2.CAP_PROP_FPS, 30)
frame_count = 0
update_interval = 15  # 매 5 프레임마다 추적 업데이트

# tracks를 while 루프 밖에서 초기화
tracks = []

# FPS 계산을 위한 시간 변수
prev_time = time.time()

start_time = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # YOLO 감지
    results = model(frame,verbose=False)

    # 일정 간격으로만 추적기 업데이트
    if frame_count % update_interval == 0:
        detections = []
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])  # 클래스 ID
                if cls in [0]:  # 클래스 0(person), 3(motorcycle)만 추적
                    conf = box.conf[0].item()
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))

        # DeepSORT 업데이트
        tracks = tracker.update_tracks(detections, frame=frame)

        # tracks가 초기화되지 않으면 빈 리스트로 처리
        if tracks is None:
            tracks = []

    # 결과 그리기
    if tracks:  # tracks가 빈 리스트가 아니면 그리기
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            bbox = track.to_ltrb()
            x1, y1, x2, y2 = map(int, bbox)
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

end_time = time.time()
print(f"총 소요 시간: {end_time - start_time:.2f}초")

cap.release()
cv2.destroyAllWindows()
