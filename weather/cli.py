import argparse
import sys

from rich.console import Console

from .client import APIKeyError, CityNotFoundError, WeatherAPIError, get_weather
from . import display

err = Console(stderr=True, style="bold red")


def run():
    parser = argparse.ArgumentParser(
        prog="weather",
        description="Get current weather for any city.",
    )
    parser.add_argument("city", nargs="+", help="City name (e.g. Mumbai or 'New Delhi')")
    args = parser.parse_args()

    city = " ".join(args.city)

    try:
        data = get_weather(city)
        display.render(data)
    except CityNotFoundError as e:
        err.print(f"Error: {e}")
        sys.exit(1)
    except APIKeyError as e:
        err.print(f"Config error: {e}")
        sys.exit(2)
    except WeatherAPIError as e:
        err.print(f"Network error: {e}")
        sys.exit(3)
