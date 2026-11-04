
#Parent Error Method
class ParkingError(Exception):
    """Base error for all parking-lot domain errors."""
    

#Sub-classes to clarify each error
 
class TicketNotFoundError(ParkingError):
    """Raised when a ticket id is unknown or already exited."""
    
class LotFullError(ParkingError):
    """Raised when no fitting free spot exists."""
    
class SpotOutOfServiceError(ParkingError):
    """Raised when a spot is out of service and cannot be used."""