import numpy as np
from pypdevs.DEVS import AtomicDEVS
import math


# Define the state of the Confluence as a structured object
class ConfluencePortState:
    def __init__(self):
        self.queue = []
        self.map_port = [["S"], [1, 2], [3, 4, 5, 6, 7, 8]]
        for i in range(3):
            self.queue.append([])
        self.current_time = 0
        self.output_number = 3

        self.ships_in_port = 0
        self.avg_time = 0
        self.ships_time = []
        self.ships_average = [0]
        self.ships_average_weight = []
        self.last_hour = -1
        self.ships_memory_hour = [[], [], [], [], [], [], [], [], [], [], [], [],
                             [], [], [], [], [], [], [], [], [], [], [], []]
        self.hour_update = False
        self.count = 1
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
        self.state.current_time += self.state.remaining_time
        if self.state.hour_update:
            pass
            # ananlitic 4
            # print(self.state.ships_in_port, self.state.current_time)
        self.state.remaining_time = self.state.count-math.floor(self.state.current_time)
        return self.state

    def extTransition(self, inputs):
        self.state.current_time += self.elapsed

        for i in range(self.state.output_number):
            if self.in_ports[i] in inputs:
                for vessel in inputs[self.in_ports[i]]:
                    if i == 0:
                        vessel.enter_port = self.state.current_time
                        self.state.ships_in_port += 1
                    else:
                        if vessel.destination == "S":
                            avg_time = self.state.current_time - vessel.enter_port
                            self.state.ships_time.append(avg_time)
                            self.state.avg_time = sum(self.state.ships_time)/len(self.state.ships_time)
                            self.state.ships_in_port -= 1

                    # Analytics 3

                    self.state.ships_average.append(self.state.ships_in_port)
                    if len(self.state.ships_average_weight)>0:

                        self.state.ships_average_weight.append(self.state.current_time-self.state.ships_average_weight[-1])
                    else:

                        self.state.ships_average_weight.append(self.state.current_time)


                    #print("3: Average number of vessels in port: ",np.average(self.state.ships_average[:-1], weights=self.state.ships_average_weight))

                    # Analytics 4
                    hour = math.floor(self.state.current_time) % 24
                    if self.state.last_hour == -1:
                        self.state.last_hour = hour
                    if self.state.last_hour != hour:
                        # print(
                        #     f"4: Total number of vessels in the port at hour {self.state.last_hour}: "
                        #     f"{sum(self.state.ships_memory_hour[self.state.last_hour]) / len(self.state.ships_memory_hour[self.state.last_hour])}")
                        self.state.ships_memory_hour[self.state.last_hour] = []
                        self.state.last_hour = hour

                    self.state.ships_memory_hour[hour].append(self.state.ships_in_port)

                    destination = vessel.destination
                    for ports in range(len(self.state.map_port)):
                        if destination in self.state.map_port[ports]:
                            self.state.queue[ports].append(vessel)
                            break
        return self.state

    def timeAdvance(self):
        self.state.remaining_time = math.floor(self.state.current_time)+1-self.state.current_time
        self.state.hour_update =True
        for queue in self.state.queue:
            if len(queue) > 0:
                self.state.hour_update = False
                self.state.remaining_time = 0
        return self.state.remaining_time

    def outputFnc(self):
        output_dict = {}
        for queue_number in range(self.state.output_number):
            if len(self.state.queue[queue_number]) > 0:
                vessel = self.state.queue[queue_number]
                port = self.out_ports[queue_number]
                output_dict[port] = vessel
                self.state.queue[queue_number] = []

        output_dict[self.stat1_out] = 0

        if len(self.state.ships_average_weight) > 0:
            print("HAHAHAHAHAHAHAHAHAHA : ", np.average(self.state.ships_average[:-1], weights=self.state.ships_average_weight))
            output_dict[self.stat3_out] = np.average(self.state.ships_average[:-1], weights=self.state.ships_average_weight)
        else:
            print("hi")
            output_dict[self.stat3_out] = 0

        if self.state.hour_update:
            output_dict[self.stat4_out] = np.average(self.state.ships_in_port)

        return output_dict
