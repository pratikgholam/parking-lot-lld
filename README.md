# Parking Lot (Low Level Design)

A small, framework-free Python library that models a parking lot. It demonstrates three classic design patterns — Strategy, Factory, and State — in about 200 lines of code so a reviewer can read it in minutes.

## What it does

- Park a vehicle and return a ticket
- Unpark a vehicle by ticket and return a fee
- Assign the nearest free spot that fits the vehicle type
- Support motorcycles, cars, and large vehicles across small, medium, and large spots
- Calculate fees with swappable pricing strategies (hourly, flat rate, peak-hour)
- Report free-spot counts by spot type
- Track spot lifecycle states: free, occupied, out of service

Everything lives in memory. There is no database, web API, or persistence.

## How to run

Requires Python 3.11+ and `pytest`.

```bash
# Run the test suite
pytest

# Run the demo
python main.py
```

## Class diagram

```text
VehicleType (enum)      SpotType (enum)
   |                         |
   v                         v
Vehicle dataclass      ParkingSpot dataclass
   |                         |
   v                         v
Ticket dataclass         +--- SpotState (ABC)
                                          |
                    +---------------------+---------------------+
                    |                     |                     |
              FreeState             OccupiedState      OutOfServiceState

PricingStrategy (ABC)    ParkingLot
   |                          |
   +--- HourlyPricing         +-- uses --+
   +--- FlatRatePricing       |          |
   +--- PeakHourPricing       v          v
                               errors.py  factory.py
                               (exceptions) (VehicleFactory, SpotFactory)
```

## Why each pattern

**Strategy** — Pricing rules change independently of the lot logic. `ParkingLot` holds a `PricingStrategy` and delegates fee calculation to it. To add a new pricing rule (say, weekend rates), you create one new class and never touch `ParkingLot`.

**Factory** — Creating vehicles and spots from type strings is centralized in `VehicleFactory` and `SpotFactory`. Validation and defaults live in one place instead of being scattered through the codebase.

**State** — A spot's behavior depends on its state. You can only park in a `Free` spot, only unpark from an `Occupied` spot, and an `OutOfService` spot rejects both. State objects replace scattered `if spot.state == ...` checks.

## Known limitations

- No concurrency control or threading
- Data lives in memory only (no database or file storage)
- No web API, payments, sensors, or license plate recognition

## Files

- `parking_lot/models.py` — domain models (enums, dataclasses)
- `parking_lot/states.py` — State pattern for spot lifecycle
- `parking_lot/pricing.py` — Strategy pattern for pricing
- `parking_lot/factory.py` — Factory for vehicles and spots
- `parking_lot/lot.py` — `ParkingLot` orchestrator
- `parking_lot/errors.py` — domain exceptions
- `tests/` — pytest suite
- `main.py` — demo script
