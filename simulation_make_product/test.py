
import random
import csv
import simpy
# from picamera import PiCamera
# import RPi.GPIO as GPIO
# from time import sleep
# import time   


product_a_count = 0
product_b_count = 0
product_c_count = 0
complete_product_count = 0
unnormal_product_head_count = 0
unnormal_product_body_count = 0
unnormal_product_foot_count = 0
machineA_complete_list = []

class Product:
    def __init__(self, env, name, conveyor1, conveyor2, conveyor3,
                  conveyor1_1, conveyor2_1, conveyor3_1, weight):
        self.env = env
        self.name = name
        self.conveyor1 = conveyor1
        self.conveyor2 = conveyor2
        self.conveyor3 = conveyor3
        self.conveyor1_1 = conveyor1_1
        self.conveyor2_1 = conveyor2_1
        self.conveyor3_1 = conveyor3_1
        self.weight = weight

        
        if name =='head':
            self.action = env.process(self.machine_A1())
        elif name =='body':
            self.action = env.process(self.machine_A2())
        elif name =='foot':
            self.action = env.process(self.machine_A3())
    
    def machine_A1(self):
        global product_a_count
       
        yield env.timeout(2)
        machineA_completetime = env.now
        product_a_count += 1
        yield self.conveyor1.put('제품 %s' % (self.name + str(product_a_count)))
        print('시간 %d: 머신 A1가 제품 %s를 완성하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_a_count), self.conveyor1))
        self.env.process(self.machine_A1_1( machineA_completetime))

    def machine_A2(self):
        global product_b_count
      
        yield env.timeout(4)
        machineA_completetime = env.now
        product_b_count += 1
        yield self.conveyor2.put('제품 %s' % (self.name + str(product_b_count)))
        print('시간 %d: 머신 A2가 제품 %s를 완성하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_b_count), self.conveyor2))
        self.env.process(self.machine_A2_1(machineA_completetime))

    def machine_A3(self):
        global product_c_count
     
        yield env.timeout(10)
        machineA_completetime = env.now
        product_c_count += 1
        yield self.conveyor3.put('제품 %s' % (self.name + str(product_c_count)))
        print('시간 %d: 머신 A3가 제품 %s를 완성하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_c_count), self.conveyor3))
        self.env.process(self.machine_A3_1(machineA_completetime))


    
    def machine_A1_1(self, machineA_completetime):
        global product_a_count
        
        yield env.timeout(2)
        machineA_1_completetime = env.now
        yield self.conveyor1_1.put('제품 %s' % (self.name + str(product_a_count)))
        print('시간 %d: 머신 A1_1가 제품 %s를 가공하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_a_count), self.conveyor1_1))
        print(self.weight)
        if self.weight == 'normal':
            self.env.process(self.machine_B(machineA_completetime, machineA_1_completetime))
        
        elif self.weight == 'unnormal':
            print('이상')
            self.env.process(self.machine_C())
        
            


    def machine_A2_1(self, machineA_completetime):
        global product_b_count
       
        yield env.timeout(2)
        machineA_1_completetime = env.now
        product_b_count += 1
        yield self.conveyor2_1.put('제품 %s' % (self.name + str(product_b_count)))
        print('시간 %d: 머신 A2_1가 제품 %s를 가공하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_b_count), self.conveyor2_1))
        print(self.weight)
        if self.weight == 'normal':
            self.env.process(self.machine_B(machineA_completetime, machineA_1_completetime))
    
        else:
            print('이상')
            self.env.process(self.machine_C())
       
                


    def machine_A3_1(self, machineA_completetime):
        global product_c_count
      
        yield env.timeout(2)
        machineA_1_completetime = env.now
        product_c_count += 1
        yield self.conveyor3_1.put('제품 %s' % (self.name + str(product_c_count)))
        print('시간 %d: 머신 A3_1가 제품 %s를 가공하고 %s 컨베이어에 넣음' % (env.now, self.name + str(product_c_count), self.conveyor3_1))
        print(self.weight)
        if self.weight == 'normal':
            self.env.process(self.machine_B(machineA_completetime, machineA_1_completetime))
        
        else:
            print('이상')
            self.env.process(self.machine_C())
      
            



    def machine_B(self, machineA_completetime, machineA_1_completetime):
        global complete_product_count
        while True:
            item1 = yield self.conveyor1.get()
            item2 = yield self.conveyor2.get()
            item3 = yield self.conveyor3.get()
            yield env.timeout(3)
            print('시간 %d: 머신 B가 %s와 %s와 %s를 사용하여 완성 제품을 만듦' % (env.now, item1, item2, item3))
            result_data = [self.name, self.conveyor1, self.conveyor2, self.conveyor3, machineA_completetime, self.conveyor1_1, self.conveyor2_1, self.conveyor3_1, machineA_1_completetime]
            machineA_complete_list.append(result_data)
            complete_product_count += 1
            

    def machine_C(self):
        global unnormal_product_head_count
        global unnormal_product_body_count
        global unnormal_product_foot_count
        while True:
            item1 = yield self.conveyor1.get()
            yield env.timeout(3)
            unnormal_product_head_count += 1
        # if item1.name == 'head':
        #     unnormal_product_head_count += 1
        #     self.action = env.process(self.machine_A1())
        # elif self.name == 'body':
        #     unnormal_product_body_count += 1
        #     self.action = env.process(self.machine_A2())
        # else:
        #     unnormal_product_foot_count +=1
        #     self.action = env.process(self.machine_A3())
            
            print('시간 %d 불량 의심 제품 %s 별도 분리' % (env.now, self.name))
           # yield를 하지 않으면 generate None 오류 나옴
        


weight_list = ['unnormal'] * 4 + ['normal'] * 4
print(weight_list)
env = simpy.Environment()
temporature = 'normal'
stop_production = False

def monitor_temperature():
    global stop_production
    while True:
        # 온도 감지 코드(10번 이상 이상 시 작동)
        if temporature == "unnormal":
            stop_production = True
            env.stop()
            factory_enviroment_unnormal()
        yield env.timeout(10)  # 모니터 간격
    # 연락, cctv 작동 등
env.process(monitor_temperature())

def factory_enviroment_unnormal():
    pass

def monitor_vibration():
    pass



conveyor1 = simpy.Store(env, capacity=1)
conveyor2 = simpy.Store(env, capacity=1)
conveyor3 = simpy.Store(env, capacity=1)
conveyor1_1 = simpy.Store(env, capacity=1)
conveyor2_1 = simpy.Store(env, capacity=1)
conveyor3_1 = simpy.Store(env, capacity=1)

for i in range(1000):
    Product(env, 'head', conveyor1, conveyor2, conveyor3,
            conveyor1_1, conveyor2_1, conveyor3_1, random.choice(weight_list))
for i in range(1000):
    Product(env, 'body', conveyor1, conveyor2, conveyor3,
            conveyor1_1, conveyor2_1, conveyor3_1, random.choice(weight_list))
for i in range(1000):
    Product(env, 'foot', conveyor1, conveyor2, conveyor3,
            conveyor1_1, conveyor2_1, conveyor3_1, random.choice(weight_list))

env.run(until=500)

print('완성 개수:', complete_product_count)
print('불량의심(head) 개수:', unnormal_product_head_count)
print('불량의심(body) 개수:', unnormal_product_body_count)
print('불량의심(foot) 개수:', unnormal_product_foot_count)


csv_filename = "data/smartfactory.csv"
def save_results_to_csv(filename, machineA_complete_list):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'conveyor1', 'conveyor2', 'conveyor3', 'AcompleteTime', 'conveyor1_1', 'conveyor2_1', 'conveyor3_1', 'A_1completeTime'])
        for product in machineA_complete_list:
            writer.writerow([product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8]])
        print(len(machineA_complete_list))
    print("저장완료")
    print("machinea1", product_a_count)
    print("machinea2", product_b_count)
    print("machinea3", product_c_count)

save_results_to_csv(csv_filename, machineA_complete_list)
