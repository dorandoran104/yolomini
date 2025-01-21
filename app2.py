import cv2
import os
from ultralytics import YOLO
from datetime import datetime
from queue import Queue
from threading import Thread
from thread_processing2 import consume_tasks
import yt_dlp
# YOLO 모델 로드
model = YOLO("best_n.pt")

# 큐 생성
task_queue = Queue()

# 소비 스레드 실행
consumer_thread = Thread(target=consume_tasks, args=(task_queue,))
consumer_thread.start()

# 영상 파일 로드
youtube_url = "https://www.youtube.com/watch?v=DfnMZDL6aVU"

ydl_opts = {
    "format": "best[ext=mp4][protocol=https]/best",
    "quiet": True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(youtube_url, download=False)
    video_url = info["url"]

cap = cv2.VideoCapture(video_url)
# video_url = "video_short.mp4"
# cap = cv2.VideoCapture(video_url)

# 스크린샷 저장 경로
capture_path = "capture/"
if not os.path.exists(capture_path):
    os.makedirs(capture_path)

def enqueue_task(queue, file_name, rider_crop, plate_crop, rider_box, plate_box):
    """큐에 작업 추가"""
    task_data = (file_name, rider_crop, plate_crop, rider_box, plate_box)
    queue.put(task_data)

frame_skip = 1
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # 일정 간격으로만 프레임 처리

    results = model.predict(frame, verbose=False)
    detections = results[0].boxes

    riders = []
    task_added = False  # 작업이 큐에 추가되었는지 확인하는 변수

    for box in detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0].item())

        if cls == 0:  # Rider class
            riders.append((x1, y1, x2, y2))

        if cls == 1:  # Without helmet
            for rx1, ry1, rx2, ry2 in riders:
                if rx1 <= x1 <= rx2 and ry1 <= y1 <= ry2:
                    for plate_box in detections:
                        np_x1, np_y1, np_x2, np_y2 = map(int, plate_box.xyxy[0])
                        np_cls = int(plate_box.cls[0].item())
                        if np_cls == 3 and rx1 <= np_x1 <= rx2 and ry1 <= np_y1 <= ry2:
                            # cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)
                            # cv2.rectangle(frame, (np_x1, np_y1), (np_x2, np_y2), (0, 255, 0), 2)
                            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            # cv2.putText(frame, "Without Helmet", (x1, y1 - 10),
                            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                            # 스크린샷 저장
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_name = f"{capture_path}screenshot_{timestamp}.png"
                            cv2.imwrite(file_name, frame)

                            rider_crop = frame[ry1:ry2, rx1:rx2]
                            plate_crop = frame[np_y1:np_y2, np_x1:np_x2]

                            # 작업 데이터를 큐에 추가
                            enqueue_task(task_queue, timestamp, rider_crop, plate_crop, 
                                         (rx1, ry1, rx2, ry2), (np_x1, np_y1, np_x2, np_y2))
                            task_added = True  # 작업이 추가됨

    # if not task_added:
    #     print("프레임에서 검출된 객체가 없어서 작업을 추가하지 않았습니다.")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# 종료 신호 보내기
task_queue.put(None)

# 소비 스레드 종료 대기
consumer_thread.join()
