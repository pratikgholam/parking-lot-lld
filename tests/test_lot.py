from __future__ import annotations

import pytest

from parking_lot.errors import LotFullError, TicketNotFoundError
from parking_lot.lot import ParkingLot
from parking_lot.models import SpotType, Vehicle, VehicleType


def _make_lot() -> ParkingLot:
    """Create a fresh lot with 2 small, 2 medium, 2 large spots."""
    lot = ParkingLot()
    for _ in range(2):
        lot.add_spot(SpotType.SMALL)
    for _ in range(2):
        lot.add_spot(SpotType.MEDIUM)
    for _ in range(2):
        lot.add_spot(SpotType.LARGE)
    return lot


def test_park_and_unpark() -> None:
    lot = _make_lot()
    vehicle = Vehicle("ABC-123", VehicleType.CAR)
    ticket = lot.park(vehicle)
    assert ticket.id.startswith("T")
    fee = lot.unpark(ticket.id)
    assert fee == 5.0


def test_lot_full_raises() -> None:
    lot = _make_lot()
    for i in range(6):
        lot.park(Vehicle(f"V{i}", VehicleType.MOTORCYCLE))
    with pytest.raises(LotFullError):
        lot.park(Vehicle("V6", VehicleType.MOTORCYCLE))


def test_unknown_ticket_raises() -> None:
    lot = _make_lot()
    with pytest.raises(TicketNotFoundError):
        lot.unpark("T999")


def test_double_unpark_raises() -> None:
    lot = _make_lot()
    vehicle = Vehicle("ABC-123", VehicleType.CAR)
    ticket = lot.park(vehicle)
    lot.unpark(ticket.id)
    with pytest.raises(TicketNotFoundError):
        lot.unpark(ticket.id)


def test_free_spot_counts() -> None:
    lot = _make_lot()
    assert lot.free_spot_counts() == {
        SpotType.SMALL: 2,
        SpotType.MEDIUM: 2,
        SpotType.LARGE: 2,
    }
    vehicle = Vehicle("ABC-123", VehicleType.CAR)
    lot.park(vehicle)
    counts = lot.free_spot_counts()
    assert counts[SpotType.MEDIUM] == 1
    assert counts[SpotType.SMALL] == 2
    assert counts[SpotType.LARGE] == 2