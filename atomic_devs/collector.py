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
        self.stat5A_info = []
        self.stat5B_info = []
        self.stat5C_info = []
        self.stat6A_info = []
        self.stat6B_info = []
        self.stat6C_info = []
        self.stat7A_info = []
        self.stat7B_info = []
        self.stat7C_info = []


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

        # Avg idle time for each Lock
        self.stat5A_in = self.addInPort("stat5A_in")
        self.stat5B_in = self.addInPort("stat5B_in")
        self.stat5C_in = self.addInPort("stat5C_in")

        # Lock changed state without containing ships
        self.stat6A_in = self.addInPort("stat6A_in")
        self.stat6B_in = self.addInPort("stat6B_in")
        self.stat6C_in = self.addInPort("stat6C_in")

        # Avg vessels in port
        self.stat7A_in = self.addInPort("stat7A_in")
        self.stat7B_in = self.addInPort("stat7B_in")
        self.stat7C_in = self.addInPort("stat7C_in")

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

        # add anchor info to the list
        if self.stat5A_in in inputs:
            self.state.stat5A_info.append(inputs[self.stat5A_in])
        if self.stat5B_in in inputs:
            self.state.stat5B_info.append(inputs[self.stat5B_in])
        if self.stat5C_in in inputs:
            self.state.stat5C_info.append(inputs[self.stat5C_in])

        # add cp info to the list
        if self.stat6A_in in inputs:
            self.state.stat6A_info.append(inputs[self.stat6A_in])
        if self.stat6B_in in inputs:
            self.state.stat6B_info.append(inputs[self.stat6B_in])
        if self.stat6C_in in inputs:
            self.state.stat6C_info.append(inputs[self.stat6C_in])

        # add anchor info to the list
        if self.stat7A_in in inputs:
            self.state.stat7A_info.append(inputs[self.stat7A_in])
        if self.stat7B_in in inputs:
            self.state.stat7B_info.append(inputs[self.stat7B_in])
        if self.stat7C_in in inputs:
            self.state.stat7C_info.append(inputs[self.stat7C_in])

        return self.state

    # Don't define anything else, as we only store events.
    # Collector has no behaviour of its own.