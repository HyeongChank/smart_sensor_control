



# 스마트 센서 네트워크 설계 및 장비를 활용한 생산 공정 자동 제어, 모니터링 시스템 구축하기

## 모바일을 통한 모니터링 및 제어(07.26)
- Test로 안드로이드 - 파이썬 소켓을 통한 연동(O)
- 프로젝트에 적용해야 함(Todo)


## 라즈베리파이 센서를 통한 데이터 수집 연습
### LED 켜기(06.05)
- GPIO(Gnenral Prupose Input Output: 범용입출력) 라이브러리 사용
- 점퍼 케이블(라즈베리파이, 브레드보드 연결), LED, 저항 연결
    - LED 왼쪽-GPIO / LED 오른쪽-저항-GND
### 스위치 입력 시 LED 점등하기(06.09)
- pull_up_down

### 온습도 측정(06.19)
- Adafruit_DHT 모듈 사용
- VCC-5V / GND-GND / DATA-GPIO 연결

### 카메라 모듈로 사진, 동영상 촬영(06.20)
- PiCamera 모듈 사용
- .capture / .start_recording
- 라즈베리파이 카메라 설정
    - sudo raspi-config -> interface options -> legacy camera -> yes -> finish
    - 재부팅 -> vcgencmd get_camera(카메라 연결 확인) -> raspistill -o test.jpg(test 촬영)

### 진동감지 시 LED 켜기(06.21)
- GPIO.IN(스위치와 동일)
- VCC-5V / GND-GND / DO-GPIO

### 충돌감지(06.22)
- GPIO.IN(진동감지 센서와 동일)
- VCC-5V / GNd-GND / OUT-GPIO
- pull-down 저항 활성화 : 저전압(OV), 입력 없을 때 LOW 상태 유지
- pull-up 저항 활성화 : VCC, 입력 없을 때 HIGH 상태 유지


> 충돌감지
<img width="200" height="200" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/c9e7f7f3-7599-46c6-80fd-6ed4fffc13b8"/>

> 진동감지에 따른 LED 조명 On
<img width="200" height="200" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/0d671ea5-7567-4161-9b9c-fba7abc75560"/>

> 동영상(카메라)
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/b2269571-27de-4cec-ab94-c4ab68821a6c"/>

> 사진(카메라)
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/114b1aa8-c49f-45ab-9340-eeb5bd8a9e54"/>

> 온습도
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/e919baae-1be2-4c43-a0fe-ba2997a9dc58"/>

> 스위치
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/4ecca2e1-a5e6-47e0-8b33-2d3f8ff8b52b"/>

> LED 켜기
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/083a0c25-f94a-447f-9058-7998667e6243"/>




