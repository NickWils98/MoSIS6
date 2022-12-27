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

class TestSystemSmall(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "SmallSystem")

        # Define generator atomic submodel
        generator = self.addSubModel(Generator())

        # Define anchorpoint atomic submodel
        anchorpoint = self.addSubModel(AnchorPoint())

        # Define sea atomic submodel
        sea = self.addSubModel(Sea())

        # Define control_tower atomic submodel
        control_tower = self.addSubModel(ControlTower())

        # Define all waterway atomic submodels
        waterway_K = self.addSubModel(Waterway(47.52))
        waterway_S = self.addSubModel(Waterway(30.85))
        waterway_KS_to_CP = self.addSubModel(Waterway(68.54))
        waterway_CP_to_A = self.addSubModel(Waterway(2.1))
        waterway_CP_to_MID = self.addSubModel(Waterway(4.7))
        waterway_MID_to_C = self.addSubModel(Waterway(5.16))

        # Define all confluence atomic submodels
        confluence_port = self.addSubModel(ConfluencePort())
        confluence_KS = self.addSubModel(Confluence([["K"], ["S"], [1, 2, 3, 4, 5, 6, 7, 8]], 3))  # TODO: Narekenen
        confluence_MID = self.addSubModel(Confluence([["K", "S", 6, 7, 8], [3, 4, 5], [1, 2]], 3))
        confluence_A1 = self.addSubModel(Confluence([["K", "S", 6, 7, 8], [1], [2, 3, 4, 5]], 3))
        confluence_A2 = self.addSubModel(Confluence([], 3))
        confluence_B1 = self.addSubModel(Confluence([], 3))
        confluence_B2 = self.addSubModel(Confluence([], 3))
        confluence_C1 = self.addSubModel(Confluence([], 5))

        # Define all canal atomic submodels
        canal_A1_A = self.addSubModel(Canal(0.8))
        canal_A1_1 = self.addSubModel(Canal(1.89))
        canal_A1_A2 = self.addSubModel(Canal(2.39))

        canal_A2_2 = self.addSubModel(Canal(1.13))
        canal_A2_C1 = self.addSubModel(Canal(5.70))

        canal_C1_C = self.addSubModel(Canal(1.08))
        canal_C1_4 = self.addSubModel(Canal(1.30))
        canal_C1_5 = self.addSubModel(Canal(1.68))
        canal_C1_3 = self.addSubModel(Canal(1.86))

        canal_MID_B = self.addSubModel(Canal(3.14))

        canal_B1_B = self.addSubModel(Canal(0.89))
        canal_B1_B2 = self.addSubModel(Canal(1.24))
        canal_B1_8 = self.addSubModel(Canal(2.4))

        canal_B2_7 = self.addSubModel(Canal(1.07))
        canal_B2_6 = self.addSubModel(Canal(1.37))

        # Define all lock atomic submodels
        lock_A = self.addSubModel(Lock("A", 20/60, 1, 7/60, 62500))
        lock_B = self.addSubModel(Lock("B", 12/60, 45/60, 5/60, 34000))
        lock_C = self.addSubModel(Lock("C", 8/60, 30/60, 5/60, 25650))

        # Define all dock atomic submodels
        dock_1 = self.addSubModel(Dock(1))
        dock_2 = self.addSubModel(Dock(2))
        dock_3 = self.addSubModel(Dock(3))
        dock_4 = self.addSubModel(Dock(4))
        dock_5 = self.addSubModel(Dock(5))
        dock_6 = self.addSubModel(Dock(6))
        dock_7 = self.addSubModel(Dock(7))
        dock_8 = self.addSubModel(Dock(8))






        self.connectPorts(generator.out_port, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway_K.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)
        self.connectPorts(waterway_K.out1_port, confluence_KS.in_ports[0])

        self.connectPorts(confluence_KS.out_ports[2], waterway_KS_to_CP.in1_port)


        self.connectPorts(waterway_KS_to_CP.out1_port, confluence_port.in_ports[0])
        self.connectPorts(confluence_port.out_ports[1], waterway_CP_to_A.in1_port)

        self.connectPorts(waterway_CP_to_A.out1_port, lock_A.in_port_sea)
        self.connectPorts(lock_A.out_port_dock, canal_A1_A.in1_port)

        self.connectPorts(canal_A1_A.out1_port, confluence_A1.in_ports[0])

        self.connectPorts(confluence_A1.out_ports[1], canal_A1_1.in1_port)
        self.connectPorts(canal_A1_1.out1_port, dock_1.in_port)
        self.connectPorts(dock_1.out_port, canal_A1_1.in2_port)
        self.connectPorts(dock_1.out_event, control_tower.free_event)

        self.connectPorts(canal_A1_1.out2_port, confluence_A1.in_ports[1])


        self.connectPorts(confluence_A1.out_ports[0], canal_A1_A.in2_port)
        self.connectPorts(canal_A1_A.out2_port, lock_A.in_port_dock)

        self.connectPorts(lock_A.out_port_sea, waterway_CP_to_A.in2_port)
        self.connectPorts(waterway_CP_to_A.out2_port, confluence_port.in_ports[1])
        self.connectPorts(confluence_port.out_ports[0], waterway_KS_to_CP.in2_port)
        self.connectPorts(waterway_KS_to_CP.out2_port, confluence_KS.in_ports[2])
        self.connectPorts(confluence_KS.out_ports[1], waterway_S.in1_port)
        self.connectPorts(waterway_S.out1_port, sea.in_port)

