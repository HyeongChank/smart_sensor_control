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

class MachineA1:
    def __init__(self, env, conveyor_b, conveyor_c):
        self.env = env
        self.conveyor_b = conveyor_b
        self.conveyor_c = conveyor_c

    def run(self):
        global normal_head
        global unnormal_head
        while True:
            yield self.env.timeout(2)  # takes 2 time units
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            if product == 'normal':
                yield self.conveyor_b.put('head' + product)
                # yield self.env.timeout(1)
                normal_head += 1
            else:
                yield self.conveyor_c.put('head' + product)
                # yield self.env.timeout(1)
                unnormal_head += 1
            print(f'Machine A1 produced a {product} at time {self.env.now}')

class MachineA2:
    def __init__(self, env, conveyor_b, conveyor_c):
        self.env = env
        self.conveyor_b = conveyor_b
        self.conveyor_c = conveyor_c

    def run(self):
        global normal_body
        global unnormal_body
        while True:
            yield self.env.timeout(2)  # takes 3 time units
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            if product == 'normal':
                yield self.conveyor_b.put('body' + product)
                #yield self.env.timeout(1)
                normal_body += 1
            else:
                yield self.conveyor_c.put('body' + product)
                #yield self.env.timeout(1)
                unnormal_body += 1
            print(f'Machine A2 produced a {product} at time {self.env.now}')

class MachineA3:
    def __init__(self, env, conveyor_b, conveyor_c):
        self.env = env
        self.conveyor_b = conveyor_b
        self.conveyor_c = conveyor_c

    def run(self):
        global normal_foot
        global unnormal_foot
        while True:
            yield self.env.timeout(2)  # takes 4 time units
            product_weight = ['normal'] * 95 + ['unnormal'] * 5
            product = random.choice(product_weight)
            if product == 'normal':
                yield self.conveyor_b.put('foot' + product)
                #yield self.env.timeout(1)
                normal_foot += 1
            else:
                yield self.conveyor_c.put('foot' + product)
                #yield self.env.timeout(1)
                unnormal_foot += 1
            print(f'Machine A3 produced a {product} at time {self.env.now}')

class MachineB:
    def __init__(self, env, conveyor_a1, conveyor_a2, conveyor_a3):
        self.env = env
        self.conveyor_a1 = conveyor_a1
        self.conveyor_a2 = conveyor_a2
        self.conveyor_a3 = conveyor_a3

    def run(self):
        global product_count
        while True:
            product_a1 = yield self.conveyor_a1.get()
            product_a2 = yield self.conveyor_a2.get()
            product_a3 = yield self.conveyor_a3.get()

            products = {product_a1, product_a2, product_a3}
            if 'headnormal' in products and 'bodynormal' in products and 'footnormal' in products:
                yield self.env.timeout(1)
                product_count += 1
                print(f'Machine B processed products at time {self.env.now}')
            else:
                pass

class MachineC:
    def __init__(self, env, conveyor_a1, conveyor_a2, conveyor_a3):
        self.env = env
        self.conveyor_a1 = conveyor_a1
        self.conveyor_a2 = conveyor_a2
        self.conveyor_a3 = conveyor_a3

    def run(self):
        global unnormal_total
        while True:
            product_a1 = yield self.conveyor_a1.get()
            product_a2 = yield self.conveyor_a2.get()
            product_a3 = yield self.conveyor_a3.get()

            unnormal_total += 1

            print(f'Machine C processed at time {self.env.now}')

env = simpy.Environment()
conveyor_b = simpy.Store(env, capacity=100)
conveyor_c = simpy.Store(env, capacity=100)
machine_A1 = MachineA1(env, conveyor_b, conveyor_c)
machine_A2 = MachineA2(env, conveyor_b, conveyor_c)
machine_A3 = MachineA3(env, conveyor_b, conveyor_c)
machine_B = MachineB(env, conveyor_b, conveyor_b, conveyor_b)
machine_C = MachineC(env, conveyor_c, conveyor_c, conveyor_c)

env.process(machine_A1.run())
env.process(machine_A2.run())
env.process(machine_A3.run())
env.process(machine_B.run())
env.process(machine_C.run())
env.run(until=200)

print('product_count', product_count)
print('normal_head', normal_head)
print('normal_body', normal_body)
print('normal_foot', normal_foot)

print(unnormal_head)
print(unnormal_body)
print(unnormal_foot)
