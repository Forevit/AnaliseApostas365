# AnaliseApostas365

Projeto de coleta e exibição de análises estatísticas de partidas de futebol.

## Arquitetura

- `scraper/`: Python + API-Football.
- `web/`: Next.js.
- GitHub Actions: executa a coleta diariamente.
- Vercel: publica o frontend.
- `web/data/jogos.json`: dados consumidos pelo frontend.

## API-Football

Este projeto usa **API-Football diretamente pela API-Sports**, em:

`https://v3.football.api-sports.io`

A chave deve ficar somente em variável de ambiente:

```text
API_FOOTBALL_KEY
```

### GitHub Actions

No repositório:

**Settings → Secrets and variables → Actions → New repository secret**

Crie:

```text
Name: API_FOOTBALL_KEY
Value: sua_chave
```

Nunca coloque a chave no código ou no Git.

## Vercel

Configure o projeto apontando o **Root Directory** para:

```text
web
```

A Vercel deve cuidar apenas do Next.js. O Python é executado pelo GitHub Actions.

## Execução local

```bash
cd scraper
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Defina `API_FOOTBALL_KEY` e execute:

```bash
python collect.py
```

## Consumo da API

O coletor usa cache em memória por time para evitar buscar repetidamente o mesmo histórico durante uma execução.

Isso reduz chamadas desnecessárias, mas **não elimina o limite diário da API-Football**. A quantidade de partidas, ligas e estatísticas coletadas deve ser compatível com a franquia da sua conta.

## Importante

Os dados são estatísticos e não representam garantia de resultado. O projeto não deve ser interpretado como recomendação de aposta.
