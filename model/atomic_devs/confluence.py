from pypdevs.DEVS import AtomicDEVS


# Define the state of the Confluence as a structured object
class ConfluenceState:
    def __init__(self, map_port, outputs):
        # queue to keep FIFO
        self.queue = []
        self.map_port = map_port

        for i in range(outputs):
            self.queue.append([])

        self.current_time = 0
        self.output_number = outputs

class Confluence(AtomicDEVS):
    def __init__(self, map_port, outputs=3):
        AtomicDEVS.__init__(self, "CF")
        self.state = ConfluenceState(map_port, outputs)

        # Add the input and output port
        self.in_ports = []
        self.out_ports = []
        # one input and one output for each split
        for i in range(outputs):
            self.out_ports.append(self.addOutPort(f"out_port_{i}"))
            self.in_ports.append(self.addInPort(f"in_port_{i}"))

    def intTransition(self):
        return self.state

    def extTransition(self, inputs):
        # Go over all the inputs
        for i in range(self.state.output_number):
            if self.in_ports[i] in inputs:
                # go over all the vessels
                for vessel in inputs[self.in_ports[i]]:
                    destination = vessel.destination
                    # go over all the destinations
                    for ports in range(len(self.state.map_port)):
                        if destination in self.state.map_port[ports]:
                            self.state.queue[ports].append(vessel)
                            break
        return self.state

    def timeAdvance(self):
        # if there is a vessel that needs to leave
        for queue in self.state.queue:
            if len(queue) > 0:
                return 0

        return float('inf')

    def outputFnc(self):
        output_dict = {}
        # let the vessels leave in each split
        for queue_number in range(self.state.output_number):
            if len(self.state.queue[queue_number]) > 0:
                vessel = self.state.queue[queue_number]
                port = self.out_ports[queue_number]
                output_dict[port] = vessel

                self.state.queue[queue_number] = []

        return output_dict
