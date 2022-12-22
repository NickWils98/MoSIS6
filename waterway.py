from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.current_time = 0
        # Keep a list with ingoing and outgoing vessels
        # ingoing = vaart de haven in
        # outgoing = vaart de haven uit
        self.ingoing = {}
        self.outgoing = []
        self.distance = distance
        self.ingoing_leaving = []

        # The vessel that is currently being processed
        self.processing = None

        # Time remaining for this event
        self.remaining_time = 0

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
            for vessel in self.state.ingoing:
                self.remaining_time = self.state.distance / vessel.avg_v # dees ist aantal uur da het er over doet


        return self.state

    def extTransition(self, inputs):
        if self.in1_port in inputs:
            remaining_time = self.state.distance / self.state.ingoing[(inputs[self.in1_port])].avg_v
            self.state.ingoing[(inputs[self.in1_port])] = remaining_time


        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        return self.state.remaining_time

    def outputFnc(self):
        # Output the event to the processor
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
