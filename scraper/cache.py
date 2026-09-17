"""In-memory cache used during a single scraper execution."""

from __future__ import annotations

from typing import Any, Dict


class TeamHistoryCache:
    def __init__(self) -> None:
        self._history: Dict[int, Any] = {}

    def get(self, team_id: int):
        return self._history.get(team_id)

    def set(self, team_id: int, value: Any) -> None:
        self._history[team_id] = value

    def __contains__(self, team_id: int) -> bool:
        return team_id in self._history

    def clear(self) -> None:
        self._history.clear()
