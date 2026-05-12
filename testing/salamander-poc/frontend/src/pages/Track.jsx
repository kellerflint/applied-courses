import { useState } from "react";
import { postVideo, absoluteVideoUrl } from "../api.js";

// "Track" page: hits POST /track on the backend. The backend uses
// model.track() so each detection carries a stable track_id across
// frames. The response includes per-track aggregate metrics
// (total distance traveled, time on screen) that we render in a table.
export default function Track() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const result = await postVideo("/track", file);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <h1>Track (per-individual metrics)</h1>
      <p className="lede">
        Same model, different mode. <code>model.track()</code> assigns each
        detection a stable ID across frames, so the backend can compute
        per-salamander metrics: total pixels traveled and total time on
        screen.
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

      {error && <p className="error">{error}</p>}

      {data && (
        <div className="results">
          <div className="video-col">
            <video
              src={absoluteVideoUrl(data.video_url)}
              controls
              playsInline
            />
            <p className="meta">
              {data.frame_count} frames &middot; {data.fps.toFixed(1)} fps
              &middot; {data.duration}s total
            </p>
          </div>

          <div className="metrics-col">
            <section className="card">
              <h2>Per-salamander metrics</h2>
              {data.tracks.length === 0 ? (
                <p className="muted">No tracks recorded.</p>
              ) : (
                <table className="coords">
                  <thead>
                    <tr>
                      <th>track id</th>
                      <th>label</th>
                      <th>distance (px)</th>
                      <th>time on screen</th>
                      <th>frames seen</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.tracks.map((t) => (
                      <tr key={t.track_id}>
                        <td>{t.track_id}</td>
                        <td>{t.label}</td>
                        <td>{t.total_distance_px}</td>
                        <td>{t.time_on_screen_s}s</td>
                        <td>{t.frames_seen}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </section>
          </div>
        </div>
      )}
    </div>
  );
}
