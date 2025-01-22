import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# 저장된 이미지 폴더 경로
capture_folder = "capture/"
process_folder = "processed/"

# 폴더가 없다면 생성
if not os.path.exists(capture_folder):
    os.makedirs(capture_folder)
if not os.path.exists(process_folder):
    os.makedirs(process_folder)

# 서버 URL
server_url = "http://0.0.0.0:8000/upload"

# 스케줄러 인스턴스를 전역 변수로 관리
scheduler = None

def send_images_to_server():
    """capture 및 process 폴더 내의 이미지를 서버로 전송"""
    # capture 폴더와 process 폴더에서 파일 목록 가져오기
    files_in_capture_folder = [f for f in os.listdir(capture_folder) if os.path.isfile(os.path.join(capture_folder, f))]
    files_in_process_folder = [f for f in os.listdir(process_folder) if os.path.isfile(os.path.join(process_folder, f))]
    
    # 두 폴더에서 파일들을 합침
    all_files = files_in_capture_folder + files_in_process_folder

    if all_files:
        try:
            # 여러 파일을 서버에 전송할 수 있도록 딕셔너리 준비
            files_to_send = []
            for file_name in all_files:
                file_path = None
                if file_name in files_in_capture_folder:
                    file_path = os.path.join(capture_folder, file_name)
                elif file_name in files_in_process_folder:
                    file_path = os.path.join(process_folder, file_name)
                
                if file_path:
                    files_to_send.append(('files', open(file_path, 'rb')))
            
            # 파일 전송
            response = requests.post(server_url, files=files_to_send)
            if response.status_code == 200:
                print("모든 파일 전송 완료")
                
                # 전송 성공 후 파일 핸들 정리 및 파일 삭제
                for _, file_object in files_to_send:
                    file_object.close()  # 파일 핸들 닫기
                
                # 파일 삭제 (capture와 process 폴더 모두에서 삭제)
                for file_name in all_files:
                    if file_name in files_in_capture_folder:
                        file_path = os.path.join(capture_folder, file_name)
                    elif file_name in files_in_process_folder:
                        file_path = os.path.join(process_folder, file_name)
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)  # 파일 삭제
                        print(f"{file_name} 파일이 삭제되었습니다.")
            else:
                print(f"파일 전송 실패, 응답 코드: {response.status_code}")

        except Exception as e:
            print(f"파일 전송 중 오류: {e}")
    else:
        print("전송할 파일이 없습니다.")

def start_scheduler():
    """APScheduler 시작"""
    global scheduler

    # 이미 스케줄러가 실행 중이라면 다시 시작하지 않음
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_images_to_server, "interval", seconds=10)  # 10초마다 실행
        scheduler.start()
        print("스케줄러가 시작되었습니다.")
    else:
        print("스케줄러가 이미 실행 중입니다.")
    return scheduler
