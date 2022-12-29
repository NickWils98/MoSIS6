from pypdevs.DEVS import AtomicDEVS
import math
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
        self.start_empty = 0
        self.hourly_remainig_cappacity = -1
        self.hour_update =True

        self.hour_remaining = 1
        self.closegate = False
class Lock(AtomicDEVS):
    def __init__(self, lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area):
        AtomicDEVS.__init__(self, "Lock")
        self.state = LockState(lock_id, washing_duration, lock_shift_interval, open_close_duration, surface_area)

        self.in_port_sea = self.addInPort("in_port_sea")
        self.out_port_dock = self.addOutPort("out_port_dock")

        self.in_port_dock = self.addInPort("in_port_dock")
        self.out_port_sea = self.addOutPort("out_port_sea")

        # Add output port for analytics
        self.stat5_out = self.addOutPort("stat5_out")
        self.stat6_out = self.addOutPort("stat6_out")
        self.stat7_out = self.addOutPort("stat7_out")


    def intTransition(self):
        if self.state.hour_update:
            self.state.hour_update = False
            self.state.current_time += self.state.hour_remaining
            self.state.remaining_time -= self.state.hour_remaining

            if self.state.time_open_used != -1:
                self.state.time_open_used -= self.state.hour_remaining
            return self.state
        # else:
        #     self.state.hour_remaining -= self.state.remaining_time

        # ships are leaving takeing 30s each
        self.state.current_time += self.state.remaining_time
        if self.state.leaving_bool:
            self.state.time_open_used -= self.state.remaining_time
            # ships are still leaving
            if len(self.state.leaving) > 0:
                # remove the ship
                self.state.left = self.state.leaving.pop(0)
                # the delay is 30 seconds
                self.state.remaining_time = START_DELAY * HOUR_TO_SECOND
                # the delay of leaving a ship is subtracted from the time the gate stays open
            # no ships to leave
            else:
                self.state.leaving_bool = False
                # wait the remaining time the gate stays open
                self.state.remaining_time = self.state.time_open_used
                self.state.time_open_used=-1
        # No ships are leaving
        else:
            # if the gate closes:
            if self.state.gate_sea == 1 or self.state.gate_dock == 1:
                print(self.state.current_time)
                if self.state.hourly_remainig_cappacity == -1:
                    self.state.hourly_remainig_cappacity =0
                self.state.hourly_remainig_cappacity += self.state.remaining_capacity
                if len(self.state.in_lock)==0:
                    # analytic 6
                    self.state.empty_itteration += 1
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
                        self.state.remaining_time = START_DELAY*HOUR_TO_SECOND
                        self.state.time_open_used = self.state.time_open
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
                        self.state.remaining_time = START_DELAY * HOUR_TO_SECOND
                        self.state.time_open_used = self.state.time_open
                        self.state.leaving_bool = True
                    # no ships need to leave
                    else:
                        self.state.remaining_time = self.state.time_open


        return self.state

    def extTransition(self, inputs):
        if self.state.time_open_used != -1:
            self.state.time_open_used -= self.elapsed
        self.state.current_time += self.elapsed
        self.state.remaining_time -= self.elapsed

        # ship at sea gate
        if self.in_port_sea in inputs:
            for vessel in inputs[self.in_port_sea]:
                self.state.empty = False

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
                if self.state.empty:
                    self.state.idle_time += self.state.current_time -  self.state.start_empty
                    self.state.start_empty = 0
                self.state.empty = False

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
        self.state.hour_update = False

        self.state.hour_remaining = math.floor(self.state.current_time)+1-self.state.current_time

        # return the remaining time that the lock will be open or closed or leaving of a ship
        if self.state.remaining_time < self.state.hour_remaining:

            return self.state.remaining_time
        else:
            self.state.hour_update = True
            return self.state.hour_remaining

    def outputFnc(self):
        return_dict = {}


        if self.state.empty:
            self.state.idle_time += self.state.current_time - self.state.start_empty
            self.state.start_empty = self.state.current_time
        if self.state.left is not None:
            in_lock_bool = len(self.state.in_lock) == 0
            leaving_bool = len(self.state.leaving) == 0
            waiting_dock_bool = len(self.state.waiting_queue_dock) == 0
            waiting_sea_bool = len(self.state.waiting_queue_sea) == 0
            if in_lock_bool and leaving_bool and waiting_sea_bool and waiting_dock_bool and not self.state.empty:
                self.state.start_empty = self.state.current_time
                self.state.empty = True
            vessel = self.state.left


            self.state.left = None
            if self.state.gate_dock == 1:
                return_dict[self.out_port_dock] = [vessel]
            else:
                return_dict[self.out_port_sea] = [vessel]

            # Statistic ports connect
        if self.state.current_time > 0:
            return_dict[self.stat5_out] = self.state.idle_time / (self.state.current_time)
        else:
            return_dict[self.stat5_out] = 0

        return_dict[self.stat6_out] = self.state.empty_itteration

        if self.state.hour_update:
            remaining_capacity = self.state.hourly_remainig_cappacity
            self.state.hourly_remainig_cappacity = -1
            return_dict[self.stat7_out] = remaining_capacity

        return return_dict

