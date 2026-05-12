"""
Salamander Tracker backend (proof-of-concept).

Two endpoints, both synchronous:

- POST /detect  -- runs model.predict() on each frame. Returns the annotated
                   video URL plus per-frame detection data. The frontend uses
                   this for the "live coordinates readout" and the
                   "detection count over time" chart.

- POST /track   -- runs model.track() on each frame so each detection gets a
                   stable track_id. Returns the annotated video URL plus a
                   per-track summary (total distance traveled, time on screen).

Annotated videos are written to ./outputs/ and served at /outputs/<name>.mp4
as static files.

The default model is yolov8n.pt (COCO classes). Swap MODEL_PATH below to
point at a custom-trained salamander model.
"""

from __future__ import annotations

import math
import shutil
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Folder where annotated videos are written and served from.
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

# Default to the YOLO weights sitting at the poc root. When a student trains
# their own salamander model, they swap this path for runs/detect/.../best.pt.
MODEL_PATH = str(Path(__file__).parent.parent / "yolov8n.pt")

# Load the model once at startup so each request reuses the same instance.
# Ultralytics auto-downloads yolov8n.pt if it isn't on disk yet.
model = YOLO(MODEL_PATH)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="Salamander Tracker POC")

# Vite dev server runs on 5173. Allow it (and a few other common dev ports)
# to call the API and load the annotated mp4.
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

# Serve annotated videos as static files. The URL the frontend uses is
# http://localhost:8000/outputs/<filename>.mp4
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")


@app.get("/")
def root() -> dict:
    return {"ok": True, "endpoints": ["/detect", "/track"]}


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _save_upload_to_tempfile(upload: UploadFile) -> Path:
    """Persist the uploaded video to a temp file so OpenCV can read it."""
    suffix = Path(upload.filename or "input.mp4").suffix or ".mp4"
    tmp = NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        shutil.copyfileobj(upload.file, tmp)
    finally:
        tmp.close()
    return Path(tmp.name)


def _open_video(path: Path) -> tuple[cv2.VideoCapture, float, int, int, int]:
    """Open a video and return (cap, fps, width, height, total_frames)."""
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open uploaded video")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return cap, fps, width, height, total


