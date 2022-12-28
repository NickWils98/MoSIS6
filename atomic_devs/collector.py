from pypdevs.DEVS import AtomicDEVS

# Define the state of the collector as a structured object
class CollectorState(object):
    def __init__(self):
        # Contains received events and simulation time
        self.current_time = 0.0

        # Contains all info about anchor, confluence_port and the lock
        self.anchor_info = []
        self.cp_info = []
        self.lock_info = []



class Collector(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Collector")
        self.state = CollectorState()

        # Input port for anchorpoint analytics
        self.anchor_event = self.addInPort("anchor_event")
        # Input port for CP analytics
        self.cp_event = self.addInPort("cp_event")
        # Input port for lock analytics
        self.lock_event = self.addInPort("lock_event")

    def extTransition(self, inputs):
        # Update simulation time
        self.state.current_time += self.elapsed

        # add anchor info to the list
        if self.anchor_event in inputs:
            self.state.anchor_info.append(inputs[self.anchor_event])

        # add cp info to the list
        if self.cp_event in inputs:
            self.state.cp_info.append(inputs[self.cp_event])

        # add anchor info to the list
        if self.lock_event in inputs:
            self.state.lock_info.append(inputs[self.lock_event])

        return self.state

    # Don't define anything else, as we only store events.
    # Collector has no behaviour of its own.