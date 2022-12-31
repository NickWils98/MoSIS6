from pypdevs.DEVS import AtomicDEVS
from messages_events.port_events import portEntryPermission

# Define the state of the Control Tower as a structured object
class ControlTowerState:
    def __init__(self, dock_count=8):
        # list for responses
        self.answers = []
        # list of all the docks with their places available
        self.docks = []
        for _ in range(dock_count):
            self.docks.append(50)
        # list of request in FIFO
        self.queue = []
        # there is a place free in a dock
        self.place_free = True

class ControlTower(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "CT")
        self.state = ControlTowerState()

        # Add the other ports: incoming events and finished event
        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")
        self.free_event = self.addInPort("free_event")

    def intTransition(self):
        #  if there is a request pending and place in a dock
        if len(self.state.queue) > 0 and self.state.place_free == True:
            request = self.state.queue.pop(0)
            quay_id = 0
            # find a free dock
            for i in range(0, len(self.state.docks)):
                if self.state.docks[i] >= 1:
                    self.state.docks[i] -= 1
                    quay_id = i + 1
                    break
            # if no dock was free put it back first
            if quay_id == 0:
                self.state.queue.insert(0,request)
                self.state.place_free = False
            # make a response
            else:
                answer = portEntryPermission(request.vessel_id, quay_id, request.current_time)
                self.state.answers.append(answer)
        return self.state

    def extTransition(self, inputs):
        # Check if there are ships who sent message they want to enter the dock
        if self.in_event in inputs:
            for request in inputs[self.in_event]:
                #  check if there is an availability
                quay_id = 0
                for i in range(0, len(self.state.docks)):
                    if self.state.docks[i]>=1:
                        self.state.docks[i] -= 1
                        quay_id = i+1
                        break
                if quay_id == 0:
                    # if not put it in the queue
                    self.state.queue.append(request)
                    self.state.place_free = False
                else:
                    #  if there is make a response
                    answer = portEntryPermission(request.vessel_id, quay_id, request.current_time)
                    self.state.answers.append(answer)

        # Check if there are ships who sent message they left the dock
        if self.free_event in inputs:
            for return_update in inputs[self.free_event]:
                quay_id = return_update.quay_id - 1
                self.state.docks[quay_id] += 1
                self.state.place_free = True
        return self.state

    def timeAdvance(self):
        # if an answer is ready don't wait else be idle waiting
        if len(self.state.answers) > 0:
            return 0
        if len(self.state.queue)>0 and self.state.place_free == True:
            return 0
        return float('inf')

    def outputFnc(self):
        return_dict = {}
        if len(self.state.answers) > 0:
            answer = self.state.answers
            return_dict[self.out_event] = answer
            self.state.answers = []
        return return_dict

