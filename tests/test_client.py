from unittest.mock import MagicMock, patch

import pytest
import requests

from weather.client import CityNotFoundError, WeatherAPIError, get_weather
from weather.models import WeatherData

MOCK_RESPONSE = {
    "name": "Mumbai",
    "sys": {"country": "IN"},
    "main": {"temp": 32.0, "feels_like": 35.0, "humidity": 80},
    "weather": [{"description": "haze"}],
    "wind": {"speed": 4.5},
}


@patch("weather.client.config.API_KEY", "test-key")
@patch("weather.client.cache.get", return_value=None)
@patch("weather.client.cache.set")
@patch("weather.client.requests.get")
def test_get_weather_success(mock_get, mock_cache_set, mock_cache_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = MOCK_RESPONSE
    mock_get.return_value = mock_resp

    result = get_weather("Mumbai")
    assert isinstance(result, WeatherData)
    assert result.city == "Mumbai"
    assert result.temperature == 32.0
    assert not result.is_stale


@patch("weather.client.config.API_KEY", "test-key")
@patch("weather.client.cache.get", return_value=None)
@patch("weather.client.requests.get")
def test_city_not_found(mock_get, mock_cache_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp

    with pytest.raises(CityNotFoundError):
        get_weather("Fakecityxyz")


@patch("weather.client.config.API_KEY", "test-key")
@patch("weather.client.cache.get", return_value=None)
@patch("weather.client.cache.get_stale", return_value=MOCK_RESPONSE)
@patch("weather.client.requests.get", side_effect=requests.RequestException("timeout"))
def test_falls_back_to_stale_cache(mock_get, mock_stale, mock_cache_get):
    result = get_weather("Mumbai")
    assert result.is_stale


@patch("weather.client.config.API_KEY", "test-key")
@patch("weather.client.cache.get", return_value=MOCK_RESPONSE)
def test_returns_cached_data(mock_cache_get):
    result = get_weather("Mumbai")
    assert result.city == "Mumbai"
    assert not result.is_stale
