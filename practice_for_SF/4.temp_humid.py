import Adafruit_DHT

# 온습도 센서의 타입과 GPIO 핀 번호를 지정합니다.
sensor = Adafruit_DHT.DHT11
pin = 4

# 센서에서 온도와 습도를 읽어옵니다.
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
