"""
Configurações do projeto: limiares de estatística, thresholds e
campeonatos monitorados.

Ajuste esses valores conforme o que você quer acompanhar.
"""

import os

API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY", "")
API_FOOTBALL_HOST = "v3.football.api-sports.io"
API_FOOTBALL_BASE_URL = f"https://{API_FOOTBALL_HOST}"

# Percentual mínimo para um jogo entrar na lista final (0.8 = 80%)
THRESHOLD_PERCENT = 0.8

# Quantos jogos anteriores olhar por time, dentro do mesmo campeonato
LAST_N_GAMES = 10

# Linhas usadas para decidir se um jogo "bateu" o critério.
# Ex: OVER_CORNERS = 4.5 significa "jogo teve mais de 4.5 escanteios"
LINES = {
    "corners": 4.5,   # escanteios (por time, ajuste se preferir total da partida)
    "cards": 3.5,     # cartões (total da partida)
    "goals": 2.5,     # gols (total da partida)
}

# IDs de liga na API-Football (ver https://www.api-football.com/documentation-v3#tag/Leagues)
# Preencha com os campeonatos que você quer acompanhar.
LEAGUES = {
     "Serie A": 71,
     "Serie B": 72 
     "Premier League": 39,
     "La Liga": 140,
     "CONMEBOL Libertadores": 13,
     "CONMEBOL Sudamericana": 11,

}

# Temporada (ajustar a cada virada de ano/temporada)
SEASON = 2026

DATA_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "web", "data", "jogos.json"
)
