import { useEffect, useRef, useState } from "react";
import { postVideo, absoluteVideoUrl } from "../api.js";

// "Detect" page: hits POST /detect on the backend. Plays the annotated
// video, shows the live coordinates of every detection in the current
// frame, and renders a small line chart of detection count over time.
//
// This page does NOT use tracking. Each frame is processed independently,
// so the same salamander has no identity from frame to frame.
export default function Detect() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null); // { video_url, fps, frames, ... }

  // currentFrame is the frame index the video is currently displaying.
  // We update it on the <video>'s timeupdate event so the coordinates
  // and chart highlight stay in sync.
  const videoRef = useRef(null);
  const [currentFrame, setCurrentFrame] = useState(0);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setData(null);
    setCurrentFrame(0);
    try {
      const result = await postVideo("/detect", file);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Wire up the timeupdate listener once data lands. Convert the video's
  // currentTime into a frame index using the fps the backend reported.
  useEffect(() => {
    const v = videoRef.current;
    if (!v || !data) return;
    function onTime() {
      const idx = Math.min(
        data.frames.length - 1,
        Math.floor(v.currentTime * data.fps)
      );
      setCurrentFrame(idx);
    }
    v.addEventListener("timeupdate", onTime);
    return () => v.removeEventListener("timeupdate", onTime);
  }, [data]);

  const frame = data?.frames?.[currentFrame];

  return (
    <div className="page">
      <h1>Detect (per-frame, no tracking)</h1>
      <p className="lede">
        Upload a video. The backend runs YOLO on each frame and returns the
        annotated video plus the bounding box of every detection. No track
        IDs. If a salamander leaves the frame and comes back, it's a new
        detection.
      </p>

      <form onSubmit={handleSubmit} className="uploader">
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? "Processing…" : "Run detection"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {data && (
        <div className="results">
          <div className="video-col">
            <video
              ref={videoRef}
              src={absoluteVideoUrl(data.video_url)}
              controls
              playsInline
            />
            <p className="meta">
              {data.frame_count} frames &middot; {data.fps.toFixed(1)} fps
              &middot; {data.width}&times;{data.height}
            </p>
          </div>

          <div className="metrics-col">
            <section className="card">
              <h2>Live coordinates</h2>
              <p className="muted">
                Frame {currentFrame} &middot; {frame?.detections.length ?? 0}{" "}
                detection{frame?.detections.length === 1 ? "" : "s"}
              </p>
              <table className="coords">
                <thead>
                  <tr>
                    <th>label</th>
                    <th>cx</th>
                    <th>cy</th>
                    <th>conf</th>
                  </tr>
                </thead>
                <tbody>
                  {frame?.detections.length ? (
                    frame.detections.map((d, i) => (
                      <tr key={i}>
                        <td>{d.label}</td>
                        <td>{d.cx}</td>
                        <td>{d.cy}</td>
                        <td>{d.conf}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="muted">
                        (nothing detected this frame)
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </section>

            <section className="card">
              <h2>Detection count over time</h2>
              <CountChart frames={data.frames} currentFrame={currentFrame} />
            </section>
          </div>
        </div>
      )}
    </div>
  );
}

// Tiny inline SVG line chart: x = frame index, y = detection count.
// A vertical line marks the frame the video is currently showing.
function CountChart({ frames, currentFrame }) {
  const W = 480;
  const H = 140;
  const PAD = 24;

  if (!frames?.length) return null;

  const counts = frames.map((f) => f.detections.length);
  const maxCount = Math.max(1, ...counts);

  const x = (i) => PAD + (i / Math.max(1, frames.length - 1)) * (W - 2 * PAD);
  const y = (c) => H - PAD - (c / maxCount) * (H - 2 * PAD);

  const points = counts.map((c, i) => `${x(i)},${y(c)}`).join(" ");
  const cursorX = x(currentFrame);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="chart">
      {/* axes */}
      <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} className="axis" />
      <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} className="axis" />

      {/* y label: max count */}
      <text x={4} y={PAD + 4} className="tick">
        {maxCount}
      </text>
      <text x={4} y={H - PAD} className="tick">
        0
      </text>

      {/* the line */}
      <polyline points={points} className="series" />

      {/* current-frame cursor */}
      <line
        x1={cursorX}
        x2={cursorX}
        y1={PAD}
        y2={H - PAD}
        className="cursor"
      />
    </svg>
  );
}
