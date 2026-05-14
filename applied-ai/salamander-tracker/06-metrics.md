---
title: "Step 4: Per-Track Metrics"
order: 6
---

The annotated video already shows you which salamanders are where. This step turns that into numbers. For each individual the tracker identified, the backend will count how many frames it was visible in, convert that to seconds, and ship the result alongside the annotated video.

The lesson under the hood: `model.track()` stamps each detection with a `track_id` that stays consistent for the same individual across frames.

## Backend

The frame loop stays the same shape. Add two dicts before it, four lines inside it, and a list comprehension after it.

```python
import time
from collections import defaultdict
from pathlib import Path

import cv2
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


@app.post("/track")
def start_track(video: UploadFile = File(...)):
    input_path = VIDEOS_DIR / "input.mp4"
    output_path = VIDEOS_DIR / "output.mp4"
    input_path.write_bytes(video.file.read())

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

        result = model.track(frame, persist=True, verbose=False)[0]
        writer.write(result.plot())

        boxes = result.boxes
        if boxes is not None and boxes.id is not None:
            for tid, cls_id in zip(boxes.id.tolist(), boxes.cls.tolist()):
                frames_seen[int(tid)] += 1
                label_for[int(tid)] = model.names[int(cls_id)]

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
    print(f"done. {len(tracks)} unique track id(s)", flush=True)

    return {
        "status": "done",
        "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
        "tracks": tracks,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

A few things to call out:

**`defaultdict(int)`** means `frames_seen[some_new_id] += 1` works without an existence check. Missing keys default to `0`.

**The `None` checks.** `result.boxes` is `None` when there are no detections in a frame. `boxes.id` is `None` when there are detections but tracking hasn't assigned IDs yet (which can happen on the first frame or two). Skip both cases.

**`.tolist()`** turns the torch tensors that `boxes.id` and `boxes.cls` hand back into plain Python lists you can iterate.

**`model.names`** is a class-id-to-label dict from the trained model. If your model has one class it's `{0: "salamander"}`. We use it to turn the numeric class id from each box into a string.

The list comprehension after the loop converts each track's frame count to seconds (dividing by `fps`) and pairs it with the label. That list goes in the response next to `status` and `video_url`.

## Frontend

Render the tracks. After the `<video>` element, add a `<table>` with one row per entry in `data.tracks`. Columns: `track_id`, `label`, `time_on_screen_s`. React's array `.map()` is the natural fit for rendering rows.

You can use the table styles in `styles.css` from earlier templates if you have them, or write your own. Functionality is what matters.

## Verify

Upload a short clip. After processing, you should see the annotated video plus a small table next to it. Each row is one tracked individual, with how many seconds it was on screen.

If the table is empty, the tracker didn't find anything across the whole video. Open the JSON response in the browser's network tab and confirm `tracks` is `[]`. Try a different clip or check that the model you loaded actually detects the thing you're looking at.

> **With your partner:** Run the same video twice. Do you get the same track IDs both times? Why or why not? What does that tell you about how stable `model.track()` is across separate sessions?
