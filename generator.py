from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
import random
import numpy as np
import math
import vessel as Vessel
from pypdevs.simulator import Simulator

SHIPS_HOURS = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227, 246, 203, 43, 51, 33, 143, 187, 164, 123]

# Define the state of the generator as a structured object
class GeneratorState:
    def __init__(self, gen_num):
        # Current simulation time (statistics)
        self.current_time = 0.0
        # Remaining time until generation of new event
        self.remaining = 0.0
        # Counter on how many events to generate still
        # self.to_generate = gen_num
        hour = 24 % math.floor(self.current_time)
        self.next_generate_time = np.random.exponential(scale=1 / SHIPS_HOURS[hour])
        ":'("

class Generator(AtomicDEVS):
    def __init__(self, gen_param, size_param, gen_num):
        AtomicDEVS.__init__(self, "Generator")
        # Output port for the vessel
        self.outport = self.addOutPort("outport")
        # Define the state
        self.state = GeneratorState(gen_num)

        # Parameters defining the generator's behaviour
        self.gen_param = gen_param
        self.size_param = size_param

    def intTransition(self):
        # Update simulation time
        self.state.current_time += self.timeAdvance()
        # Update number of generated events
        self.state.to_generate -= 1
        if self.state.to_generate == 0:
            # Already generated enough events, so stop
            self.state.remaining = float('inf')
        else:
            # Still have to generate events, so sample for new duration
            self.state.remaining = random.expovariate(self.gen_param)
        return self.state

    def timeAdvance(self):
        # Return remaining time; infinity when generated enough
        return self.state.remaining

    def outputFnc(self):
        # Determine size of the event to generate
        size = max(1, int(random.gauss(self.size_param, 5)))
        # Calculate current time (note the addition!)
        creation = self.state.current_time + self.state.remaining
        # Output the new event on the output port
        return {self.out_event: Job(size, creation)}