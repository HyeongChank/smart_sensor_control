import RPi.GPIO as GPIO
import time

# 센서가 연결된 GPIO 핀 번호
SENSOR_PIN = 17

# 라즈베리파이 GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def callback_function(channel):
    # 여기서 "Vibration detected!" 대신에 원하는 기능을 수행하면 됩니다.
    print("Vibration detected!")

# 이벤트 감지 설정
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=callback_function)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
