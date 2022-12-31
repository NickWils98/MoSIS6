from pypdevs.DEVS import AtomicDEVS


# Define the state of the Canal as a structured object
class CanalState:
    def __init__(self, distance):
        # remaining time for closest vessel
        self.remaining_time = float('inf')

        # list of vessels in canal in order from first to last
        self.ingoing = [] # list of [vessel, remaining time]
        self.ingoing_leaving = [] # list van vessels leaving
        # list of vessels in canal in order from first to last other direction
        self.outgoing = []
        self.outgoing_leaving = []

        self.distance = distance


class Canal(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "Canal")
        self.state = CanalState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")

        # Create input and output ports for the other way
        self.in2_port = self.addInPort("in_port")
        self.out2_port = self.addOutPort("out_port")

    def intTransition(self):
        # update all the remaining times

        for i in range(len(self.state.ingoing)):
            self.state.ingoing[i][1] -= self.state.remaining_time
            #  if the vessel is arrived add it to the leaving list

            if self.state.ingoing[i][1] <= 0:
                self.state.ingoing_leaving.append(self.state.ingoing[i][0])

        # delete from the list
        for vessel in self.state.ingoing_leaving:
            self.state.ingoing.pop(0)

        # update all the remaining times for the other directions
        for i in range(len(self.state.outgoing)):
            self.state.outgoing[i][1] -= self.state.remaining_time
            #  if the vessel is arrived add it to the leaving list

            if self.state.outgoing[i][1] <= 0:
                self.state.outgoing_leaving.append(self.state.outgoing[i][0])

        # delete from the list
        for _ in self.state.outgoing_leaving:
            self.state.outgoing.pop(0)

        return self.state

    def extTransition(self, inputs):
        # Update times of ingoing vessels
        for i in range(len(self.state.ingoing)):
            self.state.ingoing[i][1] -= self.elapsed

            if self.state.ingoing[i][1] < 0:
                self.state.ingoing[i][1] = 0

        # Update times of outgoing vessels
        for i in range(len(self.state.outgoing)):
            self.state.outgoing[i][1] -= self.elapsed

            if self.state.outgoing[i][1] < 0:
                self.state.outgoing[i][1] = 0

        # Loop over all the new vessels
        if self.in1_port in inputs:
            for vessel in inputs[self.in1_port]:
                # If first vessel, no need to take into account velocity ship in front
                if len(self.state.ingoing) == 0:
                    # calculate the remaining time
                    remaining_time = self.state.distance / vessel.avg_v
                    self.state.ingoing.append([vessel, remaining_time, vessel.avg_v])

                # If not first vessel, need to take into account velocity ship in front (take min)
                else:
                    # Get vessel in front with it's velocity to calculate min (vessel, front vessels)
                    front_vessel_avg = self.state.ingoing[-1][2]
                    min_avg_velocity = min(vessel.avg_v, front_vessel_avg)
                    remaining_time = self.state.distance / min_avg_velocity
                    self.state.ingoing.append([vessel, remaining_time, min_avg_velocity])

        if self.in2_port in inputs:
            for vessel in inputs[self.in2_port]:
                # If first vessel, no need to take into account velocity ship in front
                if len(self.state.outgoing) == 0:
                    # calculate the remaining time
                    remaining_time = self.state.distance / vessel.avg_v
                    self.state.outgoing.append([vessel, remaining_time, vessel.avg_v])

                # If not first vessel, need to take into account velocity ship in front (take min)
                else:
                    # Get vessel in front with it's velocity to calculate min (my vel, front vel)
                    front_vessel_avg = self.state.outgoing[-1][2]
                    min_avg_velocity = min(vessel.avg_v, front_vessel_avg)
                    remaining_time = self.state.distance / min_avg_velocity
                    self.state.outgoing.append([vessel, remaining_time, min_avg_velocity])

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the waterway
        self.state.remaining_time = float("inf")

        # wait for the vessels in front
        if len(self.state.ingoing) > 0:
            self.state.remaining_time = self.state.ingoing[0][1]
        if len(self.state.outgoing) > 0:
            self.state.remaining_time = min(self.state.outgoing[0][1], self.state.remaining_time)
        # if a vessel wants to leave: no delay
        if len(self.state.ingoing_leaving) > 0:
            self.state.remaining_time = 0
        if len(self.state.outgoing_leaving) > 0:
            self.state.remaining_time = 0
        return self.state.remaining_time

    def outputFnc(self):
        # Output all the vessels who left the water canal
        return_dict = {}
        if len(self.state.ingoing_leaving) > 0:
            leaving = self.state.ingoing_leaving
            self.state.ingoing_leaving = []
            return_dict[self.out1_port] = leaving

        if len(self.state.outgoing_leaving) > 0:
            leaving = self.state.outgoing_leaving
            self.state.outgoing_leaving = []
            return_dict[self.out2_port] = leaving

        return return_dict