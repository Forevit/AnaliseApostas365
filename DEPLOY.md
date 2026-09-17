# Checklist de deploy

## GitHub

1. Suba todo o conteúdo deste projeto.
2. Em **Settings → Secrets and variables → Actions**, crie `API_FOOTBALL_KEY`.
3. Abra **Actions → Atualizar análises diariamente**.
4. Use **Run workflow** para testar manualmente.
5. Confirme que `web/data/jogos.json` foi atualizado.

## Vercel

1. Importe o repositório.
2. Defina **Root Directory** como `web`.
3. Framework: Next.js (detecção automática).
4. Faça o deploy.
5. Depois do primeiro deploy, confira se a página lê `data/jogos.json`.

## Se o GitHub Action falhar

Confira primeiro:
- `API_FOOTBALL_KEY` existe como secret.
- a chave é válida;
- a conta API-Football tem franquia disponível;
- o erro não é de limite `429`;
- `scraper/requirements.txt` instala normalmente.
