import threading
import queue
import time

# 사용자 입력을 받는 함수
def get_user_input(input_prompt, q):
    while True:
        user_input = input(input_prompt)
        q.put(user_input)

# 메시지 큐 생성
message_queue = queue.Queue()

# 사용자 입력을 받는 스레드 생성
input_thread = threading.Thread(target=get_user_input, args=("Enter something: ", message_queue))
input_thread.start()

# 메인 프로세스는 별도로 계속 진행
while True:
    if not message_queue.empty():
        message = message_queue.get()
        print(f"You entered: {message}")
        if message == "stop":
            print("Stopping main process...")
            break
    print("Main process is running...")
    time.sleep(1)
