from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
import generator as Generator
import anchorpoint as AnchorPoint
from pypdevs.simulator import Simulator
import random

class TestSystem(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "QueueSystem")

        # Define all atomic submodels of which there are only one
        generator = self.addSubModel(Generator)
        anchorpoint = self.addSubModel(AnchorPoint)

        self.connectPorts(generator.out_event, anchorpoint.in_event)

if __name__ == '__main__':
    # Make sure each of them simulates exactly the same workload
    random.seed(1)
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