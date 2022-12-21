import random


class Vessel(object):
    def __init__(self):
        self.name = self.getVesselName()
        self.id = 0
        self.destination = ""

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
        self.avg_v = 19.8164
        self.max_v = 28.5727
        self.prob = .28


class BulkCarrier(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Bulk Carrier"
        self.surface_area = 5399
        self.avg_v = 22.224
        self.max_v = 28.8912
        self.prob = .22


class TugBoat(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Tug Boat"
        self.surface_area = 348
        self.avg_v = 14.4456
        self.max_v = 19.6312
        self.prob = .33


class SmallCargoFreighter(Vessel):
    def __init__(self):
        super().__init__()
        self.type = "Small Cargo Freighter"
        self.surface_area = 1265
        self.avg_v = 11.8528
        self.max_v = 18.1496
        self.prob = .17


