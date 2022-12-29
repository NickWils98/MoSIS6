import numpy as np
import os

# Conversion from knots to km/h
KNOT_TO_KM_H = 1.852

class VesselFactory:
    """
    Make vessels
    """
    def __init__(self, prob=(.28, .22, .33, .17)):
        self.vessel_id = 0
        self.prob_COT = prob[0]
        self.prob_BK = prob[1]
        self.prob_TB = prob[2]
        self.prob_SCF = prob[3]
        # COT then BK then TB then SCF
        self.counter = [0,0,0,0]

    def create(self, creation_time):
        """
        Create a vessel based on a probability.
        """
        number = np.random.uniform()

        if number < self.prob_COT:
            self.counter[0] +=1
            boat = CrudeOilTanker
        elif number < self.prob_COT + self.prob_BK:
            self.counter[1] +=1
            boat = BulkCarrier
        elif number < self.prob_COT + self.prob_BK + self.prob_TB:
            self.counter[2] +=1
            boat = TugBoat
        else:
            self.counter[3] +=1
            boat = SmallCargoFreighter
        self.vessel_id += 1
        return boat(creation_time, self.vessel_id)


class Vessel(object):
    def __init__(self, creation_time, vessel_id):
        self.name = self.getVesselName()
        self.creation_time = creation_time
        self.vessel_id = vessel_id
        self.destination = None
        self.enter_port = -1

    def getVesselName(self):
        '''
        Get vessel name for ship
        :return: random name chose from list
        '''
        with open(os.path.dirname(__file__) +"/../shipnames.txt", 'r', encoding='utf-8') as f:
            words = f.read().splitlines()

        return np.random.choice(words)


class CrudeOilTanker(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Crude Oil Tanker"
        self.surface_area = 11007
        self.avg_v = 10.7*KNOT_TO_KM_H
        self.max_v = 15.4 * KNOT_TO_KM_H
        self.prob = .28


class BulkCarrier(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Bulk Carrier"
        self.surface_area = 5399
        self.avg_v = 12*KNOT_TO_KM_H
        self.max_v = 15.6 * KNOT_TO_KM_H
        self.prob = .22


class TugBoat(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Tug Boat"
        self.surface_area = 348
        self.avg_v = 7.8*KNOT_TO_KM_H
        self.max_v = 10.6 * KNOT_TO_KM_H
        self.prob = .33


class SmallCargoFreighter(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Small Cargo Freighter"
        self.surface_area = 1265
        self.avg_v = 6.4*KNOT_TO_KM_H
        self.max_v = 9.8 * KNOT_TO_KM_H
        self.prob = .17


