from pypdevs.DEVS import AtomicDEVS
from port_events import portEntryRequest

# Define the state of the AnchorPoint as a structured object
class AnchorpointState:
    def __init__(self):
        # for statistics
        self.current_time = 0
        self.avg_waiting_time = 0
        self.passed_ships = []
        # Keep a queue with vessels that just came in
        self.waiting = []
        # Keep a queue with vessels that requested to enter the port
        self.requested = []
        # Keep a queue with vessels that are about to leave
        self.leaving = []
        # List of request to send
        self.requests = []


class AnchorPoint(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "K")
        self.state = AnchorpointState()

        # Create input and output ports
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")

        # Add the other ports: incoming events and finished event for communication
        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        # Make a request to ask the control tower for a port
        if len(self.state.waiting) != 0:
            for vessel in self.state.waiting:
                # remove it from the waiting list and make the message
                self.state.waiting.remove(vessel)
                request = portEntryRequest(vessel.vessel_id, self.state.current_time)
                self.state.requests.append(request)
                self.state.requested.append(vessel)
        return self.state

    def extTransition(self, inputs):
        if self.elapsed is not None:
            self.state.current_time += self.elapsed
        # add a vessel to the queue
        if self.in_port in inputs:
            self.state.waiting.append(inputs[self.in_port])

        # When a message is received proces it
        if self.in_event in inputs:
            for permission in inputs[self.in_event]:

                vessel = None
                # Find the vessel
                for ship in self.state.requested:

                    if ship.vessel_id == permission.vessel_id:
                        vessel = ship
                        self.state.requested.remove(vessel)
                        break
                if vessel is not None:
                    vessel.destination = permission.destination
                    self.state.leaving.append(vessel)
                    avg_time = self.state.current_time - permission.current_time
                    self.state.passed_ships.append(avg_time)
                    self.state.avg_waiting_time = sum(self.state.passed_ships)/len(self.state.passed_ships)

        return self.state

    def timeAdvance(self):
        # Don't wait if there is a message or vessel waiting to send else be idle
        if len(self.state.leaving) > 0:
            return 0
        if len(self.state.waiting) > 0:
            return 0
        return float('inf')

    def outputFnc(self):
        return_dict = {}
        if len(self.state.leaving) > 0:
            leaving = self.state.leaving
            return_dict[self.out_port] = leaving
            self.state.leaving = []


        if len(self.state.requests) > 0:
            requests = self.state.requests
            return_dict[self.out_event] = requests
            self.state.requests = []


        return return_dict
