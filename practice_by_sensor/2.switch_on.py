import RPi.GPIO as GPIO     
import time

GPIO.setmode(GPIO.BCM)

LED_pin = 2
sw_pin = 17
GPIO.setup(LED_pin, GPIO.OUT)
# 내부 풀다운 저항을 활성화하여, 스위치를 안 눌렀을 때, 저항활성화
# 즉, LOW인 상태
GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_input = 0

try:
    while True:
        input = GPIO.input(sw_pin)
        if ((not prev_input) and input):
            GPIO.output(LED_pin, GPIO.HIGH)
            print("pressed")
        else:
            GPIO.output(LED_pin, GPIO.LOW)
            # print("not pressed")
        prev_input = input
        time.sleep(0.05)  # debounce time of 50ms

finally: 
    GPIO.cleanup()
