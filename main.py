from __future__ import annotations

from parking_lot.lot import ParkingLot
from parking_lot.models import SpotType, Vehicle, VehicleType
from parking_lot.pricing import FlatRatePricing



def main() -> None:
    lot = ParkingLot(pricing_strategy=FlatRatePricing(5.0))
    for _ in range(2):
        lot.add_spot(SpotType.SMALL)
    for _ in range(2):
        lot.add_spot(SpotType.MEDIUM)
    for _ in range(2):
        lot.add_spot(SpotType.LARGE)
    
    print("Free Spots: ",lot.free_spot_counts())
    
    bike = Vehicle("MH-12-AB-1234", VehicleType.MOTORCYCLE)
    car = Vehicle("MH-12-CD-5678", VehicleType.CAR)
    truck = Vehicle("MH-12-EF-9012", VehicleType.LARGE)

    t1 = lot.park(bike)
    t2 = lot.park(car)
    t3 = lot.park(truck)
    
    print("Free spots after parking:", lot.free_spot_counts())

    print(f"Unpark bike {t1.id}: fee ${lot.unpark(t1.id):.2f}")
    print(f"Unpark car {t2.id}: fee ${lot.unpark(t2.id):.2f}")
    print(f"Unpark truck {t3.id}: fee ${lot.unpark(t3.id):.2f}")

    print("Free spots after unparking:", lot.free_spot_counts())


if __name__ == "__main__":
    main()