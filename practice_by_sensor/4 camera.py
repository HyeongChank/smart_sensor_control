from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5) # 5초간 프리뷰 화면을 띄웁니다
camera.capture('/home/pi/Desktop/image.jpg') # 지정한 경로에 사진을 저장합니다
camera.stop_preview()


camera.start_preview()
camera.start_recording('/home/pi/Desktop/video.h264') # 지정한 경로에 비디오를 녹화 시작
sleep(5) # 5초간 녹화
camera.stop_recording() # 녹화 중지
camera.stop_preview()