import argparse
import sys

from .client import APIKeyError, CityNotFoundError, WeatherAPIError, get_weather


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
        print(data.display())
    except CityNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except APIKeyError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(2)
    except WeatherAPIError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(3)
