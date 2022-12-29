from pypdevs.DEVS import AtomicDEVS

# Define the state of the Sea as a structured object
class SeaState:
    def __init__(self):
        # Keep track of current time and received vessels
        self.current_time = 0.0
        self.entered = []
        self.left_counter = 0


class Sea(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "S")
        self.state = SeaState()
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")

    def intTransition(self):
        self.state.entered.pop(0)

        return self.state

    def extTransition(self, inputs):
        # Update simulation time
        self.state.current_time += self.elapsed

        # add vessel to leaving list
        if self.in_port in inputs:

            self.state.entered.append(inputs[self.in_port])

        return self.state

    def timeAdvance(self):
        # Don't wait if there is a message or vessel waiting to send else be idle
        if len(self.state.entered) > 0:
            return 0
        return float('inf')

    def outputFnc(self):
        self.state.left_counter += 1
        return_dict = {self.out_port: self.state.left_counter}

        return return_dict

