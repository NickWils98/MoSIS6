from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class AnchorpointState:
    def __init__(self):
        # Keep track of current time
        self.current_time = 0.0
        # Keep a queue with vessels waiting
        self.queue = []
        # The vessel that is currently being processed
        self.processing = None
        # Time remaining for this event
        self.remaining_time = float("inf")

class AnchorPoint(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "K")
        # Fix the time needed to process a single event
        self.processing_time = 0 # TODO: Geen Processing Time om een ship te genereren, er staat "There are no additional delays in this system."
        self.state = AnchorpointState()

        # Create input and output ports
        self.in_port = self.addInPort("in_port") # TODO: Moeten gegenereerd worden door Generator
        self.outport = self.addOutPort("out_port") # TODO: Mss vessel name?

        # Add the other ports: incoming events and finished event
        self.in_finish = self.addInPort("in_finish")

    def intTransition(self):
        # Is only called when we are outputting an event
        # Pop the first idle processor and clear processing event
        self.state.queue.pop(0)
        if len(self.state.queue) != 0:
            # There are still queued elements, so continue
            self.state.processing = self.state.queue.pop(0)
            self.state.remaining_time = self.processing_time
        else:
            # No events left to process, so become idle
            self.state.processing = None
            self.state.remaining_time = float("inf")
        return self.state

    def extTransition(self, inputs):
        # Update the remaining time of this job
        self.state.remaining_time -= self.elapsed

        # self.state.processing = self.state.queue.pop(0)
        # self.state.remaining_time = self.processing_time

        # TODO: Totally no idea wa die uuid en color moet zijn
        # Messages.portEntryRequest(
        #     timestamp=self.state.current_time,
        #     uuid=0,
        #     color=0,
        #     destination=self.state.processing.destination,
        #     vessel=self.state.processing)

        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        return self.state.remaining_time

    def outputFnc(self):
        # Output the event to the processor
        return {self.outport: self.state.processing}
