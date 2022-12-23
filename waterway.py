from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.current_time = 0
        self.remaining_time = 0
        self.count =0

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


    def intTransition(self):

        #self.state.current_time += self.elapsed
        if len(self.state.ingoing) != 0:

            for vessel in self.state.ingoing.keys():
                if self.elapsed is not None:
                    self.state.ingoing[vessel] -= self.elapsed
                if self.state.ingoing[vessel]  <=0:
                    self.state.ingoing_leaving.append(vessel) # Als ge meteen popt komt uw loop in de shit

            # delete from the dictionary
            for vessel in self.state.ingoing_leaving:
                del self.state.ingoing[vessel]



        # TODO: Same for outgoing, aka other direction

        return self.state

    def extTransition(self, inputs):
        for vessel in self.state.ingoing.keys():
            self.state.ingoing[vessel] -= self.elapsed
        if self.in1_port in inputs:
            vessel = inputs[self.in1_port]
            remaining_time = self.state.distance / vessel.avg_v
            self.state.ingoing[vessel] = remaining_time
            if remaining_time< self.state.remaining_time:
                self.state.remaining_time = remaining_time
        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        self.state.remaining_time = float("inf")
        if len(self.state.ingoing.keys())>0:
            self.state.remaining_time = min(self.state.ingoing.values())
        print(self.state.remaining_time)
        self.state.count+=1
        print(self.state.count)
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
