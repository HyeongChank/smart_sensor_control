import simpy
import random

class Product:
    def __init__(self, env, machine_A):
        self.env = env
        self.machine_A = machine_A

    def process(self):
        while True:
            yield self.env.process(self.machine_A.run())
            
class MachineA:
    def __init__(self, env, conveyor1, machine_B, machine_C):
        self.env = env
        self.conveyor1 = conveyor1
        self.machine_B = machine_B
        self.machine_C = machine_C

    def run(self):
        weight = random.choice(['normal']*9 + ['unnormal'])
        yield self.env.timeout(2)
        yield self.conveyor1.put(weight)
        print(f'At time {self.env.now}, MachineA produced a product of weight {weight}')

        if weight == 'normal':
            yield self.env.process(self.machine_B.run())
        else:
            yield self.env.process(self.machine_C.run())

class MachineB:
    def __init__(self, env, conveyor2):
        self.env = env
        self.conveyor2 = conveyor2

    def run(self):
        weight = yield self.conveyor2.get()
        yield self.env.timeout(2)
        print(f'At time {self.env.now}, MachineB processed a product of weight {weight}')

class MachineC:
    def __init__(self, env, conveyor3):
        self.env = env
        self.conveyor3 = conveyor3

    def run(self):
        weight = yield self.conveyor3.get()
        yield self.env.timeout(2)
        print(f'At time {self.env.now}, MachineC processed a product of weight {weight}')

env = simpy.Environment()

conveyor1 = simpy.Store(env, capacity=1)
conveyor2 = simpy.Store(env, capacity=1)
conveyor3 = simpy.Store(env, capacity=1)
machine_A = MachineA(env, conveyor1, machine_B, machine_C)
machine_B = MachineB(env, conveyor2)
machine_C = MachineC(env, conveyor3)

product = Product(env, machine_A)

env.process(product.process())
env.run(until=100)
