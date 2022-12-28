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

        self.last_hour = -1
        self.ships_memory_hour = [[], [], [], [], [], [], [], [], [], [], [], [],
                             [], [], [], [], [], [], [], [], [], [], [], []]

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

    def intTransition(self):
        return self.state

    def extTransition(self, inputs):
        if self.elapsed is not None:
            self.state.current_time += self.elapsed

        for i in range(self.state.output_number):
            if self.in_ports[i] in inputs:
                for vessel in inputs[self.in_ports[i]]:
                    if i == 0:
                        vessel.enter_port = self.state.current_time
                        self.state.ships_in_port += 1
                    else:
                        avg_time = self.state.current_time - vessel.enter_port
                        self.state.ships_time.append(avg_time)
                        self.state.avg_time = sum(self.state.ships_time)/len(self.state.ships_time)
                        # if vessel.vessel_id == 98:
                            # print(f"avg_time = {avg_time}, current time = {self.state.current_time} and start_time for {vessel.vessel_id} = {vessel.enter_port}")
                        self.state.ships_in_port -= 1

                    hour = math.floor(self.state.current_time) % 24

                    if self.state.last_hour == -1:
                        self.state.last_hour = hour
                    if self.state.last_hour != hour:
                        print(
                            f"average number of vessels in the port at hour {self.state.last_hour} is "
                            f"{sum(self.state.ships_memory_hour[self.state.last_hour]) / len(self.state.ships_memory_hour[self.state.last_hour])}")
                        self.state.ships_memory_hour[self.state.last_hour] = []
                        self.state.last_hour = hour

                    self.state.ships_memory_hour[hour].append(self.state.ships_in_port)


                    #print(f"average number of vessels in the port at time {self.state.current_time} is {sum(self.state.ships_memory) / len(self.state.ships_memory)}")

                    destination = vessel.destination
                    for ports in range(len(self.state.map_port)):
                        if destination in self.state.map_port[ports]:
                            self.state.queue[ports].append(vessel)
                            break
        return self.state

    def timeAdvance(self):
        for queue in self.state.queue:
            if len(queue) > 0:
                return 0
        return float('inf')

    def outputFnc(self):
        output_dict = {}
        for queue_number in range(self.state.output_number):
            if len(self.state.queue[queue_number]) > 0:
                vessel = self.state.queue[queue_number]
                port = self.out_ports[queue_number]
                output_dict[port] = vessel
                self.state.queue[queue_number] = []
        return output_dict
