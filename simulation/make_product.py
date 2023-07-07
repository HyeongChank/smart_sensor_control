import simpy
import random


product_count = 0
unnormal_total = 0
normal_head = 0
normal_body = 0
normal_foot = 0
unnormal_head = 0
unnormal_body = 0
unnormal_foot = 0

# 소요시간
    # a1-2, convey(selection)-3, a1_1-3, a1tob-2 a1toc -2
    # a2-3, convey(selection)-4, a2_1-1, a1tob-2 a1toc -2
    # a3-4, convey(selection)-2, a2_1-2, a1tob-2 a1toc -2

class MachineA1:
    def __init__(self, env, conveyor_a1_1):
        self.env = env
        self.conveyor_a1_1 = conveyor_a1_1

    def run(self):
        while True:
            yield self.env.timeout(2)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            yield self.conveyor_a1_1.put(product)
            print(f'Machine A1 produced a {product} at time {self.env.now}')

class MachineA1_1:
    def __init__(self, env, conveyor_a1_1, conveyor_a1tob, conveyor_a1toc):
        self.env = env
        self.conveyor_a1_1 = conveyor_a1_1
        self.conveyor_a1tob = conveyor_a1tob
        self.conveyor_a1toc = conveyor_a1toc

    def run(self):
        global normal_head
        global unnormal_head
        while True:
            yield self.env.timeout(3)
            product_a1 = yield self.conveyor_a1_1.get()
            
            yield self.env.timeout(3)
            if product_a1 == 'normal':
                normal_head += 1
                yield self.conveyor_a1tob.put('head' + product_a1)
                yield self.env.timeout(2)
                
            else:
                unnormal_head += 1
                yield self.conveyor_a1toc.put('head' + product_a1)
                yield self.env.timeout(2)
                
            print(f'Machine A1 processed a {product_a1} at time {self.env.now}')

class MachineA2:
    def __init__(self, env, conveyor_a2_1):
        self.env = env
        self.conveyor_a2_1 = conveyor_a2_1

    def run(self):
        while True:
            yield self.env.timeout(3)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            yield self.conveyor_a2_1.put(product)
            print(f'Machine A2 produced a {product} at time {self.env.now}')

class MachineA2_1:
    def __init__(self, env, conveyor_a2_1, conveyor_a2tob, conveyor_a2toc):
        self.env = env
        self.conveyor_a2_1 = conveyor_a2_1
        self.conveyor_a2tob = conveyor_a2tob
        self.conveyor_a2toc = conveyor_a2toc

    def run(self):
        global normal_body
        global unnormal_body
        while True:
            yield self.env.timeout(4)
            product_a2 = yield self.conveyor_a2_1.get()
            yield self.env.timeout(1)
            if product_a2 == 'normal':
                normal_body += 1
                yield self.conveyor_a2tob.put('body' + product_a2)
                print('a2 normal to b')
                yield self.env.timeout(2)
                
            else:
                unnormal_body += 1
                yield self.conveyor_a2toc.put('body' + product_a2)
                yield self.env.timeout(2)
                
            print(f'Machine A2 produced a {product_a2} at time {self.env.now}')

class MachineA3:
    def __init__(self, env, conveyor_a3_1):
        self.env = env
        self.conveyor_a3_1 = conveyor_a3_1

    def run(self):
        while True:
            yield self.env.timeout(4)
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            yield self.conveyor_a3_1.put(product)
            print(f'Machine A2 produced a {product} at time {self.env.now}')

class MachineA3_1:
    def __init__(self, env, conveyor_a3_1, conveyor_a3tob, conveyor_a3toc):
        self.env = env
        self.conveyor_a3_1 = conveyor_a3_1
        self.conveyor_a3tob = conveyor_a3tob
        self.conveyor_a3toc = conveyor_a3toc

    def run(self):
        global normal_foot
        global unnormal_foot
        while True:
            yield self.env.timeout(2)
            product_a3 = yield self.conveyor_a3_1.get()
            yield self.env.timeout(2)
            if product_a3 == 'normal':
                normal_foot += 1
                yield self.conveyor_a3tob.put('foot' + product_a3)
                print('a3 normal to b')
                yield self.env.timeout(2)
                
            else:
                unnormal_foot += 1
                yield self.conveyor_a3toc.put('foot' + product_a3)
                yield self.env.timeout(2)
                
            print(f'Machine A3 produced a {product_a3} at time {self.env.now}')

