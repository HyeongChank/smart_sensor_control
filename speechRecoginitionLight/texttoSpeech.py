import pyttsx3

def text_to_speech(text):
    # Text-to-speech 엔진 초기화
    engine = pyttsx3.init()

    # 말하는 속도 설정 (선택 사항)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)

    # 텍스트를 음성으로 변환하여 말하기
    engine.say(text)

    # 대기 시간을 주어 음성이 재생되도록 함
    engine.runAndWait()

if __name__ == "__main__":
    text_to_speech("안녕하세요. 파이썬으로 텍스트를 음성으로 변환하는 예제 코드입니다.")
