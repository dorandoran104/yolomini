<details>
  <summary>25.01.20 요약</summary>

  # 25.01.20

날짜: 2025년 1월 20일
태그: 완료
    
  # 1. 미니 프로젝트
  
  - YOLO 기반으로 하는 간단한 실습을 진행하기로 하였다.
      
      우리 3조는 오토바이를 탐지하여 헬멧을 썼는지, 안썼는지, 번호판이 있는지를
      
      탐지하는걸 만들어 보기로 했다.
      
  
  # 2. 프로젝트 진행(주말 ~ 월요일)
  
  ## 2-1.데이터 서치
  
  - 유튜브, 구글을 통해 각자 최소 50장씩 데이터를 가져오기로 했다
  
  ## 2-2.라벨링 도구
  
  - RoboFlow
      
      <aside>
      💡
      
      **Roboflow**는 머신러닝 모델 개발과 데이터셋 준비를 위한 플랫폼으로, 특히 컴퓨터 비전 작업을 위한 강력한 툴을 제공합니다. 사용자는 Roboflow를 통해 이미지 주석을 추가하고, 다양한 형식으로 데이터셋을 변환하고, 모델을 훈련시키는 과정까지 쉽게 진행할 수 있습니다.
      
      ### 주요 기능:
      
      1. **이미지 주석 추가**: Roboflow는 다양한 객체 탐지, 분할, 분류 작업에 대해 쉽게 주석을 추가할 수 있는 툴을 제공합니다. 사용자 인터페이스는 매우 직관적이며, 경계 상자, 세그멘테이션 마스크, 라벨을 추가할 수 있습니다.
      2. **데이터셋 처리 및 전처리**: Roboflow는 데이터를 모델 학습에 적합한 형식으로 자동으로 변환할 수 있습니다. 예를 들어, PASCAL VOC, YOLO, COCO 등 다양한 형식으로 데이터셋을 변환할 수 있습니다. 또한 이미지 크기 조정, 회전, 플리핑, 색상 변형 등 다양한 데이터 증강(augmentation) 기능을 제공합니다.
      3. **모델 훈련**: Roboflow는 사용자가 준비한 데이터셋을 기반으로 직접 모델을 훈련시킬 수 있는 기능을 제공합니다. 이를 통해, 사용자들은 코드 작성 없이도 머신러닝 모델을 쉽게 학습시킬 수 있습니다.
      4. **클라우드 배포 및 API 제공**: 훈련된 모델은 Roboflow의 클라우드에서 배포할 수 있으며, API를 통해 쉽게 모델을 호출하고 실시간 예측을 할 수 있습니다.
      5. **협업 기능**: 여러 사람이 동일한 프로젝트에서 작업할 수 있는 협업 기능을 제공하여 팀원들이 데이터셋을 공유하고 주석을 함께 추가할 수 있습니다.
      </aside>
      
  - LabelImg
      
      <aside>
      💡
      
      [https://github.com/HumanSignal/labelImg](https://github.com/HumanSignal/labelImg)
      
      LabelImg는 이미지 주석 작업을 위한 오픈 소스 그래픽 툴로, 주로 객체 탐지 모델을 훈련하기 위해 이미지에 라벨을 붙이는 데 사용됩니다. 이 툴은 Python과 Qt5로 작성되었으며, 사용자가 이미지를 로드하고, 객체에 경계 상자를 그린 후 이를 라벨링하여 XML 형식(PASCAL VOC 포맷) 또는 YOLO 포맷으로 저장할 수 있습니다.
      
      LabelImg의 주요 기능:
      
      - **이미지 주석 추가**: 이미지에 객체의 경계 상자를 그리고 라벨을 추가할 수 있습니다.
      - **PASCAL VOC 및 YOLO 형식 지원**: 두 가지 주요 데이터 형식으로 주석을 저장할 수 있어, 다양한 머신러닝 프레임워크에서 사용할 수 있습니다.
      - **사용자 친화적인 GUI**: 직관적인 그래픽 인터페이스로, 클릭과 드래그만으로 쉽게 경계 상자를 추가할 수 있습니다.
      </aside>
      
  
  - roboflow는 라벨링을 쉽고, 팀원들과 같이 할 수 있다는 점이 장점이였는데
      
      유료라는 단점이 너무 커서 labelimg를 사용해 라벨링을 사용했다.
      
  
  ## 2-3.코드 작성
  
  - 다른 모델을 학습 하는동안 빠르게 n 모델을 작성 한 뒤
      
      추론 및 오토바이 헬멧 미착용자를 탐지하는 로직을 구성했다.
      
  
  # 3. 오늘의 문제점
  
  ## 3-1. 하드웨어의 문제
  
  나는 yolo11 의 m 모델을 사용해서 학습을 시키기로 했는데
  
  학원 컴퓨터는 gtx1060 인데 cuda를 사용했을때도 하루종일 학습을 완료하지 못했다
  
  결국 집에서 코랩을 통해 l 모델을 학습하였고,
  
  30분만에 끝났다…. 진작 사용했었어야 했다.
  
  ## 3-2. 라벨링 문제
  
  라벨링을 각자 50가지 이상 하기로 했었는데
  
  라벨 클래스 이름만 정하고 순서는 정하지 않았다.
  
  0 : rider
  
  1 : without helmet
  
  2 : with helmet
  
  3 : number plate
  
  로 다시 정의하고 오전에 다시 라벨링 작업에 들어갔다
  
  ## 3-3. 겹쳐있는 객체 탐지문제
  
  먼저 학습한 n모델로 추론하는 로직을 구현하였다.
  
  여기서 문제점이 발생되는데
  
  앞에 라이더가 검출되고, 뒤에서 헬멧 안쓴다고 검출이 되면
  
  해당 라이더를 헬멧 안쓴 라이더로 인식하는 문제가 발생되었다.
  
  이 프로젝트의 중요점은
  
  정확도도 중요하지만 아닌데 맞다고 검출되는 오류를 잡는게 제일 우선이라 생각해서
  
  이부분에 대해서 고민을 했다.
  
  <aside>
  💡
  
  먼저 해결법은 결제에 사용되는 검증 로직처럼
  
  간단한 n 모델로 먼저 1차 추론을 하고
  
  해당 부분을 crop 한뒤
  
  코랩으로 학습이 끝난 l 모델로 한번더 2차 검증을 했다.
  
  모든 상황이 걸러지는건 아니지만
  
  이부분에서 대부분 걸러지는 모습을 보여줬다
  
  </aside>
  
  ## 3-4. 프레임 드랍 문제
  
  3-3 처럼 해당 문제는 해결했는데
  
  모델이 한번에 2번 실행되니 cv2로 화면을 보게되면
  
  프레임이 현저히 떨어지는 경향이 있었다
  
  <aside>
  💡
  
  이부분은 현업에서 유지보수할때 쓰였던 로직 중
  
  스케쥴로 batch를 통해 플로우를 실행했던 기억이 있어서
  
  쓰레드를 사용하는 방법을 떠올랐다.
  
  </aside>
  
  ### 쓰레드? 프로세스?
  
  | 항목 | 프로세스 (Process) | 쓰레드 (Thread) |
  | --- | --- | --- |
  | **독립성** | 독립적으로 실행되며, 다른 프로세스와 메모리 공유 안 함 | 같은 프로세스 내에서 메모리 공간을 공유 |
  | **메모리** | 독립적인 메모리 공간 | 프로세스의 메모리 공간을 공유 |
  | **자원 소비** | 새로운 프로세스를 생성하는 데 많은 자원과 시간이 소요 | 쓰레드는 적은 자원으로 생성 가능 |
  | **오류 전파** | 하나의 프로세스 오류는 다른 프로세스에 영향 안 미침 | 쓰레드 오류는 같은 프로세스 내 다른 쓰레드에 영향 미칠 수 있음 |
  | **사용 예** | 웹 브라우저, 텍스트 에디터, 독립 실행 프로그램 등 | 서버에서 동시 요청 처리, 멀티태스킹 등 |
  | **이미지 처리** | 독립적인 프로세스로서 각 프로세스에서 독립적인 이미지 처리 가능, 자원 소비 많음 | 동일 프로세스 내에서 여러 쓰레드가 이미지 처리 작업을 병렬로 처리 가능, 자원 효율적 |
  | **HTTP 통신** | 각각의 HTTP 요청에 대해 별도의 프로세스를 생성하면, 요청을 독립적으로 처리 가능하지만, 자원 소모가 크고 느릴 수 있음 | HTTP 요청을 병렬로 처리할 수 있는 쓰레드를 활용하면, 빠르고 효율적인 처리 가능, 서버 자원 공유로 성능 향상 |
  
  ### **결론**
  
  <aside>
  💡
  
  검증을 할때 이미지 처리 및 서버에 정보를 옮기기 위해 통신을 하기 위해서는 
  
  스레드가 더 적합하다고 생각해 스레드를 사용했다.
  
  </aside>
    
  하지만 스레드를 통해 연산이 들어가면 그때 조금 드랍이 있어서
  
  모델의 경량화라던지 추후 생각해볼게 많은것같다.


</details>

<details>
  <summary>25.01.21 요약</summary>

  # 25.01.21

날짜: 2025년 1월 21일
태그: 완료

# 1. 오늘 한 일

## 1-1. fastapi 만들기

현재 프로젝트에서 2가지 모델을 사용해 돌리고 있는데

여기서 업스케일링과 ocr을 또 추가해서 사용하면

현저히 느려질것같았다.

그래서 업스케일링과 ocr부분은 따로 서버를 만들어 진행하기로 했다.

## 1-2. scheduler 사용하기

<aside>
💡

Python에서 **스케줄러**(Scheduler)는 특정 시간에 작업을 자동으로 실행할 수 있도록 도와주는 라이브러리입니다. 스케줄링은 주기적으로 또는 특정 시간에 특정 작업을 자동으로 실행해야 할 때 유용합니다. Python에서는 다양한 스케줄러 라이브러리가 있지만, 가장 많이 사용되는 것들은 **`schedule`** 라이브러리와 **`APScheduler`**입니다.

</aside>

영상처리를 한 뒤 crop이 된 사진을 하나하나 서버로 보내기엔

너무 자원 소모가 클것같아서

scheduler을 사용해서 보내기로 했다.

| 특징 | **`schedule`** | **`APScheduler`** |
| --- | --- | --- |
| **간단한 주기적 작업** | 주기적인 작업 예약이 필요할 때 간단하고 직관적 | 복잡한 작업 관리가 필요하지 않다면 과도한 기능이 될 수 있음 |
| **복잡한 스케줄링 요구** | 간단한 주기적 작업 외에는 적합하지 않음 | 고급 스케줄링(예: `cron` 스타일 예약, 병렬 처리)이 필요할 때 적합 |

이왕 해보는거 APScheduler를 사용해서 스케쥴러를 등록했다.

- 코드
    
    ```python
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
    
    ```
    

# 2. 오늘의 문제점

## 2-1. 이미지 화질

블랙박스 영상을 구할 수 있는곳이 유튜브 밖에 없어서

실시간으로 스트리밍을 받아 처리하도록 구현을 했는데

이때 헬멧 안쓴 라이더를 탐지하게되면 크롭을 한다.

이 크롭된 사진을 서버에다가 넘겨주는데

이때 화질이 너무 좋지 않아서 번호판의 번호를 추출하는데 어려움이 있었다.

### 2-1-1. 업스케일링의 한계

이때 업스케일링을 통해 화질을 올린 뒤 추출하려고 시도를 했다.

하지만 이미 화질이 좋지 않아 깨진 글씨는 추출하는데 어려움이 있었다.

## 2-2. 1프레임이 아닌 여러 프레임에서 추출하기

강사님의 도움을 받아 이런 방법도 있다고 알려주셔서 해당 방법도 시도를 해봤다.

### 2-2-1. 트래킹 사용 시도

yolo모델에 자체적으로 트래킹을 처리할 수 있는 게 있었다.

이걸 토대로 라이더의 id를 추출해서 id별로 스크린샷 혹은 동영상을 추출하게

로직을 구현해봤다.

여기서 문제점은 내장되어있는 트래킹을 사용하면 id값이 계속 달라진다는 것이다.

이것때문에 폴더는 1장당 계속 생성되는 무서운 일이 벌어졌다.

### 2-2-2. 트래킹 라이브러리 사용

- DeepSort
    
    ### DeepSORT의 특징:
    
    - **추적 알고리즘**: DeepSORT는 객체를 추적하는 데 사용되며, 영상 내에서 각 객체를 고유하게 식별하고 추적하는 기능을 제공합니다.
    - **기반 모델**: DeepSORT는 기본적으로 **SORT(Simple Online and Realtime Tracking)** 알고리즘을 확장한 것입니다. SORT는 기본적인 칼만 필터와 하푼 거리 계산을 사용하여 객체를 추적하는 알고리즘이지만, DeepSORT는 **딥러닝** 기반의 **특징 추출기**(feature extractor)를 추가하여 객체의 외형적인 특성을 기반으로 추적의 정확도를 높입니다.
    - **특징 추출기**: DeepSORT는 객체의 외형적인 특성을 추출하기 위해 **CNN(Convolutional Neural Network)** 기반의 모델을 사용합니다. 이 특징 정보는 객체가 비슷한 크기나 모양을 가진 다른 객체와 혼동되지 않도록 도와줍니다.
    

해당 라이브러리를 사용해서 id값이 변하지 않도록 구현까지 끝냈다.

하지만 문제는 프레임 드랍현상이였다.

연산하는 양이 많아져서 그런지 성능이 매우 안좋아졌다.

15프레임 단위로 연산하게, 각종 설정을 줬지만

8초 동영상이 14초까지 걸리는걸 보고 해당 라이브러리는 현재 프로젝트와 맞지 않다고 느껴서 포기를 했다.

하루종일 번호판 추출에 대해 고민하고 시도해보고 해봤지만

하드웨어 문제 및 영상 화질이 낮을때 추출하는방법을 모두 실패했다.

deepsort를 이용해 추가적인 로직을 구현 할 수 있을것같지만

블랙박스에 넣는다는 생각으로 시작한 프로젝트라

이렇게 많은 연산이 들어가게 되면 블랙박스와 동떨어진곳에서 돌려야 할 것 같았다.

그래도 3일안에 구현해야했던 우리 프로젝트는

번호판 추출은 제외하고 헬멧 안쓴 라이더를 탐지하는건 구현이 되었다.

몸상태도 좋지 않아 머리가 잘 안돌아가서 어떻게 돌파구를 찾아야할지도 떠오르지 않았다

맥북도 살려달라고 아우성을 치는것같았다…

</details>

