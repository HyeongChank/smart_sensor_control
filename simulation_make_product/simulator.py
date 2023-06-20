import simpy

def machine_A(env, name, conveyor):
    while True:
        yield env.timeout(2)  # 머신 A에서 제품을 제작하는 데 2시간 소요
        yield conveyor.put('제품 %s' % name)
        print('시간 %d: 머신 A가 제품 %s를 완성하고 컨베이어에 넣음' % (env.now, name))

def machine_B(env, conveyor):
    while True:
        item = yield conveyor.get()
        yield env.timeout(3)  # 머신 B에서 제품을 완성하는 데 3시간 소요
        print('시간 %d: 머신 B가 %s를 완성' % (env.now, item))

env = simpy.Environment()
conveyor = simpy.Store(env, capacity=2)  # 컨베이어의 용량은 2
env.process(machine_A(env, 'A', conveyor))
env.process(machine_A(env, 'B', conveyor))
env.process(machine_B(env, conveyor))

env.run(until=15)  # 15시간 동안 시뮬레이션 실행
