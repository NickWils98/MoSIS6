from pypdevs.DEVS import AtomicDEVS
import numpy as np
import port_events as Messages


# Define the state of the AnchorPoint as a structured object
class DockState:
    def __init__(self, quay_id):
        # Keep track of current time and received vessels
        self.current_time = 0.0
        self.quay_id = quay_id

        self.vessels = {}
        self.leaving = []

        # List of request to send
        self.requests = []


class Dock(AtomicDEVS):
    def __init__(self, quay_id):
        AtomicDEVS.__init__(self)
        self.state = DockState(quay_id)

        self.in_port = self.addInPort("in_port")
        self.out_port = self.addInPort("out_port")

        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        # update all the remaining times
        for vessel in self.state.vessels.keys():
            self.state.vessels[vessel] -= self.timeAdvance()

            #  if the vessel is leaving the dock, add it to the leaving list
            if self.state.vessels[vessel] <= 0:
                self.state.leaving.append(vessel)
                request = Messages.portDepartureRequests(self.state.current_time, vessel.uuid, vessel,
                                                         self.state.quay_id)  # TODO: Current time wordt ni aangepast
                self.state.requests.append(request)

        # delete the arrived vessel
        for vessel in self.state.vessels:
            del self.state.vessels[vessel]

        return self.state

    def extTransition(self, inputs):
        # update all the remaining times
        for vessel in self.state.vessels.keys():
            self.state.vessels[vessel] -= self.elapsed

        # add a new vessel in the waterway if possible
        if len(self.state.vessels) <= 50:
            if self.in_port in inputs:
                vessel = inputs[self.in_port]
                self.state.vessels[vessel] = np.random.normal(36, 12)

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the dock
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.vessels.keys()) > 0:
            self.state.remaining_time = min(self.state.vessels.values())
        return self.state.remaining_time

    def outputFnc(self):
        return_dict = {}

        # Output all the outgoing events
        if len(self.state.requests) > 0:
            requests = self.state.requests.pop()
            return_dict[self.out_event] = requests

        # Output all the ships who left the water canal
        if len(self.state.leaving) > 0:
            leaving = self.state.leaving.pop()
            return_dict[self.out_port] = leaving

        return return_dict
