import simpy
import random

class MachineA1:
    def __init__(self, env, conveyor):
        self.env = env
        self.conveyor = conveyor

    def run(self):
        while True:
            yield self.env.timeout(2)
            product = "A1_" + random.choice(['normal', 'unnormal'])
            yield self.conveyor.put(product)
            print(f'Machine A1 produced a {product} at time {self.env.now}')

class MachineA2:
    def __init__(self, env, conveyor):
        self.env = env
        self.conveyor = conveyor

    def run(self):
        while True:
            yield self.env.timeout(3)
            product = "A2_" + random.choice(['normal', 'unnormal'])
            yield self.conveyor.put(product)
            print(f'Machine A2 produced a {product} at time {self.env.now}')


class MachineA3:
    def __init__(self, env, conveyor):
        self.env = env
        self.conveyor = conveyor

    def run(self):
        while True:
            yield self.env.timeout(4)
            product = "A3_" + random.choice(['normal', 'unnormal'])
            yield self.conveyor.put(product)
            print(f'Machine A3 produced a {product} at time {self.env.now}')


class MachineB:
    def __init__(self, env, conveyor):
        self.env = env
        self.conveyor = conveyor

    def run(self):
        while True:
            yield self.env.timeout(1)
            product = yield self.conveyor.get()
            if 'normal' in product:
                print(f'Machine B processed a {product} at time {self.env.now}')

class MachineC:
    def __init__(self, env, conveyor):
        self.env = env
        self.conveyor = conveyor

    def run(self):
        while True:
            yield self.env.timeout(1)
            product = yield self.conveyor.get()
            if 'unnormal' in product:
                print(f'Machine C processed a {product} at time {self.env.now}')


env = simpy.Environment()

conveyor_a1 = simpy.Store(env, capacity=1)
conveyor_a2 = simpy.Store(env, capacity=1)
conveyor_a3 = simpy.Store(env, capacity=1)
conveyor_b = simpy.Store(env, capacity=1)
conveyor_c = simpy.Store(env, capacity=1)

machine_A1 = MachineA1(env, conveyor_a1)
machine_A2 = MachineA2(env, conveyor_a2)
machine_A3 = MachineA3(env, conveyor_a3)

machine_B = MachineB(env, conveyor_b)
machine_C = MachineC(env, conveyor_c)

def direct_product(env, conveyor, conveyor_b, conveyor_c):
    while True:
        product = yield conveyor.get()
        if 'normal' in product:
            yield conveyor_b.put(product)
        elif 'unnormal' in product:
            yield conveyor_c.put(product)

env.process(machine_A1.run())
env.process(machine_A2.run())
env.process(machine_A3.run())

env.process(direct_product(env, conveyor_a1, conveyor_b, conveyor_c))
env.process(direct_product(env, conveyor_a2, conveyor_b, conveyor_c))
env.process(direct_product(env, conveyor_a3, conveyor_b, conveyor_c))

env.process(machine_B.run())
env.process(machine_C.run())

env.run(until=100)
