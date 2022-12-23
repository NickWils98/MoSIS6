from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the Canal as a structured object
class CanalState:
    def __init__(self, distance):
        self.remaining_time = float('inf')

        self.ingoing = [] # Queue van dictionaries
        self.ingoing_leaving = [] # lijst van vessels
        self.outgoing = []
        self.outgoing_leaving = []

        self.distance = distance


class Canal(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "Canal")
        # Fix the time needed to process a single event
        self.state = CanalState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")

    def intTransition(self):

        for i in range(len(self.state.ingoing)):
            self.state.ingoing[i][1] -= self.timeAdvance()

            if self.state.ingoing[i][1] <= 0:
                self.state.ingoing_leaving.append(self.state.ingoing[i][0])

        # delete from the dictionary
        for vessel in self.state.ingoing_leaving:
            self.state.ingoing.pop(0)

        return self.state

    def extTransition(self, inputs):

        for i in range(len(self.state.ingoing)):
            self.state.ingoing[i][1] -= self.elapsed
        if self.in1_port in inputs:
            # If first vessel, no need to take into account velocity ship in front
            vessel = inputs[self.in1_port]
            if len(self.state.ingoing) == 0:
                # calculate the remaining time
                remaining_time = self.state.distance / vessel.avg_v
                self.state.ingoing.append([vessel, remaining_time])

            # If not first vessel, need to take into account velocity ship in front (take min)
            else:
                # Get vessel in front and it's velocity to calculate min (my vel, front vel)
                front_vessel = self.state.ingoing[-1]

                min_avg_velocity = min(vessel.avg_v, front_vessel.avg_v)

                remaining_time = self.state.distance / min_avg_velocity
                self.state.ingoing.append([vessel, remaining_time])
        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the waterway
        self.state.remaining_time = float("inf")

        if len(self.state.ingoing) > 0:
            self.state.remaining_time = self.state.ingoing[0][1]
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
