import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("마이크로부터 몇 초간 소리를 듣고 있습니다. 말씀하세요...")
        audio = recognizer.listen(source, timeout=5)

    try:
        print("음성을 텍스트로 변환 중...")
        text = recognizer.recognize_google(audio, language='en-US')
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("인식된 텍스트:", text)
        if '켜' in text:
            print('on the light')
        elif '꺼' in text:
            print('off the light')
            
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"Google Web Speech API 요청에 실패했습니다. 에러: {e}")

if __name__ == "__main__":
    recognize_speech()
