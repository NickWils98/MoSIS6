import numpy as np
from pypdevs.DEVS import AtomicDEVS
import math


# Define the state of the ConfluencePort as a structured object
class ConfluencePortState:
    def __init__(self):
        # queue to keep FIFO
        self.queue = []
        self.map_port = [["S"], [1, 2], [3, 4, 5, 6, 7, 8]]
        for i in range(3):
            self.queue.append([])
        self.current_time = 0
        self.output_number = 3

        # Analytics
        # amount of vessels in the port
        self.ships_in_port = 0
        # average time a vessel is in the port
        self.avg_time = 0
        # the times the vessels spend in the port
        self.ships_time = []
        # amount of ships in the port
        self.ships_average = [0]
        # time that the previous amount of ship were in the port
        self.ships_average_weight = []
        # is this an hourly update?
        self.hour_update = False
        # time remaining until the hourly update
        self.remaining_time = 0

class ConfluencePort(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "CP")
        self.state = ConfluencePortState()

        # Add the input and output port
        self.in_ports = []
        self.out_ports = []

        for i in range(3):
            self.out_ports.append(self.addOutPort(f"out_port_{i}"))
            self.in_ports.append(self.addInPort(f"in_port_{i}"))

        # Add output ports for statistics
        self.stat1_out = self.addOutPort("stat1_out")
        self.stat3_out = self.addOutPort("stat3_out")
        self.stat4_out = self.addOutPort("stat4_out")

    def intTransition(self):
        # keep time
        self.state.current_time += self.state.remaining_time
        self.state.remaining_time = 0
        return self.state

    def extTransition(self, inputs):
        # keep time
        self.state.current_time += self.elapsed
        # Go over all the inputs
        for i in range(self.state.output_number):
            if self.in_ports[i] in inputs:
                # go over all the vessels
                for vessel in inputs[self.in_ports[i]]:
                    # if the vessel comes from the ancherpoint
                    if i == 0:
                        # keep the time the vessel entered the port
                        vessel.enter_port = self.state.current_time
                        self.state.ships_in_port += 1
                    # if the vessel comes from the port
                    else:
                        # if the vessel leaves the port
                        if vessel.destination == "S":
                            # calculate the average time
                            avg_time = self.state.current_time - vessel.enter_port
                            self.state.ships_time.append(avg_time)
                            self.state.avg_time = sum(self.state.ships_time)/len(self.state.ships_time)
                            self.state.ships_in_port -= 1

                    # Analytics 3 : keep the time sinds the previous update in shipcount in port
                    self.state.ships_average.append(self.state.ships_in_port)
                    if len(self.state.ships_average_weight)>0:
                        self.state.ships_average_weight.append(self.state.current_time-self.state.ships_average_weight[-1])
                    else:
                        self.state.ships_average_weight.append(self.state.current_time)

                    # Set correct destination
                    destination = vessel.destination
                    for ports in range(len(self.state.map_port)):
                        if destination in self.state.map_port[ports]:
                            self.state.queue[ports].append(vessel)
                            break
        return self.state

    def timeAdvance(self):
        # update every hour
        self.state.remaining_time = math.floor(self.state.current_time)+1-self.state.current_time
        self.state.hour_update =True
        # if a ship is in the confluence there is no delay
        for queue in self.state.queue:
            if len(queue) > 0:
                self.state.hour_update = False
                self.state.remaining_time = 0
        return self.state.remaining_time

    def outputFnc(self):
        output_dict = {}
        # let the vessels leave in each split
        for queue_number in range(self.state.output_number):
            if len(self.state.queue[queue_number]) > 0:
                vessel = self.state.queue[queue_number]
                port = self.out_ports[queue_number]
                output_dict[port] = vessel
                self.state.queue[queue_number] = []

        # Statistics 1 output
        if self.state.avg_time > 0:
            output_dict[self.stat1_out] = self.state.avg_time

        # Statistics 3 output
        if len(self.state.ships_average_weight) > 0:
            output_dict[self.stat3_out] = np.average(self.state.ships_average[:-1], weights=self.state.ships_average_weight)
        else:
            output_dict[self.stat3_out] = 0

        # Statistics 4 output
        if self.state.hour_update:
            output_dict[self.stat4_out] = np.average(self.state.ships_in_port)

        return output_dict
