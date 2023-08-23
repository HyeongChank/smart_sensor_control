import cv2
from PIL import Image

# VideoCapture 객체 생성
cap = cv2.VideoCapture('http://172.30.1.46:8080/?action=stream')  # mjpg-streamer URL

# 배경제거 객체 생성
fgbg = cv2.createBackgroundSubtractorMOG2()

count = 0  # 움직이는 물체 감지 횟수
motion_detected = False  # 움직임 감지 여부

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)  # 배경제거
    
    # 노이즈 제거
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
    # 컨투어 찾기
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True
    
    if motion_detected:
        count += 1
        print("Detected object count:", count)

    # OpenCV 이미지를 PIL로 변환하고 표시
    im_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    im_pil.show()

    # fgmask를 표시하고 싶다면 아래의 코드 추가
    mask_pil = Image.fromarray(fgmask)
    mask_pil.show()

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
