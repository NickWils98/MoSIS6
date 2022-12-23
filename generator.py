from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
import random
import numpy as np
import math
import vessel as Vessel


# Define the state of the generator as a structured object
class GeneratorState:
    def __init__(self):
        # Current simulation time (statistics)
        self.current_time = 0.0
        # Remaining time until generation of new event
        self.remaining = 0.0
        # Keep a list of scales on how many vessels are created on each hour
        self.ships_hours = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227,
                            246, 203, 43, 51, 33, 143, 187, 164, 123]

class Generator(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Generator")
        # Output port for the vessel
        self.outport = self.addOutPort("outport")
        # factory to create vessels
        self.factory = Vessel.VesselFactory()
        # Define the state
        self.state = GeneratorState()

    def intTransition(self):
        # Update simulation time
        self.state.current_time += self.timeAdvance()

        # Get the hour from the current time
        hour = math.floor(self.state.current_time) % 24
        # Calculate waiting time to next vessel
        self.state.remaining = np.random.exponential(scale=1 / self.state.ships_hours[hour])
        return self.state

    def timeAdvance(self):
        # Return remaining time; infinity when generated enough
        return self.state.remaining

    def outputFnc(self):
        # Calculate current time (note the addition!)
        creation_time = self.state.current_time + self.state.remaining
        vessel = self.factory.create(creation_time)
        # Output the new event on the output port
        return {self.outport: vessel}