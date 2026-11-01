from datetime import datetime
from abc import ABC, abstractmethod
import math

from .models import ParkingSpot, SpotType, Ticket, Vehicle, VehicleType


class PricingStrategy(ABC):       
    @abstractmethod
    def calculate_fee(self, entry_time, exit_time) -> float:
        pass
    
class FlatRatePricing(PricingStrategy):
    def __init__(self, rate: float = 5.0) -> None:
        self._rate=rate
        
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        return self._rate
    
class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: float=2.0) -> None:
        self._rate_per_hour=rate_per_hour
        
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        minutes=(exit_time-entry_time).total_seconds()/60
        hours=math.ceil(minutes/60)
        return hours * self._rate_per_hour
    
    
class PeakHourPricing(PricingStrategy):
    def __init__(self, base_rate: float=2.0, peak_rate: float=4.0, peak_start_hour: int =18, peak_end_hour: int=22) -> None:
        self._base_rate=base_rate
        self._peak_rate=peak_rate
        self._peak_start_hour=peak_start_hour
        self._peak_end_hour=peak_end_hour
        
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        minutes=(exit_time-entry_time).total_seconds()/60
        hours=math.ceil(minutes/60)
        
        if self._peak_start_hour <= entry_time.hour < self._peak_end_hour:
            return hours * self._peak_rate
        
        return hours * self._base_rate