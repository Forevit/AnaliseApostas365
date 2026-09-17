"""
Gera o JSON final consumido pelo frontend.

Fluxo:
    1. Busca os jogos do dia.
    2. Busca o histórico dos times.
    3. Calcula os indicadores estatísticos.
    4. Filtra os jogos que possuem pelo menos um sinal.
    5. Salva em web/data/jogos.json.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from cache import TeamHistoryCache
from collect import collect_all
from config import DATA_OUTPUT_PATH, LEAGUES, SEASON
from stats import calculate_team_history, passes_threshold


def build_game(fixture: dict, cache: TeamHistoryCache) -> dict | None:
    """
    Monta a estrutura de um jogo para o frontend.
    """

    fixture_data = fixture.get("fixture", {})
    teams = fixture.get("teams", {})

    home = teams.get("home", {})
    away = teams.get("away", {})

    home_id = home.get("id")
    away_id = away.get("id")

    if not home_id or not away_id:
        return None

    league_id = fixture.get("league", {}).get("id")

    if not league_id:
        return None

    # Histórico do mandante
    if home_id not in cache:
        cache.set(
            home_id,
            calculate_team_history(
                home_id,
                league_id,
                SEASON,
            ),
        )

    # Histórico do visitante
    if away_id not in cache:
        cache.set(
            away_id,
            calculate_team_history(
                away_id,
                league_id,
                SEASON,
            ),
        )

    home_stats = cache.get(home_id)
    away_stats = cache.get(away_id)

    if not home_stats or not away_stats:
        return None

    home_signal = passes_threshold(home_stats)
    away_signal = passes_threshold(away_stats)

    # Só entra no JSON se algum dos dois times
    # apresentar pelo menos um critério acima do threshold.
    if not home_signal and not away_signal:
        return None

    signals = {
        "corners": (
            home_stats.get("corners_pct", 0) >= 0.8
            or away_stats.get("corners_pct", 0) >= 0.8
        ),
        "cards": (
            home_stats.get("cards_pct", 0) >= 0.8
            or away_stats.get("cards_pct", 0) >= 0.8
        ),
        "goals": (
            home_stats.get("goals_pct", 0) >= 0.8
            or away_stats.get("goals_pct", 0) >= 0.8
        ),
    }

    return {
        "fixture_id": fixture_data.get("id"),
        "league": fixture.get("_league_name")
        or fixture.get("league", {}).get("name", "Desconhecida"),
        "league_id": league_id,
        "date": fixture_data.get("date"),
        "status": fixture_data.get("status", {}).get("short"),
        "home_team": home.get("name"),
        "away_team": away.get("name"),
        "home_team_id": home_id,
        "away_team_id": away_id,
        "home": home_stats,
        "away": away_stats,
        "signals": signals,
    }


def save_json(data: dict) -> None:
    """
    Salva o JSON garantindo que a pasta de destino exista.
    """

    output_path = Path(DATA_OUTPUT_PATH)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"[save_json] Arquivo salvo em: {output_path}")


def main() -> None:
    print("[save_json] Iniciando coleta...")

    fixtures = collect_all()

    print(
        f"[save_json] Total de partidas encontradas: "
        f"{len(fixtures)}"
    )

    cache = TeamHistoryCache()

    games = []

    for index, fixture in enumerate(fixtures, start=1):
        try:
            game = build_game(
                fixture,
                cache,
            )

            if game:
                games.append(game)

            print(
                f"[save_json] Processado "
                f"{index}/{len(fixtures)}"
            )

        except Exception as exc:
            fixture_id = (
                fixture.get("fixture", {}).get("id", "desconhecido")
            )

            print(
                f"[save_json] Erro no fixture {fixture_id}: {exc}",
                file=sys.stderr,
            )

    games.sort(
        key=lambda game: game.get("date") or ""
    )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "season": SEASON,
        "leagues": list(LEAGUES.keys()),
        "total_fixtures_checked": len(fixtures),
        "total_matches_flagged": len(games),
        "games": games,
    }

    save_json(output)

    print(
        f"[save_json] Finalizado: "
        f"{len(games)} partida(s) sinalizada(s)."
    )


if __name__ == "__main__":
    main()
