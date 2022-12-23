from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class ControlTowerState:
    def __init__(self, dock_count=8):
        self.answers = []
        self.docks = []
        for _ in range(dock_count):
            self.docks.append(50)
        self.dock1 = 50
        self.dock2 = 50
        self.dock3 = 50
        self.dock4 = 50
        self.dock5 = 50
        self.dock6 = 50
        self.dock7 = 50
        self.dock8 = 50
        self.current_time = 0

class ControlTower(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "CT")
        self.state = ControlTowerState()

        # Add the other ports: incoming events and finished event
        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        return self.state

    def extTransition(self, inputs):

        self.state.current_time += self.elapsed
        if self.in_event in inputs:
            request = inputs[self.in_event]
            dock = 0
            for i in range(0, len(self.state.docks)):
                if self.state.docks[i]>=1:
                    self.state.docks[i] -= 1
                    dock = i
                    break
            answer = Messages.portEntryPermission(self.state.current_time, request.uuid, dock, request.vessel)
            self.state.answers.append(answer)

        return self.state

    def timeAdvance(self):
        # Just return the remaining time for this event
        if len(self.state.answers) > 0:
            return 0
        return float('inf')

    def outputFnc(self):
        answer = self.state.answers.pop()
        # self.state.answers = []
        return {self.out_event:answer}
