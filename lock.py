from pypdevs.DEVS import AtomicDEVS
import numpy as np
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class LockState:
    def __init__(self, lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area):
        # Keep track of current time and received vessels
        self.current_time = float("inf")

        self.water_level = "LOW"
        self.gate1_state = "CLOSED"
        self.gate2_state = "OPEN"

        self.lock_id = lock_id
        self.washing_duration = washing_duration
        self.lock_shift_interval = lock_shift_interval
        self.open_close_duration = open_close_duration
        self.surface_area = surface_area

        self.remaining_capacity = self.surface_area


        self.waiting_queue = []
        self.in_lock = {}
        self.leaving = []

        # List of request to send
        self.requests = []

class Lock(AtomicDEVS):
    def __init__(self, lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area):
        AtomicDEVS.__init__(self)
        self.state = LockState(lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area)

        self.in_port_sea = self.addInPort("in_port")
        self.out_port_dock = self.addInPort("out_port")

        self.in_port_dock = self.addInPort("in_port")
        self.out_port_sea = self.addInPort("out_port")

        # TODO: Ports voor de andere direction

    def intTransition(self):
        # update all the remaining times
        for vessel in self.state.in_lock.keys():
            self.state.in_lock[vessel] -= self.timeAdvance()

            #  if the vessel is arrived add it to the leaving list
            if self.state.in_lock[vessel] <= 0:
                self.state.leaving.append(vessel)

        return self.state

    def extTransition(self, inputs):
        # update all the remaining times
        for vessel in self.state.in_lock:
            self.state.in_lock[vessel] -= self.elapsed

        if self.in_port_sea in inputs:
            vessel = inputs[self.in_port_sea]
            duration = self.state.washing_duration

            # Als water level hetzelfde is en de poort open -> ships can enter
            if self.state.water_level == "HIGH" and self.state.gate1_state == "OPEN":
                # Check of het ship past
                if vessel.surface_area <= self.state.remaining_capacity:
                    self.state.remaining_capacity -= vessel.surface_area
                    duration += self.state.open_close_duration * 2 + len(self.state.in_lock)*30
                    self.state.in_lock[vessel] = duration

                    if self.state.water_level == "LOW" and self.state.gate1_state == "OPEN":
                        pass

            # Als water level [sea ~ Lock] hetzelfde is maar poort toe -> washing gaat beginnen. Voeg toe aan wait queue
            elif self.state.water_level == "LOW" and self.state.gate1_state == "CLOSED":
                self.state.waiting_queue.append(vessel)

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the dock
        self.state.remaining_time = float("inf")

        # find the shortest time between the vessels
        if len(self.state.in_lock.keys()) > 0:
            self.state.remaining_time = min(self.state.in_lock.values())
        return self.state.remaining_time

    def outputFnc(self):
        return_dict = {}

        # Output all the outgoing boats one side
        if len(self.state.requests) > 0:
            requests = self.state.requests.pop()
            return_dict[self.out_event] = requests

        # Output all the outgoing boats other side
        if len(self.state.leaving) > 0:
            leaving = self.state.leaving.pop()
            return_dict[self.out_port] = leaving

        return return_dict

