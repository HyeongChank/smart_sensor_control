import RPi.GPIO as GPIO
import time

# 충돌감지 센서의 GPIO 핀 번호 설정
SENSOR_PIN = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# 충돌 감지 함수
def collision_detect():
    while True:
        # 센서로부터 읽기
        if GPIO.input(SENSOR_PIN):
            print("Collision detected!")
            time.sleep(1)

# 함수 실행
collision_detect()

# 마지막에는 GPIO cleanup
GPIO.cleanup()



import simpy

# 충돌을 감지하면 호출되는 함수
def collision_handler(env):
    while True:
        print("Handling collision at time", env.now)
        yield env.timeout(1)  # 1 time unit 후에 다시 실행

# SimPy 환경 생성
env = simpy.Environment()

# 충돌 핸들러 프로세스를 환경에 추가
env.process(collision_handler(env))

# 시뮬레이션 시작
env.run(until=10)  # 10 time units 동안 실행