class TestSystemFull(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "FullSystem")

        # Define generator atomic submodel
        generator = self.addSubModel(Generator())

        # Define anchorpoint atomic submodel
        anchorpoint = self.addSubModel(AnchorPoint())

        # Define sea atomic submodel
        sea = self.addSubModel(Sea())

        # Define control_tower atomic submodel
        control_tower = self.addSubModel(ControlTower())

        # Define all waterway atomic submodels
        waterway_K = self.addSubModel(Waterway(47.52))
        waterway_S = self.addSubModel(Waterway(30.85))
        waterway_KS_to_CP = self.addSubModel(Waterway(68.54))
        waterway_CP_to_A = self.addSubModel(Waterway(2.1))
        waterway_CP_to_MID = self.addSubModel(Waterway(4.7))
        waterway_MID_to_C = self.addSubModel(Waterway(5.16))

        # Define all confluence atomic submodels
        confluence_port = self.addSubModel(ConfluencePort())
        confluence_KS = self.addSubModel(Confluence([["K"], ["S"], [1, 2, 3, 4, 5, 6, 7, 8]], 3))  # TODO: moet "K" hier wel instaan aangezien da eig ni reached kan worden
        confluence_MID = self.addSubModel(Confluence([[6, 7, 8], ["K", "S", 1, 2], [3, 4, 5]], 3))
        confluence_A1 = self.addSubModel(Confluence([["K", "S", 6, 7, 8], [1], [2, 3, 4, 5]], 3))
        confluence_A2 = self.addSubModel(Confluence([[2], ["K", "S", 1, 6, 7, 8], [3, 4, 5]], 3))
        confluence_B1 = self.addSubModel(Confluence([["K", "S", 1, 2, 3, 4, 5], [6, 7], [8]], 3))
        confluence_B2 = self.addSubModel(Confluence([[7], [6], ["K", "S", 1, 2, 3, 4, 5]], 3))
        confluence_C1 = self.addSubModel(Confluence([["K", "S", 6, 7, 8], [4], [5], [3], [1, 2]], 5))

        # Define all canal atomic submodels
        canal_A1_A = self.addSubModel(Canal(0.8))
        canal_A1_1 = self.addSubModel(Canal(1.89))
        canal_A1_A2 = self.addSubModel(Canal(2.39))

        canal_A2_2 = self.addSubModel(Canal(1.13))
        canal_A2_C1 = self.addSubModel(Canal(5.70))

        canal_C1_C = self.addSubModel(Canal(1.08))
        canal_C1_4 = self.addSubModel(Canal(1.30))
        canal_C1_5 = self.addSubModel(Canal(1.68))
        canal_C1_3 = self.addSubModel(Canal(1.86))

        canal_MID_B = self.addSubModel(Canal(3.14))

        canal_B1_B = self.addSubModel(Canal(0.89))
        canal_B1_B2 = self.addSubModel(Canal(1.24))
        canal_B1_8 = self.addSubModel(Canal(2.4))

        canal_B2_7 = self.addSubModel(Canal(1.07))
        canal_B2_6 = self.addSubModel(Canal(1.37))

        # Define all lock atomic submodels
        lock_A = self.addSubModel(Lock("A", 20/60, 1, 7/60, 62500))
        lock_B = self.addSubModel(Lock("B", 12/60, 45/60, 5/60, 34000))
        lock_C = self.addSubModel(Lock("C", 8/60, 30/60, 5/60, 25650))

        # Define all dock atomic submodels
        dock_1 = self.addSubModel(Dock(1))
        dock_2 = self.addSubModel(Dock(2))
        dock_3 = self.addSubModel(Dock(3))
        dock_4 = self.addSubModel(Dock(4))
        dock_5 = self.addSubModel(Dock(5))
        dock_6 = self.addSubModel(Dock(6))
        dock_7 = self.addSubModel(Dock(7))
        dock_8 = self.addSubModel(Dock(8))


        # Connect generator, anchorpoint, control_tower and confluence_KS
        self.connectPorts(generator.out_port, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway_K.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)
        self.connectPorts(waterway_K.out1_port, confluence_KS.in_ports[0])

        # Connect confluence KS to waterway KS->CP
        self.connectPorts(confluence_KS.out_ports[2], waterway_KS_to_CP.in1_port)


        self.connectPorts(waterway_KS_to_CP.out1_port, confluence_port.in_ports[0])
        self.connectPorts(confluence_port.out_ports[1], waterway_CP_to_A.in1_port)

        self.connectPorts(waterway_CP_to_A.out1_port, lock_A.in_port_sea)
        self.connectPorts(lock_A.out_port_dock, canal_A1_A.in1_port)

        self.connectPorts(canal_A1_A.out1_port, confluence_A1.in_ports[0])

        self.connectPorts(confluence_A1.out_ports[1], canal_A1_1.in1_port)
        self.connectPorts(canal_A1_1.out1_port, dock_1.in_port)
        self.connectPorts(dock_1.out_port, canal_A1_1.in2_port)
        self.connectPorts(dock_1.out_event, control_tower.free_event)

        self.connectPorts(canal_A1_1.out2_port, confluence_A1.in_ports[1])


        self.connectPorts(confluence_A1.out_ports[0], canal_A1_A.in2_port)
        self.connectPorts(canal_A1_A.out2_port, lock_A.in_port_dock)

        self.connectPorts(lock_A.out_port_sea, waterway_CP_to_A.in2_port)
        self.connectPorts(waterway_CP_to_A.out2_port, confluence_port.in_ports[1])
        self.connectPorts(confluence_port.out_ports[0], waterway_KS_to_CP.in2_port)
        self.connectPorts(waterway_KS_to_CP.out2_port, confluence_KS.in_ports[2])
        self.connectPorts(confluence_KS.out_ports[1], waterway_S.in1_port)
        self.connectPorts(waterway_S.out1_port, sea.in_port)


if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(42)
    np.random.seed(42)
    # Set up the system
    m = TestSystemSmall()

    # PythonPDEVS specific setup and configuration
    sim = Simulator(m)
    sim.setClassicDEVS()
    sim.simulate()
