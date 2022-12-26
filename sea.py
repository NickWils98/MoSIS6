from pypdevs.DEVS import AtomicDEVS

# Define the state of the Sea as a structured object
class SeaState:
    def __init__(self):
        # Keep track of current time and received vessels
        self.current_time = 0.0
        self.vessels = []

class Sea(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "S")
        self.state = SeaState()
        self.in_port = self.addInPort("in_port")

    def extTransition(self, inputs):

        if self.in_port in inputs:
            for vessel in inputs[self.in_port]:
                print(vessel.vessel_id, vessel.type)
        return self.state

