import { useState, useEffect } from "react";

const API = "http://localhost:8000";

// Types for API responses
interface TrackRow {
  id: number;
  name: string;
  artist: string;
  album?: string | null;
  release_year?: number | null;
}

interface Stats {
  artists: number;
  tracks: number;
}

export default function App() {
  // Search state
  const [q, setQ] = useState("ken");
  const [rows, setRows] = useState<TrackRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  // Stats state
  const [stats, setStats] = useState<Stats | null>(null);

  // Fetch stats on page load
  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await fetch(`${API}/api/stats/overview`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: Stats = await res.json();
        setStats(data);
      } catch (e) {
        if (e instanceof Error) {
          console.error("Stats fetch failed:", e.message);
        } else {
          console.error("Stats fetch failed:", e);
        }
      }
    }
    fetchStats();
  }, []);

  // Search API call
  async function search() {
    setLoading(true);
    setErr(null);
    try {
      const res = await fetch(
        `${API}/api/tracks/search?q=${encodeURIComponent(q)}`
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: TrackRow[] = await res.json();
      setRows(data);
    } catch (e) {
      if (e instanceof Error) {
        setErr(e.message);
      } else {
        setErr(String(e));
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>🎵 TrackStack</h1>

      {/* Stats section */}
      {stats ? (
        <p>
          <strong>{stats.artists}</strong> artists ·{" "}
          <strong>{stats.tracks}</strong> tracks
        </p>
      ) : (
        <p>Loading stats…</p>
      )}

      {/* Search section */}
      <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search tracks or artists..."
        />
        <button onClick={search} disabled={loading}>
          {loading ? "Searching…" : "Search"}
        </button>
      </div>

      {err && <p style={{ color: "crimson" }}>Error: {err}</p>}

      {/* Results */}
      <ul style={{ marginTop: 16 }}>
        {rows.map((r) => (
          <li key={r.id}>
            {r.name} — {r.artist}
            {r.album ? ` (${r.album})` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}