from __future__ import annotations

import pytest

from parking_lot.factory import (
    SpotFactory,
    UnknownSpotTypeError,
    UnknownVehicleTypeError,
    VehicleFactory,
)
from parking_lot.models import SpotType, VehicleType


def test_vehicle_factory_creates_car() -> None:
    factory = VehicleFactory()
    vehicle = factory.create("car", "ABC-123")
    assert vehicle.vehicle_type is VehicleType.CAR
    assert vehicle.plate == "ABC-123"


def test_vehicle_factory_creates_motorcycle() -> None:
    factory = VehicleFactory()
    vehicle = factory.create("motorcycle", "M1")
    assert vehicle.vehicle_type is VehicleType.MOTORCYCLE


def test_vehicle_factory_creates_large() -> None:
    factory = VehicleFactory()
    vehicle = factory.create("large", "L1")
    assert vehicle.vehicle_type is VehicleType.LARGE


def test_vehicle_factory_accepts_uppercase() -> None:
    factory = VehicleFactory()
    vehicle = factory.create("CAR", "ABC-123")
    assert vehicle.vehicle_type is VehicleType.CAR


def test_vehicle_factory_unknown_type_raises() -> None:
    factory = VehicleFactory()
    with pytest.raises(UnknownVehicleTypeError):
        factory.create("bicycle", "B1")


def test_spot_factory_creates_small() -> None:
    factory = SpotFactory()
    spot = factory.create("small")
    assert spot.spot_type is SpotType.SMALL


def test_spot_factory_creates_medium() -> None:
    factory = SpotFactory()
    spot = factory.create("medium")
    assert spot.spot_type is SpotType.MEDIUM


def test_spot_factory_creates_large() -> None:
    factory = SpotFactory()
    spot = factory.create("large")
    assert spot.spot_type is SpotType.LARGE


def test_spot_factory_accepts_uppercase() -> None:
    factory = SpotFactory()
    spot = factory.create("LARGE")
    assert spot.spot_type is SpotType.LARGE


def test_spot_factory_unknown_type_raises() -> None:
    factory = SpotFactory()
    with pytest.raises(UnknownSpotTypeError):
        factory.create("xl")