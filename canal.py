from pypdevs.DEVS import AtomicDEVS
import port_events as Messages

# Define the state of the AnchorPoint as a structured object
class WaterwayState:
    def __init__(self, distance):
        self.current_time = 0
        self.remaining_time = 0

        self.ingoing = [] # Queue van dictionaries
        self.ingoing_leaving = [] # lijst van vessels
        self.outgoing = []
        self.ingoing_leaving = []

        self.distance = distance


class Waterway(AtomicDEVS):
    def __init__(self, distance):
        AtomicDEVS.__init__(self, "K")
        # Fix the time needed to process a single event
        self.processing_time = 0
        self.state = WaterwayState(distance)

        # Create input and output ports for one way
        self.in1_port = self.addInPort("in_port")
        self.out1_port = self.addOutPort("out_port")

        # TODO: Create input and output ports for the other way

    def intTransition(self):
        #self.state.current_time += self.elapsed
        if len(self.state.ingoing) != 0:
            for vessel_dict in self.state.ingoing:
                for vessel, remainder in vessel_dict:
                    new_time = remainder - self.elapsed
                    vessel_dict[vessel] = new_time

            # Check wether a vessel has arrived or not
            for vessel_dict in self.state.ingoing:
                for vessel, remainder in vessel_dict:
                    if remainder <= 0:
                        self.state.ingoing_leaving.append(vessel)  # Als ge meteen popt komt uw loop in de shit

            # delete from the dictionary
            for vessel_dict in self.state.ingoing:
                for vessel, remainder in vessel_dict:
                    if vessel in self.state.ingoing_leaving:
                        self.state.ingoing.pop()

        # TODO: Same for outgoing, aka other direction

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
        # Just return the remaining time for this event
        return self.state.remaining_time


    def outputFnc(self):
        # Output all the ships who left the water canal
        leaving = self.state.ingoing_leaving
        self.state.ingoing_leaving = []
        return {self.out1_port: leaving}
