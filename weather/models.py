from dataclasses import dataclass


@dataclass
class WeatherData:
    city: str
    country: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float
    condition_id: int = 800
    is_stale: bool = False
