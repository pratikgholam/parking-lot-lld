from __future__ import annotations
from datetime import datetime
from typing import Dict

from .errors import LotFullError, TicketNotFoundError
from .models import ParkingSpot, SpotType, Ticket, Vehicle, VehicleType

class ParkingLot:
    def __init__(self) -> None:
        self._spots: Dict[str, ParkingSpot] = {}
        self._tickets: Dict[str, Ticket] = {}
        self._next_ticket_id = 1
        self._next_spot_id = 1
    
    def add_spot(self, spot_type:SpotType) -> None:
        spot_id = f"S{self._next_spot_id}"
        self._next_spot_id+=1
        self._spots[spot_id]=ParkingSpot(id=spot_id,spot_type=spot_type)
        
    def park(self, vehicle: Vehicle) -> Ticket:
        spot = self._find_free_spot(vehicle.vehicle_type)
        if spot is None:
            raise LotFullError(f"No Free Spot for {vehicle.vehicle_type.value}")
        spot.is_free=False
        ticket_id = f"T{self._next_ticket_id}"
        self._next_ticket_id+=1
        ticket=Ticket(
            id=ticket_id,
            vehicle=vehicle,
            spot_id=spot.id,
            entry_time=datetime.now(),
        )
        self._tickets[ticket_id]=ticket
        return ticket
        
    def unpark(self, ticket_id:str)->float:
        ticket=self._tickets.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
        if ticket.exit_time is not None:
            raise TicketNotFoundError(f"Ticket {ticket_id} already exited")
        spot = self._spots[ticket.spot_id]
        spot.is_free=True
        ticket.exit_time=datetime.now()
        return 5.0
    
    def _find_free_spot(self, vehicle_type: VehicleType) -> ParkingSpot | None:
        for spot in self._spots.values():
            if spot.is_free and self._fits(vehicle_type, spot.spot_type):
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