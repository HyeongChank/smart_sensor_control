import random
import simpy

class MachineA:
    def __init__(self, env, conveyor1, conveyor1_1):
        self.env = env
        self.conveyor1 = conveyor1
        self.conveyor1_1 = conveyor1_1

    def run(self):
        while True:
            print('a')
            yield self.env.timeout(2)
            yield self.conveyor1.put('머신 A에서 생성한 제품')
            self.env.process(self.machine_A1())

    def machine_A1(self):
        while True:
            print('a_1')
            yield self.env.timeout(2)
            yield self.conveyor1_1.put('머신 A_1에서 가공한 제품')
            weight = self.check_weight()  # 무게 확인
            if weight == 'normal':
                print('normal')
                yield from self.machine_B()
            elif weight == 'unnormal':
                yield from self.machine_C()

    def check_weight(self):
        print('checkweight')
        # 무게 확인 로직 구현
        return 'normal'  # 또는 'unnormal'

    def machine_B(self):
        
        while True:
            print('b')
            item1 = yield self.conveyor1_1.get()
            yield self.env.timeout(3)
            print('머신 B에서 제품을 합쳐서 완성함:', item1)

    def machine_C(self):
        while True:
            item = yield self.conveyor1_1.get()
            yield self.env.timeout(3)
            print('머신 C로 분류된 제품:', item)


class Product:
    def __init__(self, env, weight):
        self.env = env
        self.weight = weight
        self.conveyor1 = simpy.Store(env, capacity=1)
        self.conveyor1_1 = simpy.Store(env, capacity=1)
        self.machine_A = MachineA(env, self.conveyor1, self.conveyor1_1)

    def run(self):
        print('product')
        self.env.process(self.machine_A.run())


weight_list = ["unnormal"] * 9
print(weight_list)
env = simpy.Environment()

product = Product(env, random.choice(weight_list))
product.run()

env.run(until=100)  # 원하는 시뮬레이션 시간까지 실행
