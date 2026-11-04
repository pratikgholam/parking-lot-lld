from __future__ import annotations
from .errors import ParkingError
from .models import ParkingSpot, SpotType, Vehicle, VehicleType


class UnknownVehicleTypeError(ParkingError):
    """Raised when the vehicle type string is not recognised."""
    
class UnknownSpotTypeError(ParkingError):
    """Raised when the spot type string is not recognised."""

class VehicleFactory:
    """Centralises vehicle creation from type strings.

    Validation of the type string lives here instead of being scattered
    through callers. Case-insensitive input is accepted.
    """
    _TYPES = {
        "motorcycle" : VehicleType.MOTORCYCLE,
        "car" : VehicleType.CAR,
        "large" : VehicleType.LARGE,
    }
    
    def create(self, vehicle_type : str, plate : str) -> Vehicle:
        try:
            vtype = self._TYPES[vehicle_type.lower()]
        except KeyError:
            raise UnknownVehicleTypeError(f"Unknown vehicle type {vehicle_type}")
        return Vehicle(plate = plate, vehicle_type = vtype)
    

class SpotFactory:
    """Centralises spot creation from type strings.

    Each new spot starts in ``FreeState``. The lot owns spot id
    sequencing; the factory only resolves the type string to a spot.
    """
    _TYPES = {
        "small" : SpotType.SMALL,
        "medium" : SpotType.MEDIUM,
        "large" : SpotType.LARGE,
    }
    
    def create(self, spot_type: str) -> ParkingSpot:
        try:
            stype = self._TYPES[spot_type.lower()]
        except KeyError:
            raise UnknownSpotTypeError(f"Unknown Spot Type {spot_type}")
        return ParkingSpot(id = "", spot_type = stype)