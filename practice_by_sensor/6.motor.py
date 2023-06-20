import RPi.GPIO as GPIO
import time

# 서보모터가 연결된 GPIO 핀 번호
SERVO_PIN = 17

# 라즈베리파이 GPIO 핀 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM 주파수 설정 (50Hz는 서보모터에 적합)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

try:
    while True:
        # 0도로 이동
        servo.ChangeDutyCycle(2.5)  # duty cycle = 2.5%
        time.sleep(1)

        # 180도로 이동
        servo.ChangeDutyCycle(12.5)  # duty cycle = 12.5%
        time.sleep(1)
        
except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()
