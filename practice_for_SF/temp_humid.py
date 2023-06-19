import Adafruit_DHT
import time
# Sensor type: DHT11
DHT_SENSOR = Adafruit_DHT.DHT11

# The pin which is connected with the sensor will be declared here
DHT_PIN = 2  # assuming the sensor data pin is connected to GPIO4
before_value = 0
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        if temperature > before_value:
            print("온도 상승")
        elif temperature < before_value:
            print("온도 감소")
        else:
            print("동일")
        before_value = temperature
    else:
        print("Failed to retrieve data from humidity sensor")
        
    time.sleep(3)
