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
    stat5A = system.collector.state.stat5A_info
    stat5B = system.collector.state.stat5B_info
    stat5C = system.collector.state.stat5C_info
    stat6A = system.collector.state.stat6A_info
    stat6B = system.collector.state.stat6B_info
    stat6C = system.collector.state.stat6C_info
    stat7A = system.collector.state.stat7A_info
    stat7B = system.collector.state.stat7B_info
    stat7C = system.collector.state.stat7C_info


    print("\n\n\nAverage travel time for a vessel: \n", stat1)
    print("\n\n\nAverage waiting time for a vessel in the anchorpoint: \n", stat2)
    print("\n\n\nAverage number of vessels in the port: \n", stat3)
    print("\n\n\nTotal vessels in the port at every hour in the simulation: \n", stat4)
    print("\n\n\nAverage idle time for LockA: \n", stat5A)
    print("\n\n\nAverage idle time for LockB: \n", stat5B)
    print("\n\n\nAverage idle time for LockC: \n", stat5C)
    print("\n\n\nTimes Lock A changed state without containing ships: \n", stat6A)
    print("\n\n\nTimes Lock B changed state without containing ships: \n", stat6B)
    print("\n\n\nTimes Lock C changed state without containing ships: \n", stat6C)
    print("\n\n\nRemaining capacity for Lock A hourly: \n", stat7A)
    print("\n\n\nRemaining capacity for Lock B hourly: \n", stat7B)
    print("\n\n\nRemaining capacity for Lock C hourly: \n", stat7C)
