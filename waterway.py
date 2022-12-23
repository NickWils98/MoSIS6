from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.remaining_time = 0

        # dict: key = vessel in 1 way, value is the remaining time
        self.ingoing = {}
        self.ingoing_leaving = []
        # dict: key = vessel in 1 way, value is the remaining time
        self.outgoing = {}
        self.ingoing_leaving = []

        # distance of the waterway
        self.distance = distance
        self.remaining_time = float('inf')


class Waterway(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "K")
        self.state = WaterwayState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")


    def intTransition(self):

        # update all the remaining times
        for vessel in self.state.ingoing.keys():
            # self.state.ingoing[vessel] -= self.state.remaining_time
            self.state.ingoing[vessel] -= self.timeAdvance()

            #  if the vessel is arrived add it to the leaving list
            if self.state.ingoing[vessel] <= 0:
                self.state.ingoing_leaving.append(vessel)

        # delete the arrived vessel
        for vessel in self.state.ingoing_leaving:
            del self.state.ingoing[vessel]

        return self.state

    def extTransition(self, inputs):
        # update all the remaining times
        for vessel in self.state.ingoing.keys():
            self.state.ingoing[vessel] -= self.elapsed

        # add a new vessel in the waterway
        if self.in1_port in inputs:
            vessel = inputs[self.in1_port]
            # calculate the remaining time
            remaining_time = self.state.distance / vessel.avg_v
            self.state.ingoing[vessel] = remaining_time

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the waterway
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.ingoing.keys()) > 0:
            self.state.remaining_time = min(self.state.ingoing.values())
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        if len(self.state.ingoing_leaving) >0:
            leaving = self.state.ingoing_leaving
            self.state.ingoing_leaving = []
            return {self.out1_port: leaving}
        return {}
