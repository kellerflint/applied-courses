import time
import cv2
from collections import defaultdict
from pathlib import Path
from threading import Thread

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


VIDEOS_DIR = Path(__file__).parent / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)

model = YOLO(str(Path(__file__).parent.parent / "data" / "yolov8n.pt"))

app = FastAPI(title="Salamander Tracker POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")


@app.get("/")
def root():
    return {"ok": True}


# Single job, overwritten by each new upload. Fine for a one-user POC.
job = {"status": "idle"}


def run_track_job():
    try:
        input_path = VIDEOS_DIR / "input.mp4"
        output_path = VIDEOS_DIR / "output.mp4"

        cap = cv2.VideoCapture(str(input_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*"avc1"),
            fps,
            (width, height),
        )

        print(f"processing {total} frames", flush=True)

        frames_seen = defaultdict(int)
        label_for = {}

        for frame_idx in range(total):
            ok, frame = cap.read()
            if not ok:
                break

            # persist=True keeps track IDs stable across frames.
            result = model.track(frame, persist=True, verbose=False)[0]
            writer.write(result.plot())

            boxes = result.boxes
            if boxes is not None and boxes.id is not None:
                for tid, cls_id in zip(boxes.id.tolist(), boxes.cls.tolist()):
                    frames_seen[int(tid)] += 1
                    label_for[int(tid)] = model.names[int(cls_id)]

            job["percent"] = int((frame_idx + 1) / total * 100)

        cap.release()
        writer.release()

        tracks = [
            {
                "track_id": tid,
                "time_on_screen_s": round(count / fps, 2),
                "label": label_for[tid],
            }
            for tid, count in frames_seen.items()
        ]

        job.clear()
        job["status"] = "done"
        job["percent"] = 100
        # Cache buster on the URL so the browser doesn't show a stale video.
        job["result"] = {
            "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
            "fps": fps,
            "frame_count": total,
            "duration": round(total / fps, 2),
            "tracks": tracks,
        }
        print(f"done. {len(tracks)} unique track id(s)", flush=True)
    except Exception as e:
        print(f"error: {e}", flush=True)
        job.clear()
        job["status"] = "error"
        job["message"] = str(e)


@app.post("/track")
def start_track(video: UploadFile = File(...)):
    """Accept the upload, kick off processing in the background, return
    immediately. Frontend polls GET /track for progress."""
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    job.clear()
    job["status"] = "processing"
    job["percent"] = 0
    Thread(target=run_track_job, daemon=True).start()
    return {"status": "processing"}


@app.get("/track")
def get_track():
    return job


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
