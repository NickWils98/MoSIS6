from coupled_devs import port_system
import random
import numpy as np
from pypdevs.simulator import Simulator



if __name__ == '__main__':
    values = []

    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)

    # Set up the system and run
    system = port_system.PortSystem()
    sim =Simulator(system)
    sim.setTerminationTime(100)
    sim.setClassicDEVS()
    sim.simulate()

    # Gather information for output
    stat1 = system.collector.state.stat1_info
    stat2 = system.collector.state.stat2_info
    stat3 = system.collector.state.stat3_info
    stat4 = system.collector.state.stat4_info

    print("\n\n\nAverage travel time for a vessel: \n", stat1)
    print("\n\n\nAverage waiting time for a vessel in the anchorpoint: \n", stat2)
    print("\n\n\nAverage number of vessels in the port: \n", stat3)
    print("\n\n\nTotal vessels in the port at every hour in the simulation: \n", stat4)