from pypdevs.DEVS import AtomicDEVS
import numpy as np

# Define the state of the AnchorPoint as a structured object
class DockState:
    def __init__(self):
        # Keep track of current time and received vessels
        self.current_time = 0.0
        self.vessels = []
        self.id = 0

class Dock(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "S")
        self.state = DockState()
        self.in_event = self.addInPort("in_event")

    def intTransition(self):
        self.state.current_time += self.timeAdvance()

        hour = math.floor(self.state.current_time) % 24
        self.state.remaining = np.random.exponential(scale=1 / self.state.ships_hours[hour])
        return self.state

    def extTransition(self, inputs):
        time_at_dock = np.random.normal(36, 12)

        # Update simulation time
        self.state.current_time += self.elapsed

        # Calculate time in queue
        evt = inputs[self.in_event]
        time = self.state.current_time - evt.creation_time - evt.processing_time
        inputs[self.in_event].queueing_time = max(0.0, time)

        # Add incoming event to received events
        self.state.vessels.append(inputs[self.in_event])
        return self.state

