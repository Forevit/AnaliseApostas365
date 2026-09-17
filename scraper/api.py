"""API-Football client.

Direct API-Sports/API-Football access (v3.football.api-sports.io).
Authentication is read from API_FOOTBALL_KEY and is never stored in source.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import requests


BASE_URL = "https://v3.football.api-sports.io"
API_KEY = os.getenv("API_FOOTBALL_KEY", "").strip()

if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY não configurada.")

SESSION = requests.Session()
SESSION.headers.update({
    "x-apisports-key": API_KEY,
    "Accept": "application/json",
})

# Small retry policy for transient API/rate-limit responses.
MAX_RETRIES = 3
BACKOFF_SECONDS = 2.0


def api_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """GET an API-Football endpoint with basic retry/error handling."""
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    last_error: Optional[Exception] = None

    for attempt in range(MAX_RETRIES):
        try:
            response = SESSION.get(url, params=params or {}, timeout=30)

            if response.status_code in (429, 500, 502, 503, 504):
                if attempt < MAX_RETRIES - 1:
                    time.sleep(BACKOFF_SECONDS * (attempt + 1))
                    continue

            response.raise_for_status()
            data = response.json()

            errors = data.get("errors")
            if errors:
                raise RuntimeError(f"API-Football retornou erro: {errors}")

            return data

        except (requests.RequestException, ValueError, RuntimeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(BACKOFF_SECONDS * (attempt + 1))
            else:
                break

    raise RuntimeError(f"Falha na API-Football: {last_error}")


def get_fixtures_by_date(date: str, league_id: Optional[int] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {"date": date}
    if league_id is not None:
        params["league"] = league_id
    return api_get("fixtures", params)


def get_team_last_fixtures(team_id: int, last: int = 10) -> Dict[str, Any]:
    return api_get("fixtures", {"team": team_id, "last": last})


def get_fixture_statistics(fixture_id: int) -> Dict[str, Any]:
    return api_get("fixtures/statistics", {"fixture": fixture_id})
