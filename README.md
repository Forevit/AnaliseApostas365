# Projeto Jogos — Análise diária (escanteios, cartões, gols)

Lista diária de jogos filtrados por critérios estatísticos dos últimos 10 jogos
de cada time no mesmo campeonato: % de vitória/empate/derrota e % de jogos que
bateram linhas de escanteios, cartões e gols.

## Como funciona

1. Todo dia, o GitHub Actions (`.github/workflows/daily-collect.yml`) roda os
   scripts em `scraper/`.
2. Eles buscam os jogos do dia na API-Football, calculam o histórico de cada
   time no campeonato e filtram os que passaram de 80% em algum critério.
3. O resultado é gravado em `web/data/jogos.json` e commitado de volta no repo.
4. A Vercel detecta o push e faz redeploy automático do site.

## Setup

### 1. API-Football

Crie uma conta gratuita em https://www.api-football.com/ (ou via RapidAPI) e
pegue sua chave. O plano free tem limite de 100 requisições/dia — de olho na
quantidade de campeonatos/times configurados, porque cada time consultado gera
várias chamadas (1 para os últimos jogos + 1 por partida para estatísticas).

### 2. Configurar campeonatos

Edite `scraper/config.py` e preencha o dicionário `LEAGUES` com os IDs dos
campeonatos que você quer acompanhar (ver documentação da API-Football).
Ajuste também `LINES` (linhas de escanteios/cartões/gols) e `THRESHOLD_PERCENT`
se quiser outro corte que não 80%.

### 3. Secret no GitHub

No repositório: Settings → Secrets and variables → Actions → New repository
secret, nome `API_FOOTBALL_KEY`, valor a sua chave.

### 4. Deploy na Vercel

Importe o repositório na Vercel, apontando o **Root Directory** para `web/`.
Não precisa de variáveis de ambiente no frontend — ele só lê o JSON estático.

### 5. Rodar localmente (teste)

```bash
cd scraper
pip install -r requirements.txt
export API_FOOTBALL_KEY=sua_chave_aqui
python save_json.py
```

```bash
cd web
npm install
npm run dev
```

## Próximos passos sugeridos

- Ajustar `LINES` por campeonato (linhas diferentes para ligas diferentes)
- Guardar histórico por dia (`data/2026-09-17.json`) em vez de sobrescrever
- Cachear estatísticas de partidas já processadas pra economizar requisições
  da API (hoje o script busca de novo tudo a cada rodada)
