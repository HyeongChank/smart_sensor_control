import RPi.GPIO as GPIO
import time

# 충돌감지 센서의 GPIO 핀 번호 설정
SENSOR_PIN = 3

# GPIO 설정
GPIO.setmode(GPIO.BCM)
# pull_up_down = GPIO.PUD_DOWN 풀다운 저항 활성화(pull 당기다)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 충돌 감지 함수
def collision_detect():
    try:
        while True:
            # 센서로부터 읽기
            if GPIO.input(SENSOR_PIN)== GPIO.LOW:
                print("Collision detected!")
                time.sleep(1)
            else:
                print("no collision")
                time.sleep(1)
    except KeyboardInterrupt:
        print("error")
        # 마지막에는 GPIO cleanup
        GPIO.cleanup()

if __name__=='__main__':
    # 함수 실행
    collision_detect()




