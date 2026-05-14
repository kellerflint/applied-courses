"""Salamander Tracker backend. POST /track starts a job. GET /track/{job_id}
polls for progress and the final result."""

import uuid
from collections import defaultdict
from pathlib import Path
from threading import Thread

import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

model = YOLO(str(Path(__file__).parent.parent / "data" / "yolov8n.pt"))


app = FastAPI(title="Salamander Tracker POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")


@app.get("/")
def root():
    return {"ok": True}


# In-memory job store. Server restart clears it.
# Each entry is one of:
#   {"status": "processing", "percent": N}
#   {"status": "done", "percent": 100, "result": {...}}
#   {"status": "error", "message": "..."}
jobs = {}


class TrackAggregator:
    """Counts how many frames each tracked individual was visible.
    summarize(fps) converts those counts to seconds.

    Lifecycle: create, update(...) once per frame, summarize(fps) at end.
    """

    def __init__(self):
        self.frames_seen = defaultdict(int)
        self.label_for = {}

    def update(self, result):
        boxes = result.boxes
        if boxes is None or len(boxes) == 0 or boxes.id is None:
            return
        for tid, cls_id in zip(boxes.id.tolist(), boxes.cls.tolist()):
            self.frames_seen[int(tid)] += 1
            self.label_for[int(tid)] = model.names.get(int(cls_id), str(int(cls_id)))

    def summarize(self, fps):
        return [
            {
                "track_id": tid,
                "time_on_screen_s": round(count / fps, 2),
                "label": self.label_for[tid],
            }
            for tid, count in self.frames_seen.items()
        ]


def run_track_job(job_id, input_path):
    try:
        cap = cv2.VideoCapture(str(input_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        output_name = f"{job_id}.mp4"
        output_path = OUTPUTS_DIR / output_name

        # Prefer H.264 (avc1) so the mp4 plays in browsers. Fall back to mp4v.
        for codec in ("avc1", "mp4v"):
            writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*codec), fps, (width, height))
            if writer.isOpened():
                break

        print(f"[{job_id[:8]}] processing {total} frames", flush=True)

        aggregator = TrackAggregator()
        frame_idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            # persist=True keeps track IDs stable across frames.
            result = model.track(frame, persist=True, verbose=False)[0]
            writer.write(result.plot())
            aggregator.update(result)

            frame_idx += 1
            jobs[job_id]["percent"] = int(frame_idx / total * 100) if total else 0
            if frame_idx % 30 == 0:
                print(f"[{job_id[:8]}] {frame_idx}/{total}", flush=True)

        cap.release()
        writer.release()

        tracks = aggregator.summarize(fps)
        jobs[job_id] = {
            "status": "done",
            "percent": 100,
            "result": {
                "video_url": f"http://localhost:8000/outputs/{output_name}",
                "fps": fps,
                "frame_count": frame_idx,
                "duration": round(frame_idx / fps, 2),
                "tracks": tracks,
            },
        }
        print(f"[{job_id[:8]}] done. {len(tracks)} unique track id(s)", flush=True)
    except Exception as e:
        print(f"[{job_id[:8]}] error: {e}", flush=True)
        jobs[job_id] = {"status": "error", "message": str(e)}


@app.post("/track")
def start_track(video: UploadFile = File(...)):
    """Accept the upload, register a job, return its id. Frontend polls
    GET /track/{job_id} for progress and the result."""
    job_id = uuid.uuid4().hex
    input_path = OUTPUTS_DIR / f"{job_id}-input.mp4"
    input_path.write_bytes(video.file.read())
    jobs[job_id] = {"status": "processing", "percent": 0}
    Thread(target=run_track_job, args=(job_id, input_path), daemon=True).start()
    return {"job_id": job_id, "status": "processing"}


@app.get("/track/{job_id}")
def get_track(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
