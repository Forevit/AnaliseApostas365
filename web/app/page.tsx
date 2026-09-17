import jogos from "../data/jogos.json";

type TeamStats = {
  vitorias?: number;
  empates?: number;
  derrotas?: number;
  escanteios?: number;
  cartoes?: number;
  gols?: number;
};

type Game = {
  league?: string;
  home_team?: string;
  away_team?: string;
  home?: string;
  away?: string;
  home_stats?: TeamStats;
  away_stats?: TeamStats;
};

type Report = {
  generated_at?: string;
  total_matches_flagged?: number;
  total_fixtures_checked?: number;
  games?: Game[];
};

const report = jogos as Report;

const games = report.games ?? [];

function pct(value: number, total: number) {
  if (!total) return "0%";

  return `${Math.round((value / total) * 100)}%`;
}

function getTeamName(game: Game, side: "home" | "away") {
  if (side === "home") {
    return game.home_team ?? game.home ?? "Mandante";
  }

  return game.away_team ?? game.away ?? "Visitante";
}

function getStat(
  stats: TeamStats | undefined,
  key: keyof TeamStats
) {
  const value = stats?.[key];

  return value ?? "-";
}

function TeamStatsBlock({
  label,
  stats,
}: {
  label: string;
  stats?: TeamStats;
}) {
  return (
    <div className="team-stats">
      <div>{label}</div>

      <div>
        V {stats?.vitorias ?? 0} · E {stats?.empates ?? 0} · D{" "}
        {stats?.derrotas ?? 0}
      </div>
    </div>
  );
}

export default function Home() {
  const flagged = report.total_matches_flagged ?? games.length;
  const checked = report.total_fixtures_checked ?? games.length;

  const coverage = pct(flagged, checked);

  return (
    <div className="app">

      {/* HEADER */}

      <header className="topbar">
        <div className="topbar-inner">

          <div className="brand">
            <div className="brand-logo">⚽</div>

            <div className="brand-name">
              Análise <span>Apostas 365</span>
            </div>
          </div>

          <nav className="nav">
            <a className="nav-item active" href="#">
              Dashboard
            </a>

            <a className="nav-item" href="#">
              Jogos
            </a>

            <a className="nav-item" href="#">
              Estatísticas
            </a>

            <a className="nav-item" href="#">
              Histórico
            </a>
          </nav>

        </div>
      </header>

      {/* MAIN */}

      <main className="container">

        {/* HERO */}

        <section className="hero">

          <div className="hero-content">

            <div className="eyebrow">
              <span className="eyebrow-dot" />
              Monitoramento diário
            </div>

            <h1>
              Análise de jogos
              <br />
              <span>do dia</span>
            </h1>

            <p className="hero-description">
              Acompanhe as partidas identificadas pelo sistema
              com indicadores estatísticos para auxiliar na
              análise pré-jogo.
            </p>

          </div>

          <div className="updated">
            Última atualização:{" "}
            {report.generated_at
              ? new Date(report.generated_at).toLocaleString(
                  "pt-BR"
                )
              : "Não informado"}
          </div>

        </section>

        {/* KPIs */}

        <section className="kpi-grid">

          <div className="kpi-card">

            <div className="kpi-top">
              <span className="kpi-label">
                Jogos analisados
              </span>

              <span className="kpi-icon blue">
                ◉
              </span>
            </div>

            <div className="kpi-value">
              {checked}
            </div>

            <div className="kpi-description">
              Partidas verificadas pelo sistema
            </div>

          </div>

          <div className="kpi-card">

            <div className="kpi-top">
              <span className="kpi-label">
                Oportunidades
              </span>

              <span className="kpi-icon green">
                ✓
              </span>
            </div>

            <div className="kpi-value">
              {flagged}
            </div>

            <div className="kpi-description">
              Jogos que passaram pelos critérios
            </div>

          </div>

          <div className="kpi-card">

            <div className="kpi-top">
              <span className="kpi-label">
                Taxa de identificação
              </span>

              <span className="kpi-icon yellow">
                %
              </span>
            </div>

            <div className="kpi-value">
              {coverage}
            </div>

            <div className="kpi-description">
              Oportunidades em relação aos jogos analisados
            </div>

          </div>

        </section>

        {/* GAMES */}

        <section>

          <div className="section-header">

            <div>
              <h2 className="section-title">
                Partidas identificadas
              </h2>

              <p className="section-subtitle">
                Jogos encontrados na última coleta de dados
              </p>
            </div>

          </div>

          <div className="toolbar">

            <div className="search">
              <span className="search-icon">
                🔎
              </span>

              <input
                type="text"
                placeholder="Pesquisar time ou campeonato..."
              />
            </div>

            <select className="filter" defaultValue="all">
              <option value="all">
                Todos os campeonatos
              </option>
            </select>

          </div>

          {games.length === 0 ? (

            <div className="empty">

              <div className="empty-icon">
                ⚽
              </div>

              <div className="empty-title">
                Nenhum jogo encontrado
              </div>

              <div className="empty-description">
                O sistema ainda não encontrou partidas para
                exibir.
              </div>

            </div>

          ) : (

            <div className="games-grid">

              {games.map((game, index) => (

                <article
                  className="game-card"
                  key={`${getTeamName(game, "home")}-${getTeamName(
                    game,
                    "away"
                  )}-${index}`}
                >

                  <div className="game-header">

                    <span className="league">
                      {game.league ?? "Campeonato"}
                    </span>

                    <span className="status-badge">
                      Analisado
                    </span>

                  </div>

                  <div className="match">

                    <div className="teams">

                      <div className="team home">
                        {getTeamName(game, "home")}
                      </div>

                      <div className="vs">
                        VS
                      </div>

                      <div className="team">
                        {getTeamName(game, "away")}
                      </div>

                    </div>

                  </div>

                  <div className="stats-grid">

                    <div className="stat">

                      <div className="stat-label">
                        Gols
                      </div>

                      <div className="stat-value">
                        {getStat(
                          game.home_stats,
                          "gols"
                        )}{" "}
                        ×{" "}
                        {getStat(
                          game.away_stats,
                          "gols"
                        )}
                      </div>

                    </div>

                    <div className="stat">

                      <div className="stat-label">
                        Escanteios
                      </div>

                      <div className="stat-value">
                        {getStat(
                          game.home_stats,
                          "escanteios"
                        )}{" "}
                        ×{" "}
                        {getStat(
                          game.away_stats,
                          "escanteios"
                        )}
                      </div>

                    </div>

                    <div className="stat">

                      <div className="stat-label">
                        Cartões
                      </div>

                      <div className="stat-value">
                        {getStat(
                          game.home_stats,
                          "cartoes"
                        )}{" "}
                        ×{" "}
                        {getStat(
                          game.away_stats,
                          "cartoes"
                        )}
                      </div>

                    </div>

                    <div className="stat">

                      <div className="stat-label">
                        Campanha
                      </div>

                      <div className="stat-value">
                        {game.home_stats?.vitorias ?? 0}V
                        {" "}
                        {game.home_stats?.empates ?? 0}E
                        {" "}
                        {game.home_stats?.derrotas ?? 0}D
                      </div>

                    </div>

                  </div>

                </article>

              ))}

            </div>

          )}

        </section>

        {/* FOOTER */}

        <footer className="footer">
          Análise Apostas 365 · Dados estatísticos para
          análise esportiva
        </footer>

      </main>

    </div>
  );
}
