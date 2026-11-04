from abc import ABC, abstractmethod

class SpotState(ABC):
    """A spot's behavior depends on its state.
    
    State objects replace scattered `if spot.state == ...` checks.
    ParkingLot delegates 'can I park?' and 'can I unpark?' to the state.
    """
    @abstractmethod
    def can_park(self) -> bool:
        return True
        
    @abstractmethod
    def can_unpark(self) -> bool:
        return True
        

class FreeState(SpotState):
    def can_park(self) -> bool:
        return True
    
    def can_unpark(self) -> bool:
        return False
    
    
class OccupiedState(SpotState):
    def can_park(self) -> bool:
        return False
    
    def can_unpark(self) -> bool:
        return True
    
class OutOfServiceState(SpotState):
    def can_park(self) -> bool:
        return False
    
    def can_unpark(self) -> bool:
        return False