class portEntryRequest():
    '''
    Indicates a message sent from the Anchorpoint to the ControlTower,
    informing the latter that a ship with a certain identification number would like to enter the port.
    '''
    def __init__(self, uuid):
        self.vessel_id = uuid

class portEntryPermission():
    '''
    This is a message sent from the ControlTower to the Anchorpoint, informing the latter that a ship
    with a certain identification number is allowed to enter the port and can dock at a specified quay.
    '''
    def __init__(self, vessel_id, quay_id):
        self.vessel_id = vessel_id
        self.destination = quay_id


class portDepartureRequests():
    '''
    Sent by a Dock to the ControlTower, identifying that a certain
    Vessel has left a specific Dock, making room for another ship to arrive.
    '''
    def __init__(self, vessel_id, quay_id = "S"):
        self.vessel_id = vessel_id
        self.quay_id = quay_id