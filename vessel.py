import random


class Vessel(object):
    def __init__(self):
        self.name = self.getVesselName()
        self.id = 0
        self.destinations = ""

    def getVesselName(self):
        '''
        Get vessel name for ship
        :return: random name chose from list
        '''
        with open("shipnames.txt", 'r', encoding='utf-8') as f:
            words = f.read().splitlines()

        return random.choice(words)


class CrudeOilTanker(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Crude Oil Tanker"
        self.surface_area = 11007
        self.avg_v = 10.7
        self.max_v = 15.4
        self.prob = .28


class BulkCarrier(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Bulk Carrier"
        self.surface_area = 5399
        self.avg_v = 12
        self.max_v = 15.6
        self.prob = .22


class TugBoat(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Tug Boat"
        self.surface_area = 348
        self.avg_v = 7.8
        self.max_v = 10.6
        self.prob = .33


class SmallCargoFreighter(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Small Cargo Freighter"
        self.surface_area = 1265
        self.avg_v = 6.4
        self.max_v = 9.8
        self.prob = .17