def _make_writer(path: Path, fps: float, width: int, height: int) -> cv2.VideoWriter:
    """Make a VideoWriter, preferring H.264 so the mp4 plays in browsers."""
    for codec in ("avc1", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
        if writer.isOpened():
            return writer
    raise HTTPException(status_code=500, detail="Could not open video writer")


def _new_output_path() -> tuple[Path, str]:
    """Pick a unique filename in outputs/ and return (path, url)."""
    name = f"{uuid.uuid4().hex}.mp4"
    return OUTPUTS_DIR / name, f"/outputs/{name}"


# ---------------------------------------------------------------------------
# /detect  -- per-frame detections, no tracking
# ---------------------------------------------------------------------------


@app.post("/detect")
async def detect(video: UploadFile = File(...)) -> dict:
    """
    Run YOLO on each frame, draw boxes, and return per-frame detection data.

    Response shape:
        {
          "video_url": "/outputs/<id>.mp4",
          "fps": 30.0,
          "frame_count": 150,
          "frames": [
            {
              "frame": 0,
              "time": 0.0,
              "detections": [
                {"cx": 320, "cy": 240, "x1": 300, "y1": 220,
                 "x2": 340, "y2": 260, "conf": 0.92, "label": "salamander"}
              ]
            },
            ...
          ]
        }
    """
    input_path = _save_upload_to_tempfile(video)
    try:
        cap, fps, width, height, total = _open_video(input_path)
        output_path, output_url = _new_output_path()
        writer = _make_writer(output_path, fps, width, height)

        frames: list[dict] = []
        frame_idx = 0

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # predict() returns a list of Results, one per input image.
                results = model.predict(frame, verbose=False)
                result = results[0]

                # Draw the boxes and labels onto the frame.
                annotated = result.plot()
                writer.write(annotated)

                # Extract the box data for this frame.
                detections = []
                if result.boxes is not None and len(result.boxes) > 0:
                    # .xyxy gives [x1, y1, x2, y2] for each box.
                    xyxy = result.boxes.xyxy.cpu().numpy()
                    confs = result.boxes.conf.cpu().numpy()
                    cls_ids = result.boxes.cls.cpu().numpy().astype(int)
                    names = result.names  # {class_id: "label"}
                    for (x1, y1, x2, y2), conf, cls_id in zip(xyxy, confs, cls_ids):
                        detections.append({
                            "cx": int((x1 + x2) / 2),
                            "cy": int((y1 + y2) / 2),
                            "x1": int(x1),
                            "y1": int(y1),
                            "x2": int(x2),
                            "y2": int(y2),
                            "conf": float(round(conf, 3)),
                            "label": names.get(int(cls_id), str(cls_id)),
                        })

                frames.append({
                    "frame": frame_idx,
                    "time": round(frame_idx / fps, 3) if fps else 0.0,
                    "detections": detections,
                })
                frame_idx += 1
        finally:
            cap.release()
            writer.release()

        return {
            "video_url": output_url,
            "fps": fps,
            "frame_count": frame_idx,
            "width": width,
            "height": height,
            "frames": frames,
        }
    finally:
        # The original upload is no longer needed once the annotated copy exists.
        input_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# /track  -- per-individual aggregate metrics via track IDs
# ---------------------------------------------------------------------------


@app.post("/track")
async def track(video: UploadFile = File(...)) -> dict:
    """
    Run YOLO with tracking enabled so each detection gets a stable track_id.
    Aggregate per-track metrics across the whole video.

    Response shape:
        {
          "video_url": "/outputs/<id>.mp4",
          "fps": 30.0,
          "frame_count": 150,
          "duration": 5.0,
          "tracks": [
            {
              "track_id": 1,
              "total_distance_px": 482.3,
              "time_on_screen_s": 4.7,
              "frames_seen": 141,
              "label": "salamander"
            },
            ...
          ]
        }
    """
    input_path = _save_upload_to_tempfile(video)
    try:
        cap, fps, width, height, total = _open_video(input_path)
        output_path, output_url = _new_output_path()
        writer = _make_writer(output_path, fps, width, height)

        # Per-track aggregates we update as we walk the frames.
        # last_xy lets us compute distance from the previous frame this track
        # was seen in. frames_seen counts visible frames (converted to seconds
        # at the end using fps).
        last_xy: dict[int, tuple[float, float]] = {}
        distance: dict[int, float] = {}
        frames_seen: dict[int, int] = {}
        label_for: dict[int, str] = {}

        frame_idx = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # persist=True keeps the tracker state across frames so IDs
                # stay stable from one call to the next.
                results = model.track(frame, persist=True, verbose=False)
                result = results[0]

                annotated = result.plot()
                writer.write(annotated)

                if (
                    result.boxes is not None
                    and len(result.boxes) > 0
                    and result.boxes.id is not None
                ):
                    xyxy = result.boxes.xyxy.cpu().numpy()
                    ids = result.boxes.id.cpu().numpy().astype(int)
                    cls_ids = result.boxes.cls.cpu().numpy().astype(int)
                    names = result.names
                    for (x1, y1, x2, y2), tid, cls_id in zip(xyxy, ids, cls_ids):
                        cx = (x1 + x2) / 2.0
                        cy = (y1 + y2) / 2.0
                        if tid in last_xy:
                            px, py = last_xy[tid]
                            distance[tid] = distance.get(tid, 0.0) + math.hypot(
                                cx - px, cy - py
                            )
                        last_xy[tid] = (cx, cy)
                        frames_seen[tid] = frames_seen.get(tid, 0) + 1
                        label_for[tid] = names.get(int(cls_id), str(cls_id))

                frame_idx += 1
        finally:
            cap.release()
            writer.release()

        tracks = []
        for tid, count in frames_seen.items():
            tracks.append({
                "track_id": int(tid),
                "total_distance_px": round(distance.get(tid, 0.0), 1),
                "time_on_screen_s": round(count / fps, 2) if fps else 0.0,
                "frames_seen": int(count),
                "label": label_for.get(tid, "?"),
            })
        # Sort by most-seen first so the table reads usefully.
        tracks.sort(key=lambda t: t["frames_seen"], reverse=True)

        return {
            "video_url": output_url,
            "fps": fps,
            "frame_count": frame_idx,
            "width": width,
            "height": height,
            "duration": round(frame_idx / fps, 2) if fps else 0.0,
            "tracks": tracks,
        }
    finally:
        input_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Run the server
# ---------------------------------------------------------------------------
#
# FastAPI needs an ASGI server to serve requests. Uvicorn is the standard
# one. This block lets you start the server by just running this file:
#
#     python main.py
#
# (You could also run `uvicorn main:app --reload --port 8000` from this
# directory if you want auto-reload during development.)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
