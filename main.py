from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from generator import Generator
from waterway import Waterway
from anchorpoint import AnchorPoint
from pypdevs.simulator import Simulator
from control_tower import ControlTower
from confluence import Confluence
from canal import Canal
from dock import Dock
from lock import Lock
from sea import Sea
from port_confluence import ConfluencePort
import random
import numpy as np

class TestSystem(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "QueueSystem")

        # Define all atomic submodels of which there are only one
        generator = self.addSubModel(Generator())
        waterway = self.addSubModel(Waterway(47.52))
        waterway2 = self.addSubModel(Waterway(68.54))
        waterway3 = self.addSubModel(Waterway(2.1))
        waterway4 = self.addSubModel(Waterway(30.85))
        anchorpoint = self.addSubModel(AnchorPoint())
        control_tower = self.addSubModel(ControlTower())
        confluence_port = self.addSubModel(ConfluencePort())
        confluence = self.addSubModel(Confluence([["K"], ["S"], [1, 2, 3, 4, 5, 6, 7, 8]], 3)) # TODO: Narekenen
        confluence2 = self.addSubModel(Confluence([["K", "S", 6, 7, 8], [1], [2, 3, 4, 5]], 3))
        canal = self.addSubModel(Canal(0.8))
        canal2 = self.addSubModel(Canal(1.89))
        dock = self.addSubModel(Dock(1))
        lock = self.addSubModel(Lock("A", 20/60, 1, 7/60, 62500))
        sea = self.addSubModel(Sea())

        self.connectPorts(generator.out_port, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)
        self.connectPorts(waterway.out1_port, confluence.in_ports[0])

        self.connectPorts(confluence.out_ports[2], waterway2.in1_port)


        self.connectPorts(waterway2.out1_port, confluence_port.in_ports[0])
        self.connectPorts(confluence_port.out_ports[1], waterway3.in1_port)

        self.connectPorts(waterway3.out1_port, lock.in_port_sea)
        self.connectPorts(lock.out_port_dock, canal.in1_port)

        self.connectPorts(canal.out1_port, confluence2.in_ports[0])

        self.connectPorts(confluence2.out_ports[1], canal2.in1_port)
        self.connectPorts(canal2.out1_port, dock.in_port)
        self.connectPorts(dock.out_port, canal2.in2_port)
        self.connectPorts(dock.out_event, control_tower.free_event)

        self.connectPorts(canal2.out2_port, confluence2.in_ports[1])


        self.connectPorts(confluence2.out_ports[0], canal.in2_port)
        self.connectPorts(canal.out2_port, lock.in_port_dock)

        self.connectPorts(lock.out_port_sea, waterway3.in2_port)
        self.connectPorts(waterway3.out2_port, confluence_port.in_ports[1])
        self.connectPorts(confluence_port.out_ports[0], waterway2.in2_port)
        self.connectPorts(waterway2.out2_port, confluence.in_ports[2])
        self.connectPorts(confluence.out_ports[1], waterway4.in1_port)
        self.connectPorts(waterway4.out1_port, sea.in_port)




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