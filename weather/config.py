import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CACHE_TTL_SECONDS = 600  # 10 minutes
REQUEST_TIMEOUT_SECONDS = 5
MAX_RETRIES = 3
CACHE_FILE = "/tmp/weather_cache.json"
