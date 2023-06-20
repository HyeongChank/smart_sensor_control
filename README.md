# 라즈베리파이 센서를 통한 데이터 수집 연습
### 최종적으로 스마트 센서 네트워크 설계 및 장비를 활용한 생산 공정 자동 제어, 모니터링 시스템 구축하기

## LED 켜기(06.05)
- GPIO(Gnenral Prupose Input Output: 범용입출력) 라이브러리 사용
- 점퍼 케이블(라즈베리파이, 브레드보드 연결), LED, 저항 연결

## 스위치 입력 시 LED 점등하기(06.09)
- pull_up_down

## 온습도 측정(06.19)
- Adafruit_DHT 모듈 사용
- VCC-5v / GND-GND / DATA-GPIO 연결

## 카메라 모듈로 사진, 동영상 촬영(06.20)
- PiCamera 모듈 사용
- .capture / .start_recording

> LED 켜기
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/4ecca2e1-a5e6-47e0-8b33-2d3f8ff8b52b"/>

> 스위치
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/083a0c25-f94a-447f-9058-7998667e6243"/>

> 온습도
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/e919baae-1be2-4c43-a0fe-ba2997a9dc58"/>

> 동영상(카메라)
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/b2269571-27de-4cec-ab94-c4ab68821a6c"/>

> 사진(카메라)
<img width="200" height="100" src="https://github.com/HyeongChank/Raspberry_pi/assets/122770625/114b1aa8-c49f-45ab-9340-eeb5bd8a9e54"/>
