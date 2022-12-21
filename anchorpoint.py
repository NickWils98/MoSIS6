from pypdevs.DEVS import AtomicDEVS
import port_events as Messages
import queue

# Define the state of the AnchorPoint as a structured object
class AnchorpointState:
    def __init__(self):
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
        self.processing_time = 1.0 # TODO: Weet nog niet hoe we met time gaan werken
        self.state = AnchorpointState()

        # Create output ports
        self.outport = self.addOutPort("out_port") # TODO: Mss vessel name?

        # Add the other ports: incoming events and finished event
        self.in_event = self.addInPort("in_event")
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
        # Several possibilities
        if self.in_finish in inputs:
            # Processing a "finished" event, so mark proc as idle
            self.state.idle_procs.append(inputs[self.in_finish])
            if not self.state.processing and self.state.queue:
                # Process first task in queue
                self.state.processing = self.state.queue.pop(0)
                self.state.remaining_time = self.processing_time
        elif self.in_event in inputs:
            # Processing an incoming event
            if self.state.idle_procs and not self.state.processing:
                # Process when idle processors
                self.state.processing = inputs[self.in_event]
                self.state.remaining_time = self.processing_time
            else:
                # No idle processors, so queue it
                self.state.queue.append(inputs[self.in_event])
        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event (or infinity else)
        return self.state.remaining_time

    def outputFnc(self):
        # Output the event to the processor
        port = self.out_proc[self.state.idle_procs[0]]
        return {port: self.state.processing}