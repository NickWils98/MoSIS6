from pypdevs.DEVS import CoupledDEVS
from atomic_devs.generator import Generator
from atomic_devs.waterway import Waterway
from atomic_devs.anchorpoint import AnchorPoint
from pypdevs.simulator import Simulator
from atomic_devs.control_tower import ControlTower
from atomic_devs.confluence import Confluence
from atomic_devs.canal import Canal
from atomic_devs.dock import Dock
from atomic_devs.lock import Lock
from atomic_devs.sea import Sea
from atomic_devs.collector import Collector
from atomic_devs.confluence_port import ConfluencePort

class PortSystem(CoupledDEVS):
    def __init__(self, det_bool=False, generation_max=float('inf'), prob=(.28, .22, .33, .17), change_lock_interval=1):

        CoupledDEVS.__init__(self, "FullSystem")

        self.ships_to_generate = generation_max

        # Define generator atomic submodel
        generator = self.addSubModel(Generator(det_bool, generation_max, prob))

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
        confluence_KS = self.addSubModel(Confluence([["K"], [1, 2, 3, 4, 5, 6, 7, 8], ["S"], ], 3))
        confluence_MID = self.addSubModel(Confluence([["S", 1, 2], [3, 4, 5], [6, 7, 8]], 3))
        confluence_A1 = self.addSubModel(Confluence([["S", 6, 7, 8], [1], [2, 3, 4, 5]], 3))
        confluence_A2 = self.addSubModel(Confluence([["S", 1, 6, 7, 8], [2], [3, 4, 5]], 3))
        confluence_B1 = self.addSubModel(Confluence([["S", 1, 2, 3, 4, 5], [8], [6, 7]], 3))
        confluence_B2 = self.addSubModel(Confluence([[6], [7], ["S", 1, 2, 3, 4, 5, 8]], 3))
        confluence_C1 = self.addSubModel(Confluence([["S", 6, 7, 8], [5], [4], [3], [1, 2]], 5))

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
        lock_A = self.addSubModel(Lock("A", 20/60, (change_lock_interval*(60))/60, 7/60, 62500))
        lock_B = self.addSubModel(Lock("B", 12/60, (change_lock_interval*(45))/60, 5/60, 34000))
        lock_C = self.addSubModel(Lock("C", 8/60, (change_lock_interval*(30))/60, 5/60, 25650))

        # Define all dock atomic submodels
        dock_1 = self.addSubModel(Dock(1, det_bool))
        dock_2 = self.addSubModel(Dock(2, det_bool))
        dock_3 = self.addSubModel(Dock(3, det_bool))
        dock_4 = self.addSubModel(Dock(4, det_bool))
        dock_5 = self.addSubModel(Dock(5, det_bool))
        dock_6 = self.addSubModel(Dock(6, det_bool))
        dock_7 = self.addSubModel(Dock(7, det_bool))
        dock_8 = self.addSubModel(Dock(8, det_bool))

        # Define colector atomic submodel
        collector = self.addSubModel(Collector())

        # Connect generator, anchorpoint, Sea, control_tower and confluence_KS
        self.connectPorts(generator.out_port, anchorpoint.in_port)
        self.connectPorts(anchorpoint.out_port, waterway_K.in1_port)
        self.connectPorts(anchorpoint.out_event, control_tower.in_event)
        self.connectPorts(control_tower.out_event, anchorpoint.in_event)
        self.connectPorts(waterway_K.out1_port, confluence_KS.in_ports[0])
        self.connectPorts(confluence_KS.out_ports[2], waterway_S.in1_port)
        self.connectPorts(waterway_S.out1_port, sea.in_port)

        # Connect confluence KS to waterway KS->CP and vice versa
        self.connectPorts(confluence_KS.out_ports[1], waterway_KS_to_CP.in1_port)
        self.connectPorts(waterway_KS_to_CP.out1_port, confluence_port.in_ports[0])
        self.connectPorts(confluence_port.out_ports[0], waterway_KS_to_CP.in2_port)
        self.connectPorts(waterway_KS_to_CP.out2_port, confluence_KS.in_ports[1])

        # Connect confluence CP to Lock A
        self.connectPorts(confluence_port.out_ports[1], waterway_CP_to_A.in1_port)
        self.connectPorts(waterway_CP_to_A.out1_port, lock_A.in_port_sea)
        self.connectPorts(lock_A.out_port_sea, waterway_CP_to_A.in2_port)
        self.connectPorts(waterway_CP_to_A.out2_port, confluence_port.in_ports[1])

        # Connect confluence CP to confluence Mid
        self.connectPorts(confluence_port.out_ports[2], waterway_CP_to_MID.in1_port)
        self.connectPorts(waterway_CP_to_MID.out1_port, confluence_MID.in_ports[0])
        self.connectPorts(confluence_MID.out_ports[0], waterway_CP_to_MID.in2_port)
        self.connectPorts(waterway_CP_to_MID.out2_port, confluence_port.in_ports[2])

        # Connect Lock_A to Confluence A1
        self.connectPorts(lock_A.out_port_dock, canal_A1_A.in1_port)
        self.connectPorts(canal_A1_A.out1_port, confluence_A1.in_ports[0])
        self.connectPorts(confluence_A1.out_ports[0], canal_A1_A.in2_port)
        self.connectPorts(canal_A1_A.out2_port, lock_A.in_port_dock)

        # Connect Confluence A1 to dock 1
        self.connectPorts(confluence_A1.out_ports[1], canal_A1_1.in1_port)
        self.connectPorts(canal_A1_1.out1_port, dock_1.in_port)
        self.connectPorts(dock_1.out_port, canal_A1_1.in2_port)
        self.connectPorts(dock_1.out_event, control_tower.free_event)
        self.connectPorts(canal_A1_1.out2_port, confluence_A1.in_ports[1])

        # Connect Confluence A1 to confluence A2
        self.connectPorts(confluence_A1.out_ports[2], canal_A1_A2.in1_port)
        self.connectPorts(canal_A1_A2.out1_port, confluence_A2.in_ports[0])
        self.connectPorts(confluence_A2.out_ports[0], canal_A1_A2.in2_port)
        self.connectPorts(canal_A1_A2.out2_port, confluence_A1.in_ports[2])

        # Connect Confluence A2 to dock 2
        self.connectPorts(confluence_A2.out_ports[1], canal_A2_2.in1_port)
        self.connectPorts(canal_A2_2.out1_port, dock_2.in_port)
        self.connectPorts(dock_2.out_port, canal_A2_2.in2_port)
        self.connectPorts(dock_2.out_event, control_tower.free_event)
        self.connectPorts(canal_A2_2.out2_port, confluence_A2.in_ports[1])

        # Connect confluence A2 to confluence C1
        self.connectPorts(confluence_A2.out_ports[2], canal_A2_C1.in1_port)
        self.connectPorts(canal_A2_C1.out1_port, confluence_C1.in_ports[4])
        self.connectPorts(confluence_C1.out_ports[4], canal_A2_C1.in2_port)
        self.connectPorts(canal_A2_C1.out2_port, confluence_A2.in_ports[2])

        # # confluence mid to C
        self.connectPorts(confluence_MID.out_ports[1], waterway_MID_to_C.in1_port)
        self.connectPorts(waterway_MID_to_C.out1_port, lock_C.in_port_sea)
        self.connectPorts(lock_C.out_port_sea, waterway_MID_to_C.in2_port)
        self.connectPorts(waterway_MID_to_C.out2_port, confluence_MID.in_ports[1])

        # Connect Lock_C to Confluence C1
        self.connectPorts(lock_C.out_port_dock, canal_C1_C.in1_port)
        self.connectPorts(canal_C1_C.out1_port, confluence_C1.in_ports[0])
        self.connectPorts(confluence_C1.out_ports[0], canal_C1_C.in2_port)
        self.connectPorts(canal_C1_C.out2_port, lock_C.in_port_dock)

        # Connect Confluence C1 to dock 5
        self.connectPorts(confluence_C1.out_ports[1], canal_C1_5.in1_port)
        self.connectPorts(canal_C1_5.out1_port, dock_5.in_port)
        self.connectPorts(dock_5.out_port, canal_C1_5.in2_port)
        self.connectPorts(dock_5.out_event, control_tower.free_event)
        self.connectPorts(canal_C1_5.out2_port, confluence_C1.in_ports[1])

        # Connect Confluence C1 to dock 4
        self.connectPorts(confluence_C1.out_ports[2], canal_C1_4.in1_port)
        self.connectPorts(canal_C1_4.out1_port, dock_4.in_port)
        self.connectPorts(dock_4.out_port, canal_C1_4.in2_port)
        self.connectPorts(dock_4.out_event, control_tower.free_event)
        self.connectPorts(canal_C1_4.out2_port, confluence_C1.in_ports[2])

        # Connect Confluence C1 to dock 3
        self.connectPorts(confluence_C1.out_ports[3], canal_C1_3.in1_port)
        self.connectPorts(canal_C1_3.out1_port, dock_3.in_port)
        self.connectPorts(dock_3.out_port, canal_C1_3.in2_port)
        self.connectPorts(dock_3.out_event, control_tower.free_event)
        self.connectPorts(canal_C1_3.out2_port, confluence_C1.in_ports[3])

        # Connect confluence Mid to lock B
        self.connectPorts(confluence_MID.out_ports[2], canal_MID_B.in1_port)
        self.connectPorts(canal_MID_B.out1_port, lock_B.in_port_sea)
        self.connectPorts(lock_B.out_port_sea, canal_MID_B.in2_port)
        self.connectPorts(canal_MID_B.out2_port, confluence_MID.in_ports[2])

        # Connect lock B to confluence B1
        self.connectPorts(lock_B.out_port_dock, canal_B1_B.in1_port)
        self.connectPorts(canal_B1_B.out1_port, confluence_B1.in_ports[0])
        self.connectPorts(confluence_B1.out_ports[0], canal_B1_B.in2_port)
        self.connectPorts(canal_B1_B.out2_port, lock_B.in_port_dock)

        # Connect confluence B1 to lock 8
        self.connectPorts(confluence_B1.out_ports[1], canal_B1_8.in1_port)
        self.connectPorts(canal_B1_8.out1_port, dock_8.in_port)
        self.connectPorts(dock_8.out_port, canal_B1_8.in2_port)
        self.connectPorts(dock_8.out_event, control_tower.free_event)
        self.connectPorts(canal_B1_8.out2_port, confluence_B1.in_ports[1])

        # Connect confluence B1 to confluence B2
        self.connectPorts(confluence_B1.out_ports[2], canal_B1_B2.in1_port)
        self.connectPorts(canal_B1_B2.out1_port, confluence_B2.in_ports[2])
        self.connectPorts(confluence_B2.out_ports[2], canal_B1_B2.in2_port)
        self.connectPorts(canal_B1_B2.out2_port, confluence_B1.in_ports[2])

        # Connect confluence B2 to lock 6
        self.connectPorts(confluence_B2.out_ports[0], canal_B2_6.in1_port)
        self.connectPorts(canal_B2_6.out1_port, dock_6.in_port)
        self.connectPorts(dock_6.out_port, canal_B2_6.in2_port)
        self.connectPorts(dock_6.out_event, control_tower.free_event)
        self.connectPorts(canal_B2_6.out2_port, confluence_B2.in_ports[0])

        # Connect confluence B2 to lock 7
        self.connectPorts(confluence_B2.out_ports[1], canal_B2_7.in1_port)
        self.connectPorts(canal_B2_7.out1_port, dock_7.in_port)
        self.connectPorts(dock_7.out_port, canal_B2_7.in2_port)
        self.connectPorts(dock_7.out_event, control_tower.free_event)
        self.connectPorts(canal_B2_7.out2_port, confluence_B2.in_ports[1])

        # Connect collector ports for statistic 1
        self.connectPorts(confluence_port.stat1_out, collector.stat1_in)

        # Connect collector ports for statistic 2
        self.connectPorts(anchorpoint.stat2_out, collector.stat2_in)

        # Connect collector ports for statistic 3
        self.connectPorts(confluence_port.stat3_out, collector.stat3_in)

        # Connect collector ports for statistic 4
        self.connectPorts(confluence_port.stat4_out, collector.stat4_in)

        # Connect collector ports for statistic 5
        self.connectPorts(lock_A.stat5_out, collector.stat5A_in)
        self.connectPorts(lock_B.stat5_out, collector.stat5B_in)
        self.connectPorts(lock_C.stat5_out, collector.stat5C_in)

        # Connect collector ports for statistic 6
        self.connectPorts(lock_A.stat6_out, collector.stat6A_in)
        self.connectPorts(lock_B.stat6_out, collector.stat6B_in)
        self.connectPorts(lock_C.stat6_out, collector.stat6C_in)

        # Connect collector ports for statistic 6
        self.connectPorts(lock_A.stat7_out, collector.stat7A_in)
        self.connectPorts(lock_B.stat7_out, collector.stat7B_in)
        self.connectPorts(lock_C.stat7_out, collector.stat7C_in)

        # Connect sea for to collector
        self.connectPorts(sea.out_port, collector.total_left_input)
        self.connectPorts(generator.out_count, collector.ships_count_input)

        # Make it accessible outside of our own scope
        self.collector = collector


    def run(self):
        # PythonPDEVS specific setup and configuration
        sim = Simulator(self)
        sim.setClassicDEVS()
        sim.simulate()
