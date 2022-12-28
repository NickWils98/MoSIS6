from coupled_devs import port_system
import random
import numpy as np
from pypdevs.simulator import Simulator



if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)

    # Set up the system and run
    system = port_system.PortSystem()
    sim =Simulator(system)
    sim.setTerminationTime(74.709856)
    sim.setClassicDEVS()
    sim.simulate()
