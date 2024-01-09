import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os

def gtts(text):
    tts = gTTS(text=text, lang='en-us', slow=False)  # lang은 언어, gender는 성별
    tts.save("output.mp3")  # 음성 파일을 저장
    os.system("start output.mp3")  # 음성 파일을 재생
    
def text_to_speech(speech):
    # # Text-to-speech 엔진 초기화
    # engine = pyttsx3.init()

    # # 말하는 속도 설정 (선택 사항)
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', rate - 50)
    
    

    # 텍스트를 음성으로 변환하여 말하기
    if 'hey' in speech:
        comment = 'hello, what can i for you?'
        gtts(comment)
        # engine.say('hello, what can i do for you?')
    elif 'weather' in speech:
        comment_weather = 'pass'
        gtts(comment_weather)
        # engine.say('pass')

    # 대기 시간을 주어 음성이 재생되도록 함
    # engine.runAndWait()
    
def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("마이크로부터 몇 초간 소리를 듣고 있습니다. 말씀하세요...")
        audio = recognizer.listen(source, timeout=5)

    try:
        print("음성을 텍스트로 변환 중...")
        text = recognizer.recognize_google(audio, language='en-US')
        # text = recognizer.recognize_google(audio, language='ko-KR')
        print(text)
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        text = "try again"
    except sr.RequestError as e:
        print(f"Google Web Speech API 요청에 실패했습니다. 에러: {e}")
        text = "try again"
    return text

def operate():
    
    flag = 'on'
    while flag == 'on':
        call = recognize_speech()
        
        print("인식된 텍스트:", call)
        if 'hey' in call:
            text_to_speech(call)
            command = recognize_speech()
            text_to_speech(command)
        if 'stop' in call:
            flag = 'off'





if __name__ == "__main__":
    operate()
