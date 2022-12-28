from pypdevs.DEVS import AtomicDEVS

# Define the state of the collector as a structured object
class CollectorState(object):
    def __init__(self):
        # Contains received events and simulation time
        self.current_time = 0.0

        # Contains all info about anchor, confluence_port and the lock
        self.stat1_info = []
        self.stat2_info = []
        self.stat3_info = []
        self.stat4_info = []



class Collector(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Collector")
        self.state = CollectorState()

        # Avg travel time vessel
        self.stat1_in = self.addInPort("stat1_in")
        # Avg waiting time vessel in anchorpoint
        self.stat2_in = self.addInPort("stat2_in")
        # Avg vessels in port
        self.stat3_in = self.addInPort("stat3_in")
        # Vessels in port hourly
        self.stat4_in = self.addInPort("stat4_in")

    def extTransition(self, inputs):
        # Update simulation time
        self.state.current_time += self.elapsed

        # add anchor info to the list
        if self.stat1_in in inputs:
            self.state.stat1_info.append(inputs[self.stat1_in])

        # add cp info to the list
        if self.stat2_in in inputs:
            self.state.stat2_info.append(inputs[self.stat2_in])

        # add anchor info to the list
        if self.stat3_in in inputs:
            self.state.stat3_info.append(inputs[self.stat3_in])

        # add anchor info to the list
        if self.stat4_in in inputs:
            self.state.stat4_info.append(inputs[self.stat4_in])

        return self.state

    # Don't define anything else, as we only store events.
    # Collector has no behaviour of its own.