import time
from typing import Optional

import requests

from . import cache, config
from .models import WeatherData


class WeatherAPIError(Exception):
    pass


class CityNotFoundError(WeatherAPIError):
    pass


class APIKeyError(WeatherAPIError):
    pass


def _fetch_from_api(city: str) -> dict:
    last_exc: Optional[Exception] = None
    for attempt in range(config.MAX_RETRIES):
        try:
            response = requests.get(
                config.BASE_URL,
                params={"q": city, "appid": config.API_KEY, "units": "metric"},
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code == 404:
                raise CityNotFoundError(f"City '{city}' not found.")
            if response.status_code == 401:
                raise APIKeyError("Invalid or missing API key. Set OPENWEATHER_API_KEY.")
            if response.status_code == 429:
                raise WeatherAPIError("Rate limited by OpenWeatherMap. Try again later.")
            response.raise_for_status()
            return response.json()
        except (CityNotFoundError, APIKeyError):
            raise  # no point retrying these
        except requests.RequestException as exc:
            last_exc = exc
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # exponential backoff: 1s, 2s

    raise WeatherAPIError(f"Failed after {config.MAX_RETRIES} attempts: {last_exc}")


def _parse(raw: dict, is_stale: bool = False) -> WeatherData:
    return WeatherData(
        city=raw["name"],
        country=raw["sys"]["country"],
        temperature=raw["main"]["temp"],
        feels_like=raw["main"]["feels_like"],
        description=raw["weather"][0]["description"],
        humidity=raw["main"]["humidity"],
        wind_speed=raw["wind"]["speed"],
        condition_id=raw["weather"][0].get("id", 800),
        is_stale=is_stale,
    )


def get_weather(city: str) -> WeatherData:
    if not config.API_KEY:
        raise APIKeyError("OPENWEATHER_API_KEY environment variable is not set.")

    cached = cache.get(city)
    if cached:
        return _parse(cached)

    try:
        raw = _fetch_from_api(city)
        cache.set(city, raw)
        return _parse(raw)
    except WeatherAPIError:
        stale = cache.get_stale(city)
        if stale:
            return _parse(stale, is_stale=True)
        raise
