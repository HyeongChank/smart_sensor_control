import RPi.GPIO as GPIO
import time

# 센서가 연결된 GPIO 핀 번호
channel = 17
led_channel = 2
# 라즈베리파이 GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(led_channel, GPIO.OUT)
pwm = GPIO.PWM(led_channel, 1000)   # LED 핀에 1000Hz의 PWM을 설정
pwm.start(0)    
# 진동 감지 후 수행할 작업
def perform_action():
    print("Performing action!")
    

# GPIO 핀 상태를 주기적으로 폴링하며 감지하는 함수
def poll_GPIO(channel):
    while True:
        # GPIO 핀의 상태를 확인
        if GPIO.input(channel):
            print("Vibration detected!")
            pwm.ChangeDutyCycle(100)
            perform_action()  # 진동 감지 후 수행할 작업 호출
        else:
            print("No vibration detected.")
            pwm.ChangeDutyCycle(0)
        
        time.sleep(1)  # 다음 상태 체크를 위해 잠시 대기

try:
    # GPIO 핀 상태 폴링 시작
    poll_GPIO(channel)
except KeyboardInterrupt:
    GPIO.cleanup()
