from coupled_devs import port_system
import random
import numpy as np


if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)

    # Set up the system and run
    system = port_system.PortSystem()
    system.run()
