import simpy
import random
# from picamera import PiCamera
# import RPi.GPIO as GPIO
# from time import sleep
# import time   


# 생산품 3개
product_a_count =0
product_b_count =0
product_c_count =0

class Product:
    def __init__(self, env, name, conveyor):
        self.env = env
        self.name = name
        self.conveyor = conveyor
        if name =='head1':
            self.action = env.process(self.machine_A1())
        elif name =='body2':
            self.action = env.process(self.machine_A2())
    # def product_generate(self):



    def machine_A1(self):
        global product_a_count
        while True:
            yield env.timeout(2)  # 머신 A에서 제품을 제작하는 데 2시간 소요
            product_a_count +=1
            yield self.conveyor.put('제품 %s' % self.name + str(product_a_count))

            print('시간 %d: 머신 A1가 제품 %s를 완성하고 컨베이어에 넣음' % (env.now, self.name + str(product_a_count)))
            self.env.process(self.machine_B())

    def machine_A2(self):
        global product_b_count
        while True:
            yield env.timeout(4)  # 머신 A에서 제품을 제작하는 데 2시간 소요
            product_b_count +=1
            yield self.conveyor.put('제품 %s' % self.name + str(product_b_count))

            print('시간 %d: 머신 A1가 제품 %s를 완성하고 컨베이어에 넣음' % (env.now, self.name + str(product_b_count)))
            self.env.process(self.machine_B())
 
    def machine_B(self):
        while True:
            item1 = yield self.conveyor.get()
            item2 = yield self.conveyor.get()
            yield env.timeout(3)  # 머신 B에서 제품을 완성하는 데 3시간 소요
            print('시간 %d: 머신 B가 %s를 완성' % (env.now, item1))


env = simpy.Environment()
conveyor1 = simpy.Store(env, capacity=1)
conveyor2 = simpy.Store(env, capacity=1)
# conveyor3 = simpy.Store(env, capacity=1)

Product(env,'head' + str(1), conveyor1)
Product(env,'body' + str(2), conveyor2)
    # Product(env,'tail' + str(i+1), conveyor3)

env.run(until=150)  # 15시간 동안 시뮬레이션 실행
