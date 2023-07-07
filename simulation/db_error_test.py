# import RPi.GPIO as GPIO
import sqlite3
import time
import simpy
import threading
import random
from flask import Flask, request
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread, Event
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config.update(
#     CELERY_BROKER_URL='amqp://localhost//',
#     CELERY_RESULT_BACKEND='rpc://'
# )
thread = Thread()
thread_stop_event = Event()


product_count = 0
unnormal_total = 0
produce_head =0
produce_body =0
produce_foot =0
normal_head = 0
normal_body = 0
normal_foot = 0
unnormal_head = 0
unnormal_body = 0
unnormal_foot = 0

class WebSocketThread(Thread):
    def __init__(self, sid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sid = sid
        self.env = simpy.rt.RealtimeEnvironment()
        self.conveyor_a1_1 = simpy.Store(self.env, capacity=100)
        self.conveyor_a1tob = simpy.Store(self.env, capacity=100)
        self.conveyor_a1toc = simpy.Store(self.env, capacity=100)
        self.conveyor_a2_1 = simpy.Store(self.env, capacity=100)
        self.conveyor_a2tob = simpy.Store(self.env, capacity=100)
        self.conveyor_a2toc = simpy.Store(self.env, capacity=100)
        self.conveyor_a3_1 = simpy.Store(self.env, capacity=100)
        self.conveyor_a3tob = simpy.Store(self.env, capacity=100)
        self.conveyor_a3toc = simpy.Store(self.env, capacity=100)
        self.stop_simulation = False
        self.machine_A1 = MachineA1(self.env, self.conveyor_a1_1, self, self.emit_data)
        self.machine_A1_1 = MachineA1_1(self.env, self.conveyor_a1_1, self.conveyor_a1tob, self.conveyor_a1toc, self.emit_data)
        self.env.process(self.machine_A1.run())
        self.env.process(self.machine_A1_1.run())
        self.machine_A2 = MachineA2(self.env, self.conveyor_a2_1, self, self.emit_data)
        self.machine_A2_1 = MachineA2_1(self.env, self.conveyor_a2_1, self.conveyor_a2tob, self.conveyor_a2toc, self.emit_data)
        self.env.process(self.machine_A2.run())
        self.env.process(self.machine_A2_1.run())
        self.machine_A3 = MachineA3(self.env, self.conveyor_a3_1, self, self.emit_data)
        self.machine_A3_1 = MachineA3_1(self.env, self.conveyor_a3_1, self.conveyor_a3tob, self.conveyor_a3toc, self.emit_data)
        self.env.process(self.machine_A3.run())
        self.env.process(self.machine_A3_1.run())
        self.machine_B = MachineB(self.env, self.conveyor_a1tob, self.conveyor_a2tob, self.conveyor_a3tob, self.emit_data)
        self.machine_C = MachineC(self.env, self.conveyor_a1toc, self.conveyor_a2toc, self.conveyor_a3toc, self.emit_data)
        self.env.process(self.machine_B.run())
        self.env.process(self.machine_C.run())
        ts = threading.Thread(target=self.stop_button)
        ts.start()
        
        
        
    def emit_data(self, event, data):
        socketio.emit(event, data, room=self.sid, namespace='/test')

    def run(self):
        self.env.run(until=50)
        

    def stop_button(self):
        
        while True:
            inp_stop = input()
        
            if inp_stop.lower() =='s':
                self.stop_simulation = True
                stop_point = self.env.now
                print(stop_point)
                print(f'stop_producing at {stop_point}')
                db_conn = sqlite3.connect('smartfactory.db')
                db_cursor = db_conn.cursor()
                db_cursor.execute("create table if not exists sf (subject text, content_time REAL)")        
                db_cursor.execute("INSERT INTO sf VALUES (?, ?)", ('newstop', stop_point))
                db_conn.commit()
                db_conn.close()
                
                

            elif inp_stop.lower() == 're':
                self.stop_simulation= False
                restart_point = self.env.now
                print(restart_point)
                print(f'restart_time at {restart_point}')
                db_conn = sqlite3.connect('smartfactory.db')
                db_cursor = db_conn.cursor()
                db_cursor.execute("INSERT INTO sf VALUES (?, ?)", ('newrestart', restart_point))
                db_conn.commit()
                db_conn.close()
                
            elif inp_stop.lower() =='log':
                print("exit_close")
                db_conn = sqlite3.connect('smartfactory.db')
                db_cursor = db_conn.cursor()
                db_cursor.execute('select * from sf')
                for row in db_cursor:
                    print(row)
                db_conn.close()
                
                
                
class MachineA1:
    def __init__(self, env, conveyor_a1_1, web_socket_thread, emit_data):
        self.env = env
        self.conveyor_a1_1 = conveyor_a1_1
        self.emit_data = emit_data
        self.web_socket_thread = web_socket_thread
        
        self.time_thread = threading.Thread(target=self.time_tracker)
        self.time_thread.start()
    def time_tracker(self):
        while True:
            self.emit_data('process_time', {'Time': self.env.now})
            time.sleep(1)
        
    def run(self):
        global produce_head
        while True:
            yield self.env.timeout(5)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            produce_head +=1
            self.emit_data('machineA1_count', {'count': produce_head})
            
            self.emit_data('problem', {'problem': 'working'})
            if self.web_socket_thread.stop_simulation:
                while self.web_socket_thread.stop_simulation:
                    yield self.env.timeout(1)
                    print('machineA stop')
                    self.emit_data('problem', {'problem': 'problem occurency'})
                print('machineA_restart')

            yield self.conveyor_a1_1.put(product)
            print(f'Machine A1 produced a {product} at time {self.env.now}')

class MachineA1_1:
    def __init__(self, env, conveyor_a1_1, conveyor_a1tob, conveyor_a1toc, emit_data):
        self.env = env
        self.conveyor_a1_1 = conveyor_a1_1
        self.conveyor_a1tob = conveyor_a1tob
        self.conveyor_a1toc = conveyor_a1toc
        self.emit_data = emit_data
        
    def run(self):
        global normal_head
        global unnormal_head
        while True:
            yield self.env.timeout(1)
            product_a1 = yield self.conveyor_a1_1.get()
            
            yield self.env.timeout(3)
            if product_a1 == 'normal':
                normal_head += 1
                
                print(normal_head)
                yield self.conveyor_a1tob.put('head' + product_a1)
                yield self.env.timeout(2)
                
            else:
                unnormal_head += 1
                self.emit_data('A1_unnormal_count', {'unnormal' : unnormal_head})
                yield self.conveyor_a1toc.put('head' + product_a1)
                yield self.env.timeout(2)
            
class MachineA2:
    def __init__(self, env, conveyor_a2_1, web_socket_thread, emit_data):
        self.env = env
        self.conveyor_a2_1 = conveyor_a2_1
        self.emit_data = emit_data
        self.web_socket_thread = web_socket_thread

    def run(self):
        global produce_body
        while True:
            yield self.env.timeout(4)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            produce_body +=1
            self.emit_data('machineA2_count', {'count': produce_body})
            if self.web_socket_thread.stop_simulation:
                while self.web_socket_thread.stop_simulation:
                    yield self.env.timeout(1)
                    print('machineA2 stop')
                
                print('machineA2_restart')            
            yield self.conveyor_a2_1.put(product)
            print(f'Machine A2 produced a {product} at time {self.env.now}')

class MachineA2_1:
    def __init__(self, env, conveyor_a2_1, conveyor_a2tob, conveyor_a2toc, emit_data):
        self.env = env
        self.conveyor_a2_1 = conveyor_a2_1
        self.conveyor_a2tob = conveyor_a2tob
        self.conveyor_a2toc = conveyor_a2toc
        self.emit_data = emit_data

    def run(self):
        global normal_body
        global unnormal_body
        while True:
            yield self.env.timeout(1)
            product_a2 = yield self.conveyor_a2_1.get()
            yield self.env.timeout(1)
            if product_a2 == 'normal':
                normal_body += 1
                # self.emit_data('machineA2_status', {'status': product_a2})
                # self.emit_data('machineA2_part', {'part': 'body'})
                # self.emit_data('machineA2_count', {'count': normal_body})
                yield self.conveyor_a2tob.put('body' + product_a2)
                yield self.env.timeout(2)
                
            else:
                unnormal_body += 1
                self.emit_data('A2_unnormal_count', {'unnormal' : unnormal_body})
                yield self.conveyor_a2toc.put('body' + product_a2)
                yield self.env.timeout(2)            
            
class MachineA3:
    def __init__(self, env, conveyor_a3_1, web_socket_thread, emit_data):
        self.env = env
        self.conveyor_a3_1 = conveyor_a3_1
        self.emit_data = emit_data
        self.web_socket_thread = web_socket_thread

    def run(self):
        global produce_foot
        while True:
            yield self.env.timeout(3)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            produce_foot +=1
            self.emit_data('machineA3_count', {'count': produce_foot})
            if self.web_socket_thread.stop_simulation:
                while self.web_socket_thread.stop_simulation:
                    yield self.env.timeout(1)
                    print('machineA3 stop')
                
                print('machineA3_restart')            
            yield self.conveyor_a3_1.put(product)
            print(f'Machine A3 produced a {product} at time {self.env.now}')

class MachineA3_1:
    def __init__(self, env, conveyor_a3_1, conveyor_a3tob, conveyor_a3toc, emit_data):
        self.env = env
        self.conveyor_a3_1 = conveyor_a3_1
        self.conveyor_a3tob = conveyor_a3tob
        self.conveyor_a3toc = conveyor_a3toc
        self.emit_data = emit_data

    def run(self):
        global normal_foot
        global unnormal_foot
        while True:
            yield self.env.timeout(4)
            product_a3 = yield self.conveyor_a3_1.get()
            yield self.env.timeout(1)
            if product_a3 == 'normal':
                normal_foot += 1
                # self.emit_data('machineA3_status', {'status': product_a3})
                # self.emit_data('machineA3_part', {'part': 'foot'})
                # self.emit_data('machineA3_count', {'count': normal_foot})
                yield self.conveyor_a3tob.put('foot' + product_a3)
                print('foot a3_1')
                yield self.env.timeout(2)
                
            else:
                unnormal_foot += 1
                self.emit_data('A3_unnormal_count', {'unnormal' : unnormal_foot})
                yield self.conveyor_a3toc.put('foot' + product_a3)
                yield self.env.timeout(2)

class MachineB:
    def __init__(self, env, conveyor_a1tob, conveyor_a2tob, conveyor_a3tob, emit_data):
        self.env = env
        self.conveyor_a1tob = conveyor_a1tob
        self.conveyor_a2tob = conveyor_a2tob
        self.conveyor_a3tob = conveyor_a3tob
        self.emit_data = emit_data

    def run(self):
        global product_count
        while True:

            product_a1 = yield self.conveyor_a1tob.get()
            print(product_a1)
            product_a2 = yield self.conveyor_a2tob.get()
            print(product_a2)
            product_a3 = yield self.conveyor_a3tob.get()
            print(product_a3)
            products = {product_a1, product_a2, product_a3}
            print(products)
            if 'headnormal' in products and 'bodynormal' in products and 'footnormal' in products:
                yield self.env.timeout(3)
                product_count += 1
                self.emit_data('completed_product', {'completed_product': product_count})

                print(f'Machine B processed products at time {self.env.now}*********************')
            else:
                pass

class MachineC:
    def __init__(self, env, conveyor_a1toc, conveyor_a2toc, conveyor_a3toc, emit_data):
        self.env = env
        self.conveyor_a1toc = conveyor_a1toc
        self.conveyor_a2toc = conveyor_a2toc
        self.conveyor_a3toc = conveyor_a3toc
        self.emit_data = emit_data

    def run(self):

        global unnormal_head
        global unnormal_body
        global unnormal_foot
        while True:
            # yield 안하니까 웹소켓이랑 연결 안되는 오류 났었음
            yield self.env.timeout(5)
            unnormal_total = unnormal_head + unnormal_body + unnormal_foot
            self.emit_data('unnormal_total', {'unnormal_total': unnormal_total})
            
            
            
            
@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    thread = WebSocketThread(request.sid)
    thread.start()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
