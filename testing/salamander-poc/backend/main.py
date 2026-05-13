"""Salamander Tracker backend. POST /track kicks off a YOLO tracking job
on the uploaded video. GET /track/{job_id} polls for progress and the
final result. Processing happens on a background thread so the POST
returns immediately and the browser polls instead of holding a long
connection open."""

from __future__ import annotations

import math
import shutil
import uuid
from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Thread

import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

MODEL_PATH = str(Path(__file__).parent.parent / "data" / "yolov8n.pt")
model = YOLO(MODEL_PATH)
class_names = model.names


app = FastAPI(title="Salamander Tracker POC")

# Allow the Vite dev server (and a couple of other common dev ports) to
# call the API and load the annotated mp4.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")


@app.get("/")
def root() -> dict:
    return {"ok": True, "endpoints": ["/track"]}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _save_upload_to_tempfile(upload: UploadFile) -> Path:
    suffix = Path(upload.filename or "input.mp4").suffix or ".mp4"
    tmp = NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        shutil.copyfileobj(upload.file, tmp)
    finally:
        tmp.close()
    return Path(tmp.name)


def _open_video(path: Path) -> tuple[cv2.VideoCapture, float, int, int, int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open uploaded video")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return cap, fps, width, height, total


def _make_writer(path: Path, fps: float, width: int, height: int) -> cv2.VideoWriter:
    # Prefer H.264 (avc1) so the mp4 plays in browsers. Fall back to mp4v
    # for OpenCV builds without H.264 support.
    for codec in ("avc1", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
        if writer.isOpened():
            return writer
    raise HTTPException(status_code=500, detail="Could not open video writer")


def _new_output_path() -> tuple[Path, str]:
    name = f"{uuid.uuid4().hex}.mp4"
    return OUTPUTS_DIR / name, f"http://localhost:8000/outputs/{name}"


def _log_progress(prefix: str, frame_idx: int, total: int) -> None:
    # flush=True so the line shows up immediately instead of waiting for
    # the request to finish.
    if frame_idx % 30 == 0 or frame_idx == total:
        pct = (frame_idx / total) * 100 if total > 0 else 0
        print(f"  {prefix} {frame_idx}/{total} ({pct:.0f}%)", flush=True)


# ---------------------------------------------------------------------------
# /track
# ---------------------------------------------------------------------------


class TrackAggregator:
    """Builds per-track aggregate metrics as frames stream in.

    For each track_id seen across frames, accumulates:
      distance     -- total pixels traveled (sum of frame-to-frame moves)
      frames_seen  -- how many frames the track was visible
      label        -- its class name

    Lifecycle: create, update(...) once per frame, summarize(fps) at end.
    """

    def __init__(self):
        self.distance: dict[int, float] = defaultdict(float)
        self.frames_seen: dict[int, int] = defaultdict(int)
        self.last_xy: dict[int, tuple[float, float]] = {}
        self.label_for: dict[int, str] = {}

    def update(self, result) -> None:
        boxes = result.boxes
        if boxes is None or len(boxes) == 0 or boxes.id is None:
            return

        xyxy = boxes.xyxy.cpu().numpy()
        ids = boxes.id.cpu().numpy().astype(int)
        cls_ids = boxes.cls.cpu().numpy().astype(int)

        for (x1, y1, x2, y2), tid, cls_id in zip(xyxy, ids, cls_ids):
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            if tid in self.last_xy:
                px, py = self.last_xy[tid]
                self.distance[tid] += math.hypot(cx - px, cy - py)

            self.last_xy[tid] = (cx, cy)
            self.frames_seen[tid] += 1
            self.label_for[tid] = class_names.get(int(cls_id), str(cls_id))

    def summarize(self, fps: float) -> list[dict]:
        tracks = [
            {
                "track_id": int(tid),
                "total_distance_px": round(self.distance[tid], 1),
                "time_on_screen_s": round(count / fps, 2) if fps else 0.0,
                "frames_seen": int(count),
                "label": self.label_for.get(tid, "?"),
            }
            for tid, count in self.frames_seen.items()
        ]
        tracks.sort(key=lambda t: t["frames_seen"], reverse=True)
        return tracks


# In-memory job store. A real app would back this with Redis/a database.
# For a POC, a process-local dict is fine: server restart clears it.
# Each entry looks like one of:
#   {"status": "processing", "percent": 47}
#   {"status": "done", "percent": 100, "result": {...}}
#   {"status": "error", "message": "..."}
jobs: dict[str, dict] = {}


def _run_track_job(job_id: str, input_path: Path) -> None:
    """Background worker. Updates jobs[job_id] as it processes frames."""
    try:
        cap, fps, width, height, total = _open_video(input_path)
        output_path, output_url = _new_output_path()
        writer = _make_writer(output_path, fps, width, height)

        print(
            f"[track {job_id[:8]}] {total} frames at {width}x{height} @ {fps:.1f}fps "
            f"-> {output_path.name}",
            flush=True,
        )

        aggregator = TrackAggregator()
        frame_idx = 0

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # persist=True keeps tracker state across calls so IDs stay
                # stable across frames.
                result = model.track(frame, persist=True, verbose=False)[0]
                writer.write(result.plot())
                aggregator.update(result)

                frame_idx += 1
                jobs[job_id]["percent"] = int(frame_idx / total * 100) if total else 0
                _log_progress(f"[track {job_id[:8]}]", frame_idx, total)
        finally:
            cap.release()
            writer.release()

        tracks = aggregator.summarize(fps)
        print(
            f"[track {job_id[:8]}] done. {frame_idx} frames, {len(tracks)} unique track id(s)",
            flush=True,
        )

        jobs[job_id] = {
            "status": "done",
            "percent": 100,
            "result": {
                "video_url": output_url,
                "fps": fps,
                "frame_count": frame_idx,
                "width": width,
                "height": height,
                "duration": round(frame_idx / fps, 2) if fps else 0.0,
                "tracks": tracks,
            },
        }
    except Exception as e:
        print(f"[track {job_id[:8]}] error: {e}", flush=True)
        jobs[job_id] = {"status": "error", "message": str(e)}
    finally:
        input_path.unlink(missing_ok=True)


@app.post("/track")
def start_track(video: UploadFile = File(...)) -> dict:
    """Accept the upload, register a job, return its id immediately.
    The frontend polls GET /track/{job_id} for progress and the result."""
    job_id = uuid.uuid4().hex
    jobs[job_id] = {"status": "processing", "percent": 0}
    input_path = _save_upload_to_tempfile(video)
    Thread(target=_run_track_job, args=(job_id, input_path), daemon=True).start()
    return {"job_id": job_id, "status": "processing"}


@app.get("/track/{job_id}")
def get_track(job_id: str) -> dict:
    """Poll endpoint. Returns the current state of a job."""
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


# ---------------------------------------------------------------------------
# Run the server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
