import os
import cv2
from datetime import datetime
from ultralytics import YOLO
import queue
import time

processed_path = "processed/"
if not os.path.exists(processed_path):
    os.makedirs(processed_path)

model = YOLO("best_n.pt")

def consume_tasks(task_queue):
    """큐에서 작업 소비"""
    # timeout = time.time() + 60  # 60초 동안 작업이 없다면 종료
    while True:
        try:
            # timeout을 설정하여 무한 대기 방지
            task = task_queue.get(timeout=10)  # 1초 동안만 대기
            if task is None:  # 종료 신호
                break

            timestamp, rider_crop, plate_crop, rider_box, plate_box = task

            # 작업 처리
            # print('-'*40)
            # print(f"Rider 영역에서 검출 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            rider_results = model.predict(rider_crop, verbose=False)
            detections = rider_results[0].boxes

            has_rider = False
            has_without_helmet = False
            has_number_plate = False

            for box in detections:
                cls = int(box.cls[0].item())
                if cls == 0:  # Rider 클래스
                    has_rider = True
                    # print("Rider 검출됨")
                elif cls == 1:  # Without helmet 클래스
                    has_without_helmet = True
                    # print("Without Helmet 검출됨")
                elif cls == 3:  # 번호판 클래스
                    has_number_plate = True
                    # print("Number Plate 검출됨")

            # Step 2: 검출 결과 확인
            if has_rider and has_without_helmet and has_number_plate:
                # print("Rider 내 Without Helmet과 Number Plate 모두 확인됨")
                rider_path = f"{processed_path}rider_{timestamp}.png"
                cv2.imwrite(rider_path, rider_crop, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                # print(f"Rider 이미지 저장 완료: {rider_path}")
            # else:
            #     print("Rider 내 객체 검출 실패: Without Helmet 또는 Number Plate 없음")

        except queue.Empty:
            continue  # 타임아웃 시 계속 진행

    # print("소비 스레드 종료")