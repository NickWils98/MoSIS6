from pypdevs.DEVS import AtomicDEVS
import numpy as np
from messages_events import port_events as Messages


# Define the state of the AnchorPoint as a structured object
class DockState:
    def __init__(self, quay_id):
        # Keep track of current time and received vessels
        self.remaining_time = float('inf')
        self.quay_id = quay_id

        self.vessels = {}
        self.leaving = []

        # List of request to send
        self.requests = []
        self.activate = False
        self.counter = 0
        self.current_time = 0


class Dock(AtomicDEVS):
    def __init__(self, quay_id):
        AtomicDEVS.__init__(self, "Dock")
        self.state = DockState(quay_id)

        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")

        self.in_event = self.addInPort("in_event")
        self.out_event = self.addOutPort("out_event")

    def intTransition(self):
        # update all the remaining times
        self.state.current_time+= self.state.remaining_time
        for vessel in self.state.vessels.keys():
            self.state.vessels[vessel] -= self.state.remaining_time

            #  if the vessel is leaving the dock, add it to the leaving list
            if self.state.vessels[vessel] <= 0:
                request = Messages.portDepartureRequests(vessel.vessel_id, vessel.destination)
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
        # add a new vessel in the waterway if possible

        if self.in_port in inputs:
            for vessel in inputs[self.in_port]:
                # self.state.counter += 1
                # print(f"dock {self.state.quay_id}, counter= {self.state.counter}")
                # if self.state.activate == False:
                #     self.state.activate =True
                #     print(f"vessel= {vessel.destination}, dock = {self.state.quay_id}, same = {self.state.quay_id == vessel.destination}")
                wait_time = np.random.normal(36,12)
                if vessel.vessel_id ==98:
                    print("time in dock",vessel.vessel_id, wait_time, self.state.current_time)
                if wait_time < 6:
                    wait_time = 6
                self.state.vessels[vessel] = wait_time

        if len(self.state.vessels) > 50:
            print("ERROR")

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the dock
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.vessels.keys()) > 0:
            self.state.remaining_time = min(self.state.vessels.values())

        if len(self.state.requests) > 0 or len(self.state.leaving) > 0:
            self.state.remaining_time = 0
        if self.state.remaining_time <0:
            print("aiaiaiaiaiaiai")
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
