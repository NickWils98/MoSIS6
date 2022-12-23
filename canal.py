from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.remaining_time = 0

        self.ingoing = [] # Queue van dictionaries
        self.ingoing_leaving = [] # lijst van vessels
        self.outgoing = []
        self.outgoing_leaving = []

        self.distance = distance


class Waterway(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "K")
        # Fix the time needed to process a single event
        self.state = WaterwayState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")

    def intTransition(self):

        if len(self.state.ingoing) != 0:
            for vessel_dict in self.state.ingoing:
                for vessel in vessel_dict.keys():
                    if self.elapsed is not None:
                        vessel_dict[vessel] -= self.elapsed

                    if self.state.ingoing[vessel] <= 0:
                        self.state.ingoing_leaving.append(vessel)

            # delete from the dictionary
            for vessel in self.state.ingoing_leaving:
                del self.state.ingoing[vessel]

        return self.state

    def extTransition(self, inputs):
        if self.in1_port in inputs:
            # If first vessel, no need to take into account velocity ship in front
            if len(self.state.ingoing) == 0:
                remaining_time = self.state.distance / self.state.ingoing[(inputs[self.in1_port])].avg_v
                self.state.ingoing.append({inputs[self.in1_port]: remaining_time})
                self.state.remaining_time = 100
            # If not first vessel, need to take into account velocity ship in front (take min)
            else:
                # Get vessel in front and it's velocity to calculate min (my vel, front vel)
                front_vessel = None
                vessel_in_front_index = self.state.ingoing[len(self.state.ingoing)-1]
                for key, val in self.state.ingoing[vessel_in_front_index]:
                    front_vessel = key
                min_avg_velocity = min(inputs[self.in1_port].avg_v, front_vessel.avg_v)

                remaining_time = self.state.distance / min_avg_velocity
                self.state.ingoing.append({inputs[self.in1_port]: remaining_time})
                self.state.remaining_time = 100

        return self.state

    def timeAdvance(self):
        # wait idl if there is no ship in the waterway
        self.state.remaining_time = float("inf")

        all_times = []
        # find the shortest time between the vessels
        for vessel_dict in self.state.ingoing:
            for key, val in vessel_dict:
                all_times.append(val)

        self.state.remaining_time = min(all_times)
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
