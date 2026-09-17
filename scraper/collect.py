"""
Busca os jogos do dia (para os campeonatos configurados) na API-Football.

Uso:
    python collect.py

Requer a variável de ambiente API_FOOTBALL_KEY.
"""

import sys
import datetime
import requests

from config import (
    API_FOOTBALL_BASE_URL,
    API_FOOTBALL_HOST,
    API_FOOTBALL_KEY,
    LEAGUES,
    SEASON,
)


def get_headers() -> dict:
    if not API_FOOTBALL_KEY:
        print("ERRO: variável de ambiente API_FOOTBALL_KEY não definida.", file=sys.stderr)
        sys.exit(1)
    return {
        "x-rapidapi-host": API_FOOTBALL_HOST,
        "x-rapidapi-key": API_FOOTBALL_KEY,
    }


def fetch_fixtures_today(league_id: int, season: int) -> list[dict]:
    """Busca os jogos de hoje para uma liga específica."""
    today = datetime.date.today().isoformat()
    url = f"{API_FOOTBALL_BASE_URL}/fixtures"
    params = {"league": league_id, "season": season, "date": today}

    resp = requests.get(url, headers=get_headers(), params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", [])


def collect_all() -> list[dict]:
    """Percorre todos os campeonatos configurados e junta os jogos do dia."""
    all_fixtures = []
    for league_name, league_id in LEAGUES.items():
        try:
            fixtures = fetch_fixtures_today(league_id, SEASON)
            for f in fixtures:
                f["_league_name"] = league_name
            all_fixtures.extend(fixtures)
            print(f"[collect] {league_name}: {len(fixtures)} jogo(s) hoje")
        except requests.RequestException as exc:
            print(f"[collect] Erro ao buscar {league_name}: {exc}", file=sys.stderr)
    return all_fixtures


if __name__ == "__main__":
    if not LEAGUES:
        print(
            "Nenhum campeonato configurado em config.py (dict LEAGUES). "
            "Adicione ao menos um antes de rodar.",
            file=sys.stderr,
        )
        sys.exit(1)

    fixtures = collect_all()
    print(f"Total de jogos coletados hoje: {len(fixtures)}")
