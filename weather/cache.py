import json
import time
from typing import Optional

from . import config


def _load() -> dict:
    try:
        with open(config.CACHE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}



def _save(store: dict) -> None:
    with open(config.CACHE_FILE, "w") as f:
        json.dump(store, f)


def get(city: str) -> Optional[dict]:
    store = _load()
    entry = store.get(city.lower())
    if not entry:
        return None
    if time.time() - entry["timestamp"] > config.CACHE_TTL_SECONDS:
        return None  # expired — caller will fetch fresh
    return entry["data"]


def get_stale(city: str) -> Optional[dict]:
    """Return cached data even if expired — used as fallback when API is down."""
    store = _load()
    entry = store.get(city.lower())
    return entry["data"] if entry else None


def set(city: str, data: dict) -> None:
    store = _load()
    store[city.lower()] = {"timestamp": time.time(), "data": data}
    _save(store)
