from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread, Event

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

thread = Thread()
thread_stop_event = Event()

class RealtimeDataThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RealtimeDataThread, self).__init__()

    def dataGenerator(self):
        while not thread_stop_event.isSet():
            data1 = random.randint(1, 100)
            data2 = random.randint(1, 100)
            socketio.emit('data1', {'data': data1}, namespace='/test')
            socketio.emit('data2', {'data': data2}, namespace='/test')
            time.sleep(self.delay)

    def run(self):
        self.dataGenerator()

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    global thread
    if not thread.is_alive():
        thread = RealtimeDataThread()
        thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
