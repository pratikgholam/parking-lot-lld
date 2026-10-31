
#Parent Error Method
class ParkingError(Exception):
    print("Parking Error")
    

#Sub-classes to clarify each error
 
class TicketNotFoundError(ParkingError):
    print("Ticket not found")
    
class LotFullError(ParkingError):
    print("Lot is full")
    
class SpotOutOfServiceError(ParkingError):
    print("Spot out of service")