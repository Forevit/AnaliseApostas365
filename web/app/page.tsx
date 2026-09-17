import jogosData from "../data/jogos.json";

type TeamStats = {
  sample_size: number;
  win_pct?: number;
  draw_pct?: number;
  loss_pct?: number;
  corners_pct?: number;
  cards_pct?: number;
  goals_pct?: number;
};

type Game = {
  fixture_id: number;
  date: string;
  league: string;
  home_team: string;
  away_team: string;
  home_stats: TeamStats;
  away_stats: TeamStats;
};

type Report = {
  generated_at: string | null;
  total_fixtures_checked: number;
  total_matches_flagged: number;
  games: Game[];
};

const report = jogosData as Report;

function pct(value?: number): string {
  if (value === undefined) return "-";
  return `${Math.round(value * 100)}%`;
}

function TeamStatsBlock({ label, stats }: { label: string; stats: TeamStats }) {
  return (
    <div style={{ flex: 1 }}>
      <strong>{label}</strong>
      <ul style={{ listStyle: "none", padding: 0, margin: "4px 0" }}>
        <li>V/E/D: {pct(stats.win_pct)} / {pct(stats.draw_pct)} / {pct(stats.loss_pct)}</li>
        <li>Escanteios: {pct(stats.corners_pct)}</li>
        <li>Cartões: {pct(stats.cards_pct)}</li>
        <li>Gols: {pct(stats.goals_pct)}</li>
      </ul>
    </div>
  );
}

export default function Home() {
  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 24, fontFamily: "sans-serif" }}>
      <h1>Jogos do dia</h1>
      <p style={{ color: "#666" }}>
        {report.generated_at
          ? `Atualizado em ${new Date(report.generated_at).toLocaleString("pt-BR")}`
          : "Ainda sem dados coletados."}
        {" — "}
        {report.total_matches_flagged} de {report.total_fixtures_checked} jogos acima do critério
      </p>

      {report.games.length === 0 && <p>Nenhum jogo passou do critério hoje.</p>}

      {report.games.map((game) => (
        <div
          key={game.fixture_id}
          style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, marginBottom: 16 }}
        >
          <div style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>{game.league}</div>
          <h3 style={{ margin: "0 0 12px" }}>
            {game.home_team} x {game.away_team}
          </h3>
          <div style={{ display: "flex", gap: 24 }}>
            <TeamStatsBlock label={game.home_team} stats={game.home_stats} />
            <TeamStatsBlock label={game.away_team} stats={game.away_stats} />
          </div>
        </div>
      ))}
    </main>
  );
}
