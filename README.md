# Weather CLI

A lightweight Python CLI that fetches live weather data for any city using the [OpenWeatherMap API](https://openweathermap.org/api).

```
$ python main.py Mumbai
The Weather in Mumbai, IN is Haze
  Temperature : 33.4°C (feels like 40.1°C)
  Humidity    : 72%
  Wind Speed  : 4.1 m/s
```

---

## Features

- Query weather for any city by name
- Displays temperature, feels-like, humidity, and wind speed
- 10-minute local cache — fast repeat lookups, no wasted API calls
- Stale-cache fallback when the API is unreachable
- Exponential backoff retry (up to 3 attempts) on transient network errors
- Clean exit codes: `1` city not found, `2` bad API key, `3` network error

---

## Project Structure

```
weather_cli/
├── main.py               # Entry point
├── requirements.txt
├── weather/
│   ├── __init__.py
│   ├── cli.py            # Argument parsing, output
│   ├── client.py         # API calls, retry logic, cache integration
│   ├── cache.py          # File-based TTL cache (/tmp/weather_cache.json)
│   ├── config.py         # Env vars and constants
│   └── models.py         # WeatherData dataclass
└── tests/
    ├── __init__.py
    └── test_client.py
```

---

## Setup

**1. Get a free API key**

Sign up at [openweathermap.org](https://openweathermap.org/api) and copy your API key.

**2. Clone and install**

```bash
git clone https://github.com/chinmayrozekar/weather-cli.git
cd weather-cli
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Set your API key**

```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

Add that line to your `~/.zshrc` or `~/.bashrc` to persist it.

---

## Usage

```bash
# Single-word city
python main.py Chennai

# Multi-word city
python main.py New Delhi
python main.py "New Delhi"
```

---

## Running Tests

```bash
pytest tests/
```

---

## Configuration

All tunables live in [weather/config.py](weather/config.py):

| Variable | Default | Description |
|---|---|---|
| `OPENWEATHER_API_KEY` | *(env var)* | Your API key — never hardcode this |
| `CACHE_TTL_SECONDS` | `600` | How long a cached result is considered fresh |
| `REQUEST_TIMEOUT_SECONDS` | `5` | Per-request HTTP timeout |
| `MAX_RETRIES` | `3` | Retry attempts on transient failures |
| `CACHE_FILE` | `/tmp/weather_cache.json` | Cache file location |

---

## Scaling Notes

For high-traffic deployments (think: millions of requests):

- Replace the file cache with **Redis** (shared across instances, TTL is built-in)
- Put a **CDN or API gateway cache** in front to collapse identical city requests
- Move the OpenWeatherMap call to a **background worker** and serve from cache-first
- Use a **connection pool** and async HTTP client (e.g. `httpx` + `asyncio`) for throughput
- Rate-limit per-user at the gateway layer to prevent abuse burning your API quota
- Store API keys in a **secrets manager** (AWS Secrets Manager, Vault) — never in env vars on shared infra

---

## License

MIT
