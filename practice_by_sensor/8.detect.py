import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def detect_motion(frame1, frame2):
    # 두 프레임 간의 차이를 계산
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

# 첫 프레임을 캡쳐
camera.capture(raw_capture, format="bgr")
frame1 = raw_capture.array

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    frame2 = frame.array

    # 움직임을 감지
    contours = detect_motion(frame1, frame2)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 500: # 임의의 값: 더 작거나 큰 움직임을 감지하려면 이 값을 조정하세요.
            continue
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame2)
    frame1 = frame2.copy()
    raw_capture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
