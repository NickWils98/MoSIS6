from pypdevs.DEVS import AtomicDEVS

# Define the state of the AnchorPoint as a structured object
class SeaState:
    def __init__(self):
        # Keep track of current time and received vessels
        self.current_time = 0.0
        self.vessels = []

class Sea(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "S")
        self.state = SeaState()
        self.in_event = self.addInPort("in_event")

    def extTransition(self, inputs):
        # Update simulation time
        self.state.current_time += self.elapsed

        # Calculate time in queue
        evt = inputs[self.in_event]
        time = self.state.current_time - evt.creation_time - evt.processing_time
        inputs[self.in_event].queueing_time = max(0.0, time)

        # Add incoming event to received events
        self.state.vessels.append(inputs[self.in_event])
        return self.state

