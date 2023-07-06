# import RPi.GPIO as GPIO
import pandas as pd
import time
import simpy
import threading
import random
from flask import Flask, request
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread, Event


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

thread = Thread()
thread_stop_event = Event()


product_count = 0
unnormal_total = 0
normal_head = 0
normal_body = 0
normal_foot = 0
unnormal_head = 0
unnormal_body = 0
unnormal_foot = 0
stop_simulation = False

class WebSocketThread(Thread):
    def __init__(self, sid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sid = sid
        self.env = simpy.rt.RealtimeEnvironment()
        self.conveyor_a1_1 = simpy.Store(self.env, capacity=100)
        self.machine_A1 = MachineA1(self.env, self.conveyor_a1_1, self.emit_data)
        self.env.process(self.machine_A1.run())

    def emit_data(self, event, data):
        socketio.emit(event, data, room=self.sid, namespace='/test')

    def run(self):
        self.env.run(until=200)


class MachineA1:
    def __init__(self, env, conveyor_a1_1, emit_data):
        self.env = env
        self.conveyor_a1_1 = conveyor_a1_1
        self.emit_data = emit_data

    def run(self):
        while True:
            yield self.env.timeout(2)
            product_weight = ['normal'] * 5 + ['unnormal'] * 5
            product = random.choice(product_weight)
            self.emit_data('data1', {'product': product})
            self.emit_data('data2', {'product': product})

            if stop_simulation:
                while stop_simulation:
                    yield self.env.timeout(1)
                    print('machineA stop')
                print('machineA_restart')

            yield self.conveyor_a1_1.put(product)
            print(f'Machine A1 produced a {product} at time {self.env.now}')


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    thread = WebSocketThread(request.sid)
    thread.start()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
