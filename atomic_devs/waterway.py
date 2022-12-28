from pypdevs.DEVS import AtomicDEVS


# Define the state of the Waterway as a structured object
class WaterwayState:
    def __init__(self, distance):
        # dict: key = vessel in 1 way, value is the remaining time
        self.ingoing = {}
        self.ingoing_leaving = []
        # dict: key = vessel in 1 way, value is the remaining time
        self.outgoing = {}
        self.outgoing_leaving = []

        # distance of the waterway
        self.distance = distance
        self.remaining_time = float('inf')


class Waterway(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "Waterway")
        self.state = WaterwayState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in1_port")
        self.out1_port = self.addOutPort("out1_port")

        # Create input and output ports for the other way
        self.in2_port = self.addInPort("in2_port")
        self.out2_port = self.addOutPort("out2_port")


    def intTransition(self):
        # update all the remaining times
        for vessel in self.state.ingoing.keys():
            self.state.ingoing[vessel] -= self.timeAdvance()

            #  if the vessel is arrived add it to the leaving list
            if self.state.ingoing[vessel] <= 0:
                self.state.ingoing_leaving.append(vessel)

        # delete the arrived vessel
        for vessel in self.state.ingoing_leaving:
            del self.state.ingoing[vessel]

        # update all the remaining times
        for vessel in self.state.outgoing.keys():
            self.state.outgoing[vessel] -= self.timeAdvance()

            #  if the vessel is arrived add it to the leaving list
            if self.state.outgoing[vessel] <= 0:
                self.state.outgoing_leaving.append(vessel)

        # delete the arrived vessel
        for vessel in self.state.outgoing_leaving:
            del self.state.outgoing[vessel]

        return self.state

    def extTransition(self, inputs):
        # update all the remaining times
        for vessel in self.state.ingoing.keys():
            self.state.ingoing[vessel] -= self.elapsed
            if self.state.ingoing[vessel] < 0:
                self.state.ingoing[vessel] = 0

        # add a new vessel in the waterway in 1 way
        if self.in1_port in inputs:
            for vessel in inputs[self.in1_port]:
                # calculate the remaining time
                remaining_time = self.state.distance / vessel.avg_v
                self.state.ingoing[vessel] = remaining_time

        # add a new vessel in the waterway in 1 way
        if self.in2_port in inputs:
            for vessel in inputs[self.in2_port]:
                # calculate the remaining time
                remaining_time = self.state.distance / vessel.avg_v
                self.state.outgoing[vessel] = remaining_time

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the waterway
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.ingoing.keys()) > 0:
            self.state.remaining_time = min(self.state.ingoing.values())

        # find the shortest time between the vessels
        if len(self.state.outgoing.keys()) > 0:
            remaining_outgoing = min(self.state.outgoing.values())
            self.state.remaining_time = min(self.state.remaining_time, remaining_outgoing)

        if len(self.state.ingoing_leaving) > 0:
            self.state.remaining_time = 0

        if len(self.state.outgoing_leaving) > 0:
            self.state.remaining_time = 0
        return self.state.remaining_time


    def outputFnc(self):
        return_dict = {}
        # Output all the ships who left the water canal
        if len(self.state.ingoing_leaving) > 0:
            leaving = self.state.ingoing_leaving
            return_dict[self.out1_port] = leaving
            self.state.ingoing_leaving = []

        # Output all the ships who left the water canal
        if len(self.state.outgoing_leaving) > 0:
            leaving = self.state.outgoing_leaving
            return_dict[self.out2_port] = leaving
            self.state.outgoing_leaving = []

        return return_dict
