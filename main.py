from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
import random
import math
import vessel as Vessel
import numpy as np

from pypdevs.simulator import Simulator

if __name__ == '__main__':
    ship = Vessel.TugBoat
    y=0
    x = np.random.exponential(scale=1/250)
    for i in range(0,250):
        x = np.random.exponential(scale=1 / 250)

        y = y+x
    print(y)