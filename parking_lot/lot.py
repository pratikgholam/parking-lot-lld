from __future__ import annotations
from datetime import datetime
from typing import Dict
import math
from typing import Callable

from parking_lot.pricing import PricingStrategy,FlatRatePricing,PeakHourPricing,HourlyPricing
from .errors import LotFullError, TicketNotFoundError, SpotOutOfServiceError
from .models import ParkingSpot, SpotType, Ticket, Vehicle, VehicleType
from .states import FreeState,SpotState,OccupiedState

class ParkingLot:
    def __init__(self, pricing_strategy: PricingStrategy | None = None,
        clock: Callable[[], datetime] | None = None) -> None:
        self._spots: Dict[str, ParkingSpot] = {}
        self._tickets: Dict[str, Ticket] = {}
        self._next_ticket_id = 1
        self._next_spot_id = 1
        self._pricing_strategy = pricing_strategy or FlatRatePricing()
        self._clock = clock or datetime.now
    
    
    
    def add_spot(self, spot_type:SpotType) -> None:
        spot_id = f"S{self._next_spot_id}"
        self._next_spot_id+=1
        self._spots[spot_id]=ParkingSpot(id=spot_id,spot_type=spot_type)
        
        
        
    def park(self, vehicle: Vehicle) -> Ticket:
        spot = self._find_free_spot(vehicle.vehicle_type)
        if spot is None:
            raise LotFullError(f"No Free Spot for {vehicle.vehicle_type.value}")
        if not spot.state.can_park():
            raise SpotOutOfServiceError(f"Cannot Park in this spot")
             
        spot.state = OccupiedState()
        ticket_id = f"T{self._next_ticket_id}"
        self._next_ticket_id+=1
        ticket=Ticket(
            id=ticket_id,
            vehicle=vehicle,
            spot_id=spot.id,
            entry_time=self._clock(),
        )
        self._tickets[ticket_id]=ticket
        return ticket
     
        
    def unpark(self, ticket_id:str) -> float:
        ticket=self._tickets.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
        if ticket.exit_time is not None:
            raise TicketNotFoundError(f"Ticket {ticket_id} already exited")
        spot = self._spots[ticket.spot_id]
        if not spot.state.can_unpark():
            raise SpotOutOfServiceError(f"Cannot unpark from this spot")

        spot.state = FreeState()
        ticket.exit_time = self._clock()
        return self._pricing_strategy.calculate_fee(ticket.entry_time, ticket.exit_time)
    
    
    
    def _find_free_spot(self, vehicle_type: VehicleType) -> ParkingSpot | None:
        for spot in self._spots.values():
            if spot.state.can_park() and self._fits(vehicle_type, spot.spot_type):
                return spot
        return None
    
    
    
    @staticmethod
    def _fits(vehicle_type: VehicleType, spot_type:SpotType)->bool:
        vehicle_order={
            VehicleType.MOTORCYCLE: 1,
            VehicleType.CAR: 2,
            VehicleType.LARGE: 3,
        }
        spot_order={
            SpotType.SMALL: 1,
            SpotType.MEDIUM: 2,
            SpotType.LARGE: 3,
        }
        return spot_order[spot_type] >= vehicle_order[vehicle_type]