from pypdevs.DEVS import AtomicDEVS
import numpy as np
import math
from messages_events import vessel

# Define the state of the generator as a structured object
class GeneratorState:
    def __init__(self, det_bool=False, counter=float('inf'), prob=(.28, .22, .33, .17)):
        """
        det_bool: a boolean that tells if the generator needs to be deterministic
        counter: a number that tells the maximum amount of vessels that may be generated in total
        prob: the probabilities of the vessels in order of [CrudeOilTanker, BulkCarrier, TugBoat, SmallCargoFreighter]
        """
        # Current simulation time
        self.current_time = 0.0
        # Remaining time until generation of new event
        self.remaining = 0.0
        # Keep a list of scales on how many vessels are created on each hour
        self.ships_hours = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227,
                            246, 203, 43, 51, 33, 143, 187, 164, 123]
        # statistic
        self.counter = 0
        # factory to create vessels
        self.factory = vessel.VesselFactory(det_bool,prob)

        self.max_counter = counter
        self.det_bool = det_bool

class Generator(AtomicDEVS):
    def __init__(self, det_bool=False, generation_max=-1, prob=(.28, .22, .33, .17)):
        """
        det_bool: a boolean that tells if the generator needs to be deterministic
        counter: a number that tells the maximum amount of vessels that may be generated in total
        prob: the probabilities of the vessels in order of [CrudeOilTanker, BulkCarrier, TugBoat, SmallCargoFreighter]
        """
        AtomicDEVS.__init__(self, "Generator")
        # Output port for the vessel
        self.out_port = self.addOutPort("out_port")
        self.out_count = self.addOutPort("out_count")

        # Define the state
        self.state = GeneratorState(det_bool, generation_max, prob)

    def intTransition(self):
        self.state.counter+=1
        # Update simulation time
        self.state.current_time += self.state.remaining

        # Get the hour from the current time
        hour = math.floor(self.state.current_time) % 24

        # Calculate waiting time to next vessel
        if self.state.det_bool:
            # deterministic
            self.state.remaining = 1/self.state.ships_hours[hour]
        else:
            # random
            self.state.remaining = np.random.exponential(scale=1 / self.state.ships_hours[hour])

        # check the maximum counter
        if self.state.counter >=self.state.max_counter:
            self.state.remaining = float('inf')
        return self.state

    def timeAdvance(self):
        # Return remaining time; infinity when generated enough
        return self.state.remaining

    def outputFnc(self):
        # don't output anything if the maximum generated vessels is reached
        if self.state.counter >=self.state.max_counter:
            return {}
        # Calculate current time (note the addition!)
        creation_time = self.state.current_time + self.state.remaining
        # create the vessel
        boat = self.state.factory.create(creation_time)

        # Output the new event on the output port
        return {self.out_port: boat, self.out_count: self.state.factory.counter}