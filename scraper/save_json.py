"""
Orquestra o pipeline do dia:
  1. Busca os jogos do dia (collect.py)
  2. Para cada time, calcula o histórico dos últimos N jogos (stats.py)
  3. Filtra só os jogos com algum critério >= THRESHOLD_PERCENT
  4. Grava tudo em web/data/jogos.json

Rodado diariamente pelo GitHub Actions.
"""

import json
import datetime

from config import DATA_OUTPUT_PATH, SEASON
from collect import collect_all
from stats import calculate_team_history, passes_threshold


def build_report() -> dict:
    fixtures = collect_all()
    results = []

    for fixture in fixtures:
        league_id = fixture["league"]["id"]
        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]

        home_history = calculate_team_history(home["id"], league_id, SEASON)
        away_history = calculate_team_history(away["id"], league_id, SEASON)

        if not (passes_threshold(home_history) or passes_threshold(away_history)):
            continue

        results.append(
            {
                "fixture_id": fixture["fixture"]["id"],
                "date": fixture["fixture"]["date"],
                "league": fixture.get("_league_name", fixture["league"]["name"]),
                "home_team": home["name"],
                "away_team": away["name"],
                "home_stats": home_history,
                "away_stats": away_history,
            }
        )

    return {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_fixtures_checked": len(fixtures),
        "total_matches_flagged": len(results),
        "games": results,
    }


if __name__ == "__main__":
    report = build_report()
    with open(DATA_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Gravado: {DATA_OUTPUT_PATH} ({report['total_matches_flagged']} jogo(s) filtrado(s))")
