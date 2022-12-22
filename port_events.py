from pypdevs.message import NetworkMessage as message

class portEntryRequest(message):
    '''
    Indicates a message sent from the Anchorpoint to the ControlTower,
    informing the latter that a ship with a certain identification number would like to enter the port.
    '''
    def __init__(self, timestamp, uuid, vessel):
        self.vessel = vessel
        self.uuid = uuid
        self.timestamp = timestamp
        self.content = f"Ship {vessel.name} with id {vessel.id} would like to enter the port"
        super().__init__(timestamp, self.content, uuid)

    def getMessageContent(self):
        return self.content


class portEntryPermission(message):
    '''
    This is a message sent from the ControlTower to the Anchorpoint, informing the latter that a ship
    with a certain identification number is allowed to enter the port and can dock at a specified quay.
    '''
    def __init__(self, timestamp, uuid, destination, vessel):
        self.destination = destination
        self.vessel = vessel
        self.uuid = uuid
        self.timestamp = timestamp
        self.content = f"Ship {vessel.name} with id {vessel.id} is allowed to enter port and can dock at {destination}"
        super().__init__(timestamp, self.content, uuid, destination)

    def getMessageContent(self):
        return self.content

class portDepartureRequests(message):
    '''
    Sent by a Dock to the ControlTower, identifying that a certain
    Vessel has left a specific Dock, making room for another ship to arrive.
    '''
    def __init__(self, timestamp, uuid, destination, vessel):
        self.content = f"Ship {vessel.name} with id {vessel.id} has left dock {destination}"
        super().__init__(timestamp, self.content, uuid, destination)

    def getMessageContent(self):
        return self.content