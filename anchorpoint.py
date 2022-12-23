from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class AnchorpointState:
    def __init__(self):
        self.current_time = 0
        # Keep a queue with vessels waiting
        self.requested = []
        self.waiting = []

        # The vessel that is currently being processed
        self.processing = None
        self.leaving = []
        self.requests = []
        # Time remaining for this event
        self.remaining_time = float("inf")

class AnchorPoint(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "K")
        # Fix the time needed to process a single event
        self.processing_time = 0 # TODO: Geen Processing Time om een ship te genereren, er staat "There are no additional delays in this system."
        self.state = AnchorpointState()

        # Create input and output ports
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")

        # Add the other ports: incoming events and finished event
        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        self.state.current_time += self.elapsed
        if len(self.state.leaving) != 0:
            for vessel in self.state.leaving:
                pass
        if len(self.state.waiting) != 0:
            for vessel in self.state.waiting:
                request = Messages.portEntryRequest(self.state.current_time, vessel.uuid, vessel)
                self.state.requests.append(request)
                self.state.requested.append(vessel)
        return self.state

    def extTransition(self, inputs):
        # Als ship gegenerate is
        if self.in_port in inputs:
            self.state.waiting.append(inputs[self.in_port])

        # Nog ni connected, komt met control. Als ge message terugkrijgt van "uw vessel mag naar daar gaan"
        if self.in_event in inputs:
            permission = inputs[self.in_event]
            vessel = None
            for ship in self.state.requested:
                if ship.uuid == permission.uuid:
                    vessel = ship
                    self.state.requested.remove(vessel)
                    break
            if vessel is not None:
                vessel.destination = permission.destination
                self.state.leaving.append(vessel)

        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        return self.state.remaining_time

    def outputFnc(self):
        # Output the event to the processor
        leaving = self.state.leaving
        self.state.leaving = []
        requests = self.state.requests
        self.state.requests = []
        return {self.out_port: leaving,self.out_event:requests}
