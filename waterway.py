from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.current_time = 0
        self.remaining_time = 0

        self.ingoing = {}
        self.ingoing_leaving = []
        self.outgoing = {}
        self.ingoing_leaving = []

        self.distance = distance


class Waterway(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "K")
        # Fix the time needed to process a single event
        self.processing_time = 0
        self.state = WaterwayState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")

        # TODO: Create input and output ports for the other way

    def intTransition(self):
        #self.state.current_time += self.elapsed
        if len(self.state.ingoing) != 0:
            # Update time of each Vessel
            for vessel, remainder in self.state.ingoing:
                new_time = remainder - self.elapsed
                self.state.ingoing[vessel] = new_time

            # Check wether a vessel has arrived or not
            for vessel, remainder in self.state.ingoing:
                if remainder <= 0:
                    self.state.ingoing_leaving.append(vessel) # Als ge meteen popt komt uw loop in de shit

            # delete from the dictionary
            for vessel, remainder in self.state.ingoing:
                if vessel in self.state.ingoing_leaving:
                    del self.state.ingoing[vessel]

        # TODO: Same for outgoing, aka other direction

        return self.state

    def extTransition(self, inputs):
        if self.in1_port in inputs:
            remaining_time = self.state.distance / self.state.ingoing[(inputs[self.in1_port])].avg_v
            self.state.ingoing[(inputs[self.in1_port])] = remaining_time
            self.state.remaining_time = 100

        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
