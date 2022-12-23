from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from generator import Generator
from waterway import Waterway
from anchorpoint import AnchorPoint
from pypdevs.simulator import Simulator
from control_tower import ControlTower
import random
import numpy as np

class TestSystem(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "QueueSystem")

        # Define all atomic submodels of which there are only one
        generator = self.addSubModel(Generator())
        waterway = self.addSubModel(Waterway(68.54))
        anchorpoint = self.addSubModel(AnchorPoint())
        control_tower = self.addSubModel(ControlTower())

        self.connectPorts(generator.outport, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)

if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)
    # Set up the system
    m = TestSystem()

    # PythonPDEVS specific setup and configuration
    sim = Simulator(m)
    sim.setClassicDEVS()
    sim.simulate()

    '''ship = Vessel.TugBoat
    y=0
    x = np.random.exponential(scale=1/250)
    for i in range(0,250):
        x = np.random.exponential(scale=1 / 250)

        y = y+x
    print(y)'''