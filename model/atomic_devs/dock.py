from pypdevs.DEVS import AtomicDEVS
import numpy as np
from messages_events import port_events


# Define the state of the AnchorPoint as a structured object
class DockState:
    def __init__(self, quay_id, det_bool=False):
        # Keep track of current time and received vessels
        self.remaining_time = float('inf')
        self.quay_id = quay_id
        # does it need to be deterministic
        self.det_bool = det_bool

        # vessels in the dock with remaining time as value
        self.vessels = {}
        self.leaving = []

        # List of request to send
        self.requests = []
        self.current_time = 0


class Dock(AtomicDEVS):
    def __init__(self, quay_id, det_bool=False):
        AtomicDEVS.__init__(self, "Dock")
        self.state = DockState(quay_id, det_bool)
        # in and out port for vessels
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")
        # in and out ports for messeges
        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        # update all the remaining times
        self.state.current_time += self.state.remaining_time
        for vessel in self.state.vessels.keys():
            self.state.vessels[vessel] -= self.state.remaining_time

            #  if the vessel is leaving the dock, add it to the leaving list
            if self.state.vessels[vessel] <= 0:
                request = port_events.portDepartureRequests(vessel.vessel_id, vessel.destination)
                vessel.destination = "S"
                self.state.leaving.append(vessel)
                self.state.requests.append(request)

        # delete the arrived vessel
        for vessel in self.state.leaving:
            del self.state.vessels[vessel]

        return self.state

    def extTransition(self, inputs):
        # update all the remaining times

        self.state.current_time+= self.elapsed
        for vessel in self.state.vessels.keys():
            self.state.vessels[vessel] -= self.elapsed

        # add a new vessel in dock if possible
        if self.in_port in inputs:
            for vessel in inputs[self.in_port]:
                #  if detereministic: set wait_time on average (36)
                if self.state.det_bool:
                    wait_time = 36
                else:
                    wait_time = np.random.normal(36,12)
                # make sure the minimal waiting time is 0
                if wait_time < 6:
                    wait_time = 6
                self.state.vessels[vessel] = wait_time

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the dock
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.vessels.keys()) > 0:
            self.state.remaining_time = min(self.state.vessels.values())

        # if a vessels needs to leave: no delay
        if len(self.state.requests) > 0 or len(self.state.leaving) > 0:
            self.state.remaining_time = 0

        return self.state.remaining_time

    def outputFnc(self):
        return_dict = {}

        # Output all the outgoing events
        if len(self.state.requests) > 0:
            requests = self.state.requests
            return_dict[self.out_event] = requests
            self.state.requests = []

        # Output all the ships who left the water canal
        if len(self.state.leaving) > 0:
            leaving = self.state.leaving
            return_dict[self.out_port] = leaving
            self.state.leaving = []

        return return_dict
