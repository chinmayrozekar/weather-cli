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
    is_stale: bool = False

    def display(self) -> str:
        stale_note = " [cached — live data unavailable]" if self.is_stale else ""
        return (
            f"The Weather in {self.city}, {self.country} is {self.description.capitalize()}\n"
            f"  Temperature : {self.temperature}°C (feels like {self.feels_like}°C)\n"
            f"  Humidity    : {self.humidity}%\n"
            f"  Wind Speed  : {self.wind_speed} m/s"
            f"{stale_note}"
        )
