import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) 

# PWM 주파수를 50Hz로 설정하여 GPIO 18 핀의 PWM 인스턴스 생성
pwm = GPIO.PWM(18, 50)  
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(18, True)  
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(18, False)  
    pwm.ChangeDutyCycle(0)


try:
    while True:
        # 원하는 각도로 회전시키기 (0-180)
        SetAngle(90)  # 중앙 위치
        time.sleep(2)
        SetAngle(0)   # 왼쪽 극한 위치
        time.sleep(2)
        SetAngle(180) # 오른쪽 극한 위치
        time.sleep(2)
    
finally:
    pwm.stop()
    GPIO.cleanup()
