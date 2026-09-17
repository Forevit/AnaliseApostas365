"""
Para cada time de um jogo do dia, busca os últimos N jogos dele NO MESMO
CAMPEONATO e calcula:
  - % desses jogos que bateram cada linha (escanteios, cartões, gols)
  - % de vitória / empate / derrota

Depois filtra e devolve só os jogos do dia em que pelo menos um critério
passou do THRESHOLD_PERCENT.
"""

import sys
import requests

from config import (
    API_FOOTBALL_BASE_URL,
    API_FOOTBALL_HOST,
    API_FOOTBALL_KEY,
    LAST_N_GAMES,
    LINES,
    THRESHOLD_PERCENT,
)


def get_headers() -> dict:
    return {
        "x-rapidapi-host": API_FOOTBALL_HOST,
        "x-rapidapi-key": API_FOOTBALL_KEY,
    }


def fetch_last_games(team_id: int, league_id: int, season: int, last_n: int = LAST_N_GAMES) -> list[dict]:
    """Busca os últimos N jogos finalizados de um time num campeonato."""
    url = f"{API_FOOTBALL_BASE_URL}/fixtures"
    params = {
        "team": team_id,
        "league": league_id,
        "season": season,
        "last": last_n,
    }
    resp = requests.get(url, headers=get_headers(), params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("response", [])


def fetch_fixture_statistics(fixture_id: int) -> list[dict]:
    """Busca estatísticas (escanteios, cartões etc.) de uma partida específica."""
    url = f"{API_FOOTBALL_BASE_URL}/fixtures/statistics"
    params = {"fixture": fixture_id}
    resp = requests.get(url, headers=get_headers(), params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("response", [])


def _extract_stat_value(stats_response: list[dict], stat_name: str) -> float:
    """Soma o valor de uma estatística (ex: 'Corner Kicks') entre os dois times."""
    total = 0.0
    for team_stats in stats_response:
        for item in team_stats.get("statistics", []):
            if item.get("type", "").lower() == stat_name.lower():
                value = item.get("value")
                if isinstance(value, (int, float)):
                    total += value
                elif isinstance(value, str) and value.isdigit():
                    total += int(value)
    return total


def calculate_team_history(team_id: int, league_id: int, season: int) -> dict:
    """
    Calcula, para um time, dentro do campeonato informado:
      - % dos últimos N jogos que bateram cada linha configurada
      - % de vitória / empate / derrota
    """
    games = fetch_last_games(team_id, league_id, season)
    n = len(games)
    if n == 0:
        return {"sample_size": 0}

    wins = draws = losses = 0
    hits = {key: 0 for key in LINES}

    for game in games:
        fixture_id = game["fixture"]["id"]
        home_id = game["teams"]["home"]["id"]
        winner_home = game["teams"]["home"].get("winner")
        winner_away = game["teams"]["away"].get("winner")

        # Resultado do ponto de vista do time analisado
        is_home = home_id == team_id
        if winner_home is None and winner_away is None:
            draws += 1
        elif (is_home and winner_home) or (not is_home and winner_away):
            wins += 1
        else:
            losses += 1

        goals_total = (game["goals"]["home"] or 0) + (game["goals"]["away"] or 0)
        hits["goals"] += goals_total > LINES["goals"]

        # Escanteios e cartões exigem uma chamada extra de estatísticas
        stats_response = fetch_fixture_statistics(fixture_id)
        corners_total = _extract_stat_value(stats_response, "Corner Kicks")
        cards_total = _extract_stat_value(stats_response, "Yellow Cards") + _extract_stat_value(
            stats_response, "Red Cards"
        )
        hits["corners"] += corners_total > LINES["corners"]
        hits["cards"] += cards_total > LINES["cards"]

    return {
        "sample_size": n,
        "win_pct": wins / n,
        "draw_pct": draws / n,
        "loss_pct": losses / n,
        "corners_pct": hits["corners"] / n,
        "cards_pct": hits["cards"] / n,
        "goals_pct": hits["goals"] / n,
    }


def passes_threshold(team_history: dict) -> bool:
    """True se algum critério (escanteios/cartões/gols) passou do threshold."""
    return any(
        team_history.get(f"{key}_pct", 0) >= THRESHOLD_PERCENT for key in LINES
    )


if __name__ == "__main__":
    print(
        "Este módulo é usado como biblioteca por save_json.py. "
        "Rode 'python save_json.py' para gerar o JSON final.",
        file=sys.stderr,
    )