class MachineB:
    def __init__(self, env, conveyor_a1tob, conveyor_a2tob, conveyor_a3tob):
        self.env = env
        self.conveyor_a1tob = conveyor_a1tob
        self.conveyor_a2tob = conveyor_a2tob
        self.conveyor_a3tob = conveyor_a3tob

    def run(self):
        global product_count
        while True:

            product_a1 = yield self.conveyor_a1tob.get()
            product_a2 = yield self.conveyor_a2tob.get()
            product_a3 = yield self.conveyor_a3tob.get()
            print('bget')
            products = {product_a1, product_a2, product_a3}
            if 'headnormal' in products and 'bodynormal' in products and 'footnormal' in products:
                yield self.env.timeout(1)
                product_count += 1
                print(f'Machine B processed products at time {self.env.now}*********************')
            else:
                pass

class MachineC:
    def __init__(self, env, conveyor_a1toc, conveyor_a2toc, conveyor_a3toc):
        self.env = env
        self.conveyor_a1toc = conveyor_a1toc
        self.conveyor_a2toc = conveyor_a2toc
        self.conveyor_a3toc = conveyor_a3toc

    def run(self):
        global unnormal_total
        while True:

            product_a1 = yield self.conveyor_a1toc.get()
            if product_a1:
                unnormal_total +=1
            product_a2 = yield self.conveyor_a2toc.get()
            if product_a2:
                unnormal_total +=1
            product_a3 = yield self.conveyor_a3toc.get()
            if product_a3:
                unnormal_total +=1

            print(f'Machine C processed at time {self.env.now}')

env = simpy.Environment()
conveyor_a1_1 = simpy.Store(env, capacity=100)
conveyor_a2_1 = simpy.Store(env, capacity=100)
conveyor_a3_1 = simpy.Store(env, capacity=100)
conveyor_a1tob = simpy.Store(env, capacity=100)
conveyor_a2tob = simpy.Store(env, capacity=100)
conveyor_a3tob = simpy.Store(env, capacity=100)
conveyor_a1toc = simpy.Store(env, capacity=100)
conveyor_a2toc = simpy.Store(env, capacity=100)
conveyor_a3toc = simpy.Store(env, capacity=100)

conveyor_b = simpy.Store(env, capacity=100)
conveyor_c = simpy.Store(env, capacity=100)

machine_A1 = MachineA1(env, conveyor_a1_1)
machine_A1_1 = MachineA1_1(env, conveyor_a1_1, conveyor_a1tob, conveyor_a1toc)
machine_A2 = MachineA2(env, conveyor_a2_1)
machine_A2_1 = MachineA2_1(env, conveyor_a2_1, conveyor_a2tob, conveyor_a2toc)
machine_A3 = MachineA3(env, conveyor_a3_1)
machine_A3_1 = MachineA3_1(env, conveyor_a3_1, conveyor_a3tob, conveyor_a3toc)

machine_B = MachineB(env, conveyor_a1tob, conveyor_a2tob, conveyor_a3tob)
machine_C = MachineC(env, conveyor_a1toc, conveyor_a2toc, conveyor_a3toc)

env.process(machine_A1.run())
env.process(machine_A2.run())
env.process(machine_A3.run())
env.process(machine_A1_1.run())
env.process(machine_A2_1.run())
env.process(machine_A3_1.run())
env.process(machine_B.run())
env.process(machine_C.run())
env.run(until=2000)

print('product_count', product_count)
print('normal_head', normal_head)
print('normal_body', normal_body)
print('normal_foot', normal_foot)

print('unnormal_head', unnormal_head)
print('unnormal_body', unnormal_body)
print('unnormal_foot', unnormal_foot)
print('unnormal_total', unnormal_head+unnormal_body+unnormal_foot)
print('마감 시간까지 machine_C에 도착한 unnormal_total', unnormal_total)

