from __future__ import annotations

import pytest

from parking_lot.errors import SpotOutOfServiceError
from parking_lot.lot import ParkingLot
from parking_lot.models import ParkingSpot, SpotType, Vehicle, VehicleType
from parking_lot.states import FreeState, OccupiedState, OutOfServiceState


def test_free_state_allows_park_rejects_unpark() -> None:
    state = FreeState()
    assert state.can_park() is True
    assert state.can_unpark() is False
    
def test_occupied_state_rejects_park_allows_unpark() -> None:
    state = OccupiedState()
    assert state.can_park() is False
    assert state.can_unpark() is True


def test_out_of_service_state_rejects_both() -> None:
    state = OutOfServiceState()
    assert state.can_park() is False
    assert state.can_unpark() is False


def test_unpark_rejects_out_of_service_spot() -> None:
    lot = ParkingLot()
    lot.add_spot(SpotType.SMALL)
    lot.add_spot(SpotType.MEDIUM)
    vehicle = Vehicle("ABC-123", VehicleType.CAR)
    ticket = lot.park(vehicle)
    spot = lot._spots[ticket.spot_id]
    spot.state = OutOfServiceState()
    with pytest.raises(SpotOutOfServiceError):
        lot.unpark(ticket.id)