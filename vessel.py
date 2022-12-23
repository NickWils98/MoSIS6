import numpy as np

# Conversion from knots to km/h
KNOT_TO_KM_H =1.852

class VesselFactory:
    """
    Make vessels
    """
    def __init__(self):
        self.uuid = 0
    def create(self, creation_time):
        """
        Create a vessel based on a probability.
        """
        number = np.random.uniform()
        choice = 0
        prob_COT = .28
        prob_BK = .22
        prob_TB = .33
        prob_SCF = .17

        if number < prob_COT:
            boat = CrudeOilTanker
        elif number < prob_COT + prob_BK:
            boat = BulkCarrier
        elif number < prob_COT + prob_BK + prob_TB:
            boat = TugBoat
        else:
            boat = SmallCargoFreighter
        self.uuid += 1
        return boat(creation_time, self.uuid)


class Vessel(object):
    def __init__(self, creation_time, uuid):
        self.name = self.getVesselName()
        self.creation_time = creation_time
        self.uuid = uuid
        self.destination = None

    def getVesselName(self):
        '''
        Get vessel name for ship
        :return: random name chose from list
        '''
        with open("shipnames.txt", 'r', encoding='utf-8') as f:
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


