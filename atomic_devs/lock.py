from pypdevs.DEVS import AtomicDEVS

# Hours to seconds
HOUR_TO_SECOND = 1/3600
# delay for a ship to start when leaving a lock
START_DELAY = 30


# Define the state of the Lock as a structured object
class LockState:
    def __init__(self, lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area):
        # self.water_level = "LOW"
        # self.gate1_state = "CLOSED"
        # self.gate2_state = "OPEN"

        self.water_level = 0
        self.gate_sea = 0
        self.gate_dock = 1

        self.lock_id = lock_id
        self.washing_duration = washing_duration
        self.lock_shift_interval = lock_shift_interval
        self.open_close_duration = open_close_duration
        self.surface_area = surface_area
        self.duration = 2 * self.open_close_duration + washing_duration
        self.remaining_time = self.duration
        self.time_open = self.lock_shift_interval - self.duration
        self.time_open_used = self.time_open


        self.remaining_capacity = self.surface_area


        self.waiting_queue_sea = []
        self.waiting_queue_dock = []
        self.in_lock = []
        self.leaving = []
        self.left = None
        self.leaving_bool = False

        # List of request to send
        self.requests = []

        self.current_time = 0
        self.idle_time = 0
        self.empty_itteration = 0
        self.empty = True

class Lock(AtomicDEVS):
    def __init__(self, lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area):
        AtomicDEVS.__init__(self, "Lock")
        self.state = LockState(lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area)

        self.in_port_sea = self.addInPort("in_port_sea")
        self.out_port_dock = self.addOutPort("out_port_dock")

        self.in_port_dock = self.addInPort("in_port_dock")
        self.out_port_sea = self.addOutPort("out_port_sea")

        # Add output port for analytics
        self.out_analytic = self.addOutPort("out_analytic")

    def intTransition(self):
        # ships are leaving takeing 30s each
        self.state.current_time += self.state.remaining_time
        if self.state.leaving_bool:
            # ships are still leaving
            if len(self.state.leaving) > 0:
                # remove the ship
                self.state.left = self.state.leaving.pop(0)
                if self.state.left.vessel_id == 98:
                    pass
                    #print("leave lock at time: ", self.state.current_time)
                # the delay is 30 seconds
                self.state.remaining_time = START_DELAY * HOUR_TO_SECOND
                # the delay of leaving a ship is subtracted from the time the gate stays open
                self.state.time_open_used = self.state.time_open-self.state.remaining_time
            # no ships to leave
            else:
                self.state.leaving_bool = False
                # wait the remaining time the gate stays open
                self.state.remaining_time = self.state.time_open_used
        # No ships are leaving
        else:
            # if the gate closes:
            if self.state.gate_sea == 1 or self.state.gate_dock == 1:
                # close gates
                self.state.gate_sea = 0
                self.state.gate_dock = 0
                # set the remaining time to the duration of the shift
                self.state.remaining_time = self.state.duration
            # if the gate opens
            else:
                #  if the waterlevel changes to HIGH
                if self.state.water_level == 0:
                    # adjust the waterlevel and open gate
                    self.state.water_level = 1
                    self.state.gate_sea = 1
                    # ships can now leave and enter
                    self.state.leaving = self.state.in_lock.copy()
                    self.state.in_lock = []

                    # reset capacity
                    self.state.remaining_capacity = self.state.surface_area
                    for vessel in self.state.waiting_queue_sea[::1].copy():
                        if self.state.remaining_capacity >= vessel.surface_area:
                            # go in lock
                            self.state.in_lock.append(vessel)
                            self.state.waiting_queue_sea.remove(vessel)
                            self.state.remaining_capacity -= vessel.surface_area

                    # if a ship needs to leave
                    if len(self.state.leaving) > 0:
                        self.state.left = self.state.leaving.pop(0)
                        if self.state.left.vessel_id == 98:
                            pass
                            #print("leave lock via sea at time: ", self.state.current_time)
                        self.state.remaining_time = START_DELAY*HOUR_TO_SECOND
                        self.state.time_open_used = self.state.time_open-self.state.remaining_time
                        self.state.leaving_bool = True
                    # no ships need to leave
                    else:
                        self.state.remaining_time = self.state.time_open

                #  if the waterlevel changes to LOW
                else:
                    # adjust the waterlevel and open gate
                    self.state.water_level = 0
                    self.state.gate_dock = 1
                    # ships can now leave and enter
                    self.state.leaving = self.state.in_lock.copy()
                    self.state.in_lock = []

                    # reset capacity
                    self.state.remaining_capacity = self.state.surface_area
                    for vessel in self.state.waiting_queue_dock[::1].copy():
                        if self.state.remaining_capacity >= vessel.surface_area:
                            # go in lock
                            self.state.in_lock.append(vessel)
                            self.state.waiting_queue_dock.remove(vessel)
                            self.state.remaining_capacity -= vessel.surface_area

                    # if a ship needs to leave
                    if len(self.state.leaving) > 0:
                        self.state.left = self.state.leaving.pop(0)
                        if self.state.left.vessel_id == 98:
                            pass
                            #print("leave lock via dock at time: ", self.state.current_time)
                        self.state.remaining_time = START_DELAY * HOUR_TO_SECOND
                        self.state.time_open_used = self.state.time_open - self.state.remaining_time
                        self.state.leaving_bool = True
                    # no ships need to leave
                    else:
                        self.state.remaining_time = self.state.time_open


        return self.state

    def extTransition(self, inputs):
        self.state.current_time += self.elapsed

        # ship at sea gate
        if self.in_port_sea in inputs:
            for vessel in inputs[self.in_port_sea]:
                if vessel.vessel_id == 98:
                    pass
                    #print("enter lock via sea at time", self.state.current_time)
                # gate at sea open and there is capacity
                if self.state.water_level == 1 &\
                        self.state.gate_sea == 1 &\
                        self.state.remaining_capacity >= vessel.surface_area:
                    # go in lock
                    self.state.in_lock.append(vessel)
                # else wait in queue
                else:
                    self.state.waiting_queue_sea.append(vessel)

        if self.in_port_dock in inputs:
            for vessel in inputs[self.in_port_dock]:
                if vessel.vessel_id == 98:
                    pass
                    #print("enter lock via dock at time", self.state.current_time)
                # gate at dock open and there is capacity
                if self.state.water_level == 0 &\
                        self.state.gate_dock == 1 &\
                        self.state.remaining_capacity >= vessel.surface_area:
                    # go in lock
                    self.state.in_lock.append(vessel)

                    self.state.remaining_capacity -= vessel.surface_area
                # else wait in queue
                else:
                    self.state.waiting_queue_dock.append(vessel)
        return self.state

    def timeAdvance(self):
        # return the remaining time that the lock will be open or closed or leaving of a ship
        return self.state.remaining_time

    def outputFnc(self):
        return_dict = {}

        if self.state.left is not None:
            vessel = self.state.left

            # if vessel.vessel_id == 98:
            #     print("confused in lock", self.state.current_time)
            self.state.left = None
            if self.state.gate_dock == 1:
                return_dict[self.out_port_dock] = [vessel]
            else:
                return_dict[self.out_port_sea] = [vessel]

        return return_dict

