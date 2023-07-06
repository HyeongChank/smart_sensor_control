import streamlit as st
import simpy
import threading
import pandas as pd

# Global DataFrame to store production data
production_data = pd.DataFrame(columns=['time', 'machine', 'product', 'status'])

stop_simulation = False

class Machine:
    def __init__(self, env, name):
        self.env = env
        self.name = name

    def run(self):
        global stop_simulation
        while True:
            if stop_simulation:
                break
            product = 'product_A' if self.name == 'machine_A' else 'product_B'
            status = 'normal' if self.name == 'machine_A' else 'unnormal'
            production_data.loc[len(production_data)] = [self.env.now, self.name, product, status]
            yield self.env.timeout(1)

def run_simulation():
    env = simpy.rt.RealtimeEnvironment()
    machine_A = Machine(env, 'machine_A')
    machine_B = Machine(env, 'machine_B')
    env.process(machine_A.run())
    env.process(machine_B.run())
    env.run(until=20)

def stop_button():
    global stop_simulation
    inp_stop = input('Press "s" to stop: ')
    if inp_stop.lower() == 's':
        stop_simulation = True

# Run the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation)
simulation_thread.start()

# Streamlit app
def app():
    st.title('Simpy Simulation')

    if st.button('Stop simulation'):
        stop_button()

    # Display production data
    st.dataframe(production_data)

# Run the Streamlit app
if __name__ == "__main__":
    app()
