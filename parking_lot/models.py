from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
from datetime import datetime

from .states import FreeState,SpotState

class VehicleType(Enum):
    MOTORCYCLE="motorcycle"
    CAR="car"
    LARGE="large"
    
class SpotType(Enum):
    SMALL="small"
    MEDIUM="medium"
    LARGE="large"
    

@dataclass (frozen=True)
class Vehicle:
    plate:str
    vehicle_type:VehicleType
    
@dataclass
class Ticket:
    id:str
    vehicle:Vehicle
    spot_id:ParkingSpot
    entry_time:datetime
    exit_time:datetime|None=None
    
@dataclass
class ParkingSpot:
    id:str
    spot_type:SpotType
    state:SpotState=field(default_factory=FreeState)