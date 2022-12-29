import model
import random
import numpy as np
from pypdevs.simulator import Simulator
import matplotlib.pyplot as plt

SEED = 123

prob_COT = .0
prob_BK = .0
prob_TB = 1.0
prob_SCF = .0
prob = (prob_COT, prob_BK, prob_TB, prob_SCF)

if __name__ == '__main__':
    values = []

    # Make sure each of them simulates exactly the same workload
    random.seed(SEED)
    np.random.seed(SEED)

    # Set up the system and run
    system = model.PortSystem()
    sim = Simulator(system)
    sim.setTerminationTime(168)
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
    f = open(f'task6_seed{SEED}.txt', 'w')

    f.write(f"Average travel time for a vessel: \n {stat1[-1]}" )
    f.write(f"\n\n\nAverage waiting time for a vessel in the anchorpoint: \n{stat2[-1]}")
    f.write(f"\n\n\nAverage number of vessels in the port: \n{stat3[-1]}")
    f.write(f"\n\n\nTotal vessels in the port at every hour in the simulation: \n{stat4}")
    f.write(f"\n\n\nAverage idle time for Lock A: \n{stat5A[-1]}")
    f.write(f"\n\n\nAverage idle time for Lock B: \n{stat5B[-1]}")
    f.write(f"\n\n\nAverage idle time for Lock C: \n{stat5C[-1]}")
    f.write(f"\n\n\nTimes Lock A changed state without containing ships: \n{stat6A[-1]}")
    f.write(f"\n\n\nTimes Lock B changed state without containing ships: \n{stat6B[-1]}")
    f.write(f"\n\n\nTimes Lock C changed state without containing ships: \n{stat6C[-1]}")
    f.write(f"\n\n\nRemaining capacity for Lock A hourly: \n{stat7A}")
    f.write(f"\n\n\nRemaining capacity for Lock B hourly: \n{stat7B}")
    f.write(f"\n\n\nRemaining capacity for Lock C hourly: \n{stat7C}")

    f.write(f"\n\n\nCrudeOilTanker:{system.generator.state.factory.counter_COT}")
    f.write(f"\n\n\nBulkCarrier:{system.generator.state.factory.counter_BK}")
    f.write(f"\n\n\nTugBoat:{system.generator.state.factory.counter_TB}")
    f.write(f"\n\n\nSmallCargoFreighter:{system.generator.state.factory.counter_SCF}")


    plt.plot(range(len(stat4)), stat4)
    plt.xlabel('hour')
    plt.ylabel('number of vessels in port')
    plt.title('Total number of vessels in the port at every hour')
    plt.savefig(f"task6_stat4_seed{SEED}.png")
    plt.show()


    plt.plot(range(len(stat7A)), stat7A)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock A')
    plt.savefig(f"task6_stat7A_seed{SEED}.png")
    plt.show()

    plt.plot(range(len(stat7B)), stat7B)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock B')
    plt.savefig(f"task6_stat7B_seed{SEED}.png")
    plt.show()

    plt.plot(range(len(stat7C)), stat7C)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock C')
    plt.savefig(f"task6_stat7C_seed{SEED}.png")
    plt.show()
