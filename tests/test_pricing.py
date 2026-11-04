from datetime import datetime

from parking_lot.pricing import FlatRatePricing, HourlyPricing, PeakHourPricing

def test_flat_rate_returns_constant() -> None:
    strategy = FlatRatePricing(5.0)
    entry = datetime(2026, 1, 1, 10, 0, 0)
    exit_ = datetime(2026, 1, 1, 10, 30, 0)
    assert strategy.calculate_fee(entry, exit_) == 5.0


def test_hourly_rounds_up() -> None:
    strategy = HourlyPricing(2.0)
    entry = datetime(2026, 1, 1, 10, 0, 0)
    exit_ = datetime(2026, 1, 1, 10, 30, 0)  # 30 minutes -> rounds up to 1 hour
    assert strategy.calculate_fee(entry, exit_) == 2.0
    
def test_hourly_rounds_up_to_next_hour() -> None:
    strategy = HourlyPricing(2.0)
    entry = datetime(2026, 1, 1, 10, 0, 0)
    exit_ = datetime(2026, 1, 1, 10, 30, 0)  # 30 min -> rounds up to 1 hour
    assert strategy.calculate_fee(entry, exit_) == 2.0


def test_hourly_charges_multiple_hours() -> None:
    strategy = HourlyPricing(2.0)
    entry = datetime(2026, 1, 1, 10, 0, 0)
    exit_ = datetime(2026, 1, 1, 12, 30, 0)  # 2.5 hours -> rounds up to 3 hours
    assert strategy.calculate_fee(entry, exit_) == 6.0


def test_peak_hour_uses_peak_rate() -> None:
    strategy = PeakHourPricing(base_rate=2.0, peak_rate=4.0, peak_start_hour=18, peak_end_hour=22)
    entry = datetime(2026, 1, 1, 19, 0, 0)  # inside peak window
    exit_ = datetime(2026, 1, 1, 20, 0, 0)   # 1 hour
    assert strategy.calculate_fee(entry, exit_) == 4.0


def test_peak_hour_outside_window_uses_base_rate() -> None:
    strategy = PeakHourPricing(base_rate=2.0, peak_rate=4.0, peak_start_hour=18, peak_end_hour=22)
    entry = datetime(2026, 1, 1, 14, 0, 0)  # outside peak window
    exit_ = datetime(2026, 1, 1, 15, 0, 0)   # 1 hour
    assert strategy.calculate_fee(entry, exit_) == 2.0