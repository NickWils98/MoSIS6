from pypdevs.DEVS import AtomicDEVS
import numpy as np
import math
from messages_events import vessel

# Define the state of the generator as a structured object
class GeneratorState:
    def __init__(self, counter=float('inf'), prob=(.28, .22, .33, .17)):
        # Current simulation time (statistics)
        self.current_time = 0.0
        # Remaining time until generation of new event
        self.remaining = 0.0
        # Keep a list of scales on how many vessels are created on each hour
        self.ships_hours = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227,
                            246, 203, 43, 51, 33, 143, 187, 164, 123]
        self.max_counter = counter
        self.counter = 0
        # factory to create vessels
        self.factory = vessel.VesselFactory(prob)

class Generator(AtomicDEVS):
    def __init__(self, generation_max=-1, prob=(.28, .22, .33, .17)):
        AtomicDEVS.__init__(self, "Generator")
        # Output port for the vessel
        self.out_port = self.addOutPort("out_port")
        # Define the state
        self.state = GeneratorState(generation_max, prob)

    def intTransition(self):
        self.state.counter+=1
        # Update simulation time
        self.state.current_time += self.state.remaining

        # Get the hour from the current time
        hour = math.floor(self.state.current_time) % 24
        # Calculate waiting time to next vessel
        self.state.remaining = np.random.exponential(scale=1 / self.state.ships_hours[hour])
        if self.state.counter >=self.state.max_counter:
            self.state.remaining = float('inf')
        return self.state

    def timeAdvance(self):
        # Return remaining time; infinity when generated enough
        return self.state.remaining

    def outputFnc(self):
        if self.state.counter >=self.state.max_counter:
            return {}
        # Calculate current time (note the addition!)
        creation_time = self.state.current_time + self.state.remaining
        vessel = self.state.factory.create(creation_time)
        # Output the new event on the output port
        return {self.out_port: vessel}