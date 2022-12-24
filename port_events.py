from pypdevs.message import NetworkMessage as message

class portEntryRequest():
    '''
    Indicates a message sent from the Anchorpoint to the ControlTower,
    informing the latter that a ship with a certain identification number would like to enter the port.
    '''
    def __init__(self, timestamp, uuid, vessel):
        self.vessel = vessel
        self.uuid = uuid
        self.timestamp = timestamp
        self.content = f"Ship {vessel.name} with id {vessel.uuid} would like to enter the port"

    def getMessageContent(self):
        return self.content


class portEntryPermission():
    '''
    This is a message sent from the ControlTower to the Anchorpoint, informing the latter that a ship
    with a certain identification number is allowed to enter the port and can dock at a specified quay.
    '''
    def __init__(self, timestamp, uuid, vessel, dock):
        self.vessel = vessel
        self.uuid = uuid
        self.timestamp = timestamp
        self.destination = dock
        self.content = f"Ship {vessel.name} with id {vessel.uuid} is allowed to enter port and can dock at quay {dock}"

    def getMessageContent(self):
        return self.content

class portDepartureRequests():
    '''
    Sent by a Dock to the ControlTower, identifying that a certain
    Vessel has left a specific Dock, making room for another ship to arrive.
    '''
    def __init__(self, timestamp, uuid, vessel, quay_id):
        self.vessel = vessel
        self.uuid = uuid
        self.timestamp = timestamp
        self.quay_id = quay_id
        self.content = f"Ship {vessel.name} with id {vessel.uuid} has left dock {self.quay_id}"

    def getMessageContent(self):
        return self.content