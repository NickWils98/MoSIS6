import numpy as np


class VesselFactory():
    def create(self):
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

        return boat
class Vessel(object):
    def __init__(self, creation_time):
        self.name = self.getVesselName()
        self.creation_time = creation_time
        self.id = 0
        self.destination = ""

    def getVesselName(self):
        '''
        Get vessel name for ship
        :return: random name chose from list
        '''
        with open("shipnames.txt", 'r', encoding='utf-8') as f:
            words = f.read().splitlines()

        return np.random.choice(words)


class CrudeOilTanker(Vessel):
    def __init__(self, creation):
        super().__init__(creation)
        self.type = "Crude Oil Tanker"
        self.surface_area = 11007
        self.avg_v = 19.8164/60
        self.max_v = 28.5727/60
        self.prob = .28


class BulkCarrier(Vessel):
    def __init__(self, creation):
        super().__init__(creation)
        self.type = "Bulk Carrier"
        self.surface_area = 5399
        self.avg_v = 22.224/60
        self.max_v = 28.8912/60
        self.prob = .22


class TugBoat(Vessel):
    def __init__(self, creation):
        super().__init__(creation)
        self.type = "Tug Boat"
        self.surface_area = 348
        self.avg_v = 14.4456/60
        self.max_v = 19.6312/60
        self.prob = .33


class SmallCargoFreighter(Vessel):
    def __init__(self, creation):
        super().__init__(creation)
        self.type = "Small Cargo Freighter"
        self.surface_area = 1265
        self.avg_v = 11.8528/60
        self.max_v = 18.1496/60
        self.prob = .17


