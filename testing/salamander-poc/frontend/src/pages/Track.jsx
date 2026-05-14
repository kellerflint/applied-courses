import { useState } from "react";

const API_BASE = "http://localhost:8000";

export default function Track() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [percent, setPercent] = useState(0);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setData(null);
    setPercent(0);

    try {
      // Kick off the job. The backend returns immediately.
      const form = new FormData();
      form.append("video", file);
      const startRes = await fetch(`${API_BASE}/track`, { method: "POST", body: form });
      if (!startRes.ok) throw new Error(`Start failed (${startRes.status})`);

      // Poll for progress every 1.5s until the job is done or fails.
      while (true) {
        await new Promise((r) => setTimeout(r, 1500));
        const jobRes = await fetch(`${API_BASE}/track`);
        if (!jobRes.ok) throw new Error(`Poll failed (${jobRes.status})`);
        const job = await jobRes.json();
        setPercent(job.percent ?? 0);
        if (job.status === "done") {
          setData(job.result);
          break;
        }
        if (job.status === "error") {
          throw new Error(job.message || "Backend error");
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <h1>Salamander Tracker</h1>
      <p className="lede">
        Upload a video. The backend runs YOLO with tracking on each frame, then
        returns the annotated video and how long each individual was on screen.
      </p>

      <form onSubmit={handleSubmit} className="uploader">
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? "Processing…" : "Run tracking"}
        </button>
      </form>

      {loading && (
        <p className="progress">
          <progress value={percent} max={100} /> {percent}%
        </p>
      )}

      {error && <p className="error">{error}</p>}

      {data && (
        <div className="results">
          <video src={data.video_url} controls playsInline />
          <p className="meta">
            {data.frame_count} frames &middot; {data.fps.toFixed(1)} fps &middot;{" "}
            {data.duration}s
          </p>
          <table className="metrics">
            <thead>
              <tr>
                <th>track id</th>
                <th>label</th>
                <th>time on screen</th>
              </tr>
            </thead>
            <tbody>
              {data.tracks.map((t) => (
                <tr key={t.track_id}>
                  <td>{t.track_id}</td>
                  <td>{t.label}</td>
                  <td>{t.time_on_screen_s}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
