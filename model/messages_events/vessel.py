import numpy as np
import os
import math

# Conversion from knots to km/h
KNOT_TO_KM_H = 1.852

class VesselFactory:
    """
    Make vessels
    """
    def __init__(self,det_bool=False, prob=(0.28, .22, .33, .17)):
        self.det_bool = det_bool
        self.counter_det = [0,0,0,0]
        self.vessel_id = 0
        self.prob_COT = prob[0]
        self.prob_BK = prob[1]
        self.prob_TB = prob[2]
        self.prob_SCF = prob[3]
        # COT then BK then TB then SCF
        self.counter = [0,0,0,0]
        self.reset()
        self.phase = 0
    def reset(self):
        self.counter_det[0] = math.floor(self.prob_COT*100)
        self.counter_det[1] = math.floor(self.prob_BK*100)
        self.counter_det[2] = math.floor(self.prob_TB*100)
        self.counter_det[3] = math.floor(self.prob_SCF*100)
    def create(self, creation_time):
        """
        Create a vessel based on a probability.
        """
        boat = None
        if self.det_bool:
            vessel_type = -1
            # go over all the phases
            for _ in range(4):
                if self.counter_det[self.phase]>0:
                    vessel_type=self.phase
                    self.counter_det[self.phase]-=1
                    self.phase = (self.phase+1)%4
                    break
                else:
                    self.phase = (self.phase+1)%4
            # there was no room so reset
            if vessel_type==-1:
                self.reset()
                self.phase =1
                self.counter_det[0]-=1
                self.counter[0] +=1

                boat= CrudeOilTanker
            # choose vessel type
            if vessel_type == 0:
                boat = CrudeOilTanker
                self.counter[0] +=1

            elif vessel_type ==1:
                boat = BulkCarrier
                self.counter[1] +=1

            elif vessel_type ==2:
                boat = TugBoat
                self.counter[2] +=1

            elif vessel_type ==3:
                boat = SmallCargoFreighter
                self.counter[3] +=1

        else:
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
        self.avg_v = 10.7 * KNOT_TO_KM_H
        self.max_v = 15.4 * KNOT_TO_KM_H
        self.prob = .28


class BulkCarrier(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Bulk Carrier"
        self.surface_area = 5399
        self.avg_v = 12 * KNOT_TO_KM_H
        self.max_v = 15.6 * KNOT_TO_KM_H
        self.prob = .22


class TugBoat(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Tug Boat"
        self.surface_area = 348
        self.avg_v = 7.8 * KNOT_TO_KM_H
        self.max_v = 10.6 * KNOT_TO_KM_H
        self.prob = .33


class SmallCargoFreighter(Vessel):
    def __init__(self, creation_time, uuid):
        super().__init__(creation_time, uuid)
        self.type = "Small Cargo Freighter"
        self.surface_area = 1265
        self.avg_v = 6.4 * KNOT_TO_KM_H
        self.max_v = 9.8 * KNOT_TO_KM_H
        self.prob = .17


