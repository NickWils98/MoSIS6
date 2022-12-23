from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from generator import Generator
from waterway import Waterway
from anchorpoint import AnchorPoint
from pypdevs.simulator import Simulator
from control_tower import ControlTower
from confluence import Confluence
from dock import Dock
import random
import numpy as np

class TestSystem(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "QueueSystem")

        # Define all atomic submodels of which there are only one
        generator = self.addSubModel(Generator())
        waterway = self.addSubModel(Waterway(47.52))
        waterway2 = self.addSubModel(Waterway(68.54))
        anchorpoint = self.addSubModel(AnchorPoint())
        control_tower = self.addSubModel(ControlTower())
        confluence = self.addSubModel(Confluence([["K"], ["S"], [1,2,3,4,5,6,7,8]], 3))
        #dock = self.addSubModel(Dock(1))

        self.connectPorts(generator.outport, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)
        self.connectPorts(waterway.out1_port, confluence.in_ports[0])
        self.connectPorts(confluence.out_ports[2], waterway2.in1_port)

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