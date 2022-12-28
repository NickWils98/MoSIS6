from coupled_devs import experiment as Experiment
import random
import numpy as np


if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)

    # Set up the system and run
    system = Experiment.TestSystemFull()
    system.run()
