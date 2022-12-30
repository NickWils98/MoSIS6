import model
import random
import numpy as np
from pypdevs.simulator import Simulator
import matplotlib.pyplot as plt

SEED = 69


if __name__ == '__main__':
    values = []

    # Make sure each of them simulates exactly the same workload
    random.seed(SEED)
    np.random.seed(SEED)

    # Set up the system and run
    system = model.PortSystem(change_lock_interval=1/1.3)
    sim = Simulator(system)
    sim.setTerminationTime(168)
    sim.setClassicDEVS()
    sim.simulate()

    # Gather information for output
    total = system.collector.state.total_ships_left_sea

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
    # Write all data to txt file
    filename = f"model/plots/task7/seed{SEED}/lock/"

    f = open(f'{filename}task7_lock_seed{SEED}_info.txt', 'w')

    f.write(f"Total amount of ships that left the port via the Sea: {total}")
    f.write(f"\n\tCrudeOilTanker: {system.collector.state.ships_count_type[0]}")
    f.write(f"\n\tBulkCarrier: {system.collector.state.ships_count_type[1]}")
    f.write(f"\n\tTugBoat: {system.collector.state.ships_count_type[2]}")
    f.write(f"\n\tSmallCargoFreighter: {system.collector.state.ships_count_type[3]}")

    f.write(f"\n\nAverage travel time for a vessel: {stat1[-1]}")
    f.write(f"\n\nAverage waiting time for a vessel in the anchorpoint: {stat2[-1]}")
    f.write(f"\n\nAverage number of vessels in the port: {stat3[-1]}")
    f.write(f"\n\nTotal vessels in the port at every hour in the simulation: \n{stat4}")
    f.write(f"\n\nAverage idle time for Lock A: {stat5A[-1]}")
    f.write(f"\n\nAverage idle time for Lock B: {stat5B[-1]}")
    f.write(f"\n\nAverage idle time for Lock C: {stat5C[-1]}")
    f.write(f"\n\nTimes Lock A changed state without containing ships: {stat6A[-1]}")
    f.write(f"\n\nTimes Lock B changed state without containing ships: {stat6B[-1]}")
    f.write(f"\n\nTimes Lock C changed state without containing ships: {stat6C[-1]}")
    f.write(f"\n\nRemaining capacity for Lock A hourly: \n{stat7A}")
    f.write(f"\n\nRemaining capacity for Lock B hourly: \n{stat7B}")
    f.write(f"\n\nRemaining capacity for Lock C hourly: \n{stat7C}")

    # Plot everything for 4 and 7
    plt.plot(range(len(stat4)), stat4)
    plt.xlabel('hour')
    plt.ylabel('number of vessels in port')
    plt.title('Total number of vessels in the port at every hour')
    plt.savefig(f"{filename}stat4_lock_seed{SEED}.png")
    plt.show()

    plt.plot(range(len(stat7A)), stat7A)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock A')
    plt.savefig(f"{filename}stat7A_lock_seed{SEED}.png")
    plt.show()

    plt.plot(range(len(stat7B)), stat7B)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock B')
    plt.savefig(f"{filename}stat7B_lock_seed{SEED}.png")
    plt.show()

    plt.plot(range(len(stat7C)), stat7C)
    plt.xlabel('hour')
    plt.ylabel('Remaining capacity')
    plt.title('Remaining capacity for each Lock at every hour Lock C')
    plt.savefig(f"{filename}stat7C_lock_seed{SEED}.png")
    plt.show()