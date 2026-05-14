---
title: "Step 4: Per-Track Metrics"
order: 6
---

The annotated video already shows you which salamanders are where. This step turns that into numbers. For each individual the tracker identified, the backend will count how many frames it was visible in, convert that to seconds, and ship the result alongside the annotated video.

The lesson under the hood: `model.track()` stamps each detection with a `track_id` that stays consistent for the same individual across frames. Once you have that ID, aggregating per-individual statistics is just dict accounting.

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

What's new:

**`frames_seen = defaultdict(int)`** and **`label_for = {}`** sit before the loop. `frames_seen` maps each track ID to a frame count. `defaultdict(int)` means looking up a key that doesn't exist yet returns `0`, so we can do `+= 1` without checking first. `label_for` maps each track ID to its class label (like `"salamander"`).

**Inside the loop, after writing the annotated frame**, we look at the result's boxes. `result.boxes` is the Ultralytics object holding all the detections for this frame. It can be `None` (no detections) and `result.boxes.id` can also be `None` (detections exist but the tracker hasn't assigned IDs yet, which happens on the very first frame or two). Skip the update in either case.

When there are tracked detections, `boxes.id` and `boxes.cls` are tensors. `.tolist()` converts them to plain Python lists. We zip them together and walk through each detection: increment `frames_seen[tid]` and remember its label.

**`model.names`** is the class-id-to-label dictionary that came with the trained model. If your model was trained on a single class `salamander`, this is `{0: "salamander"}`. Looking up `model.names[int(cls_id)]` turns a numeric class id into a human-readable string.

**After the loop**, the list comprehension walks the `frames_seen` dict and builds a list of result objects, one per unique track. The frame count gets converted to seconds by dividing by `fps`.

**The response** now has a `tracks` field next to `status` and `video_url`.

## Frontend

Render the tracks. After the `<video>` element, add a `<table>` with one row per entry in `data.tracks`. Columns: `track_id`, `label`, `time_on_screen_s`. React's array `.map()` is the natural fit for rendering rows.

You can use the table styles in `styles.css` from earlier templates if you have them, or write your own. Functionality is what matters.

## Verify

Upload a short clip. After processing, you should see the annotated video plus a small table next to it. Each row is one tracked individual, with how many seconds it was on screen.

If the table is empty, the tracker didn't find anything across the whole video. Open the JSON response in the browser's network tab and confirm `tracks` is `[]`. Try a different clip or check that the model you loaded actually detects the thing you're looking at.

> **With your partner:** Run the same video twice. Do you get the same track IDs both times? Why or why not? What does that tell you about how stable `model.track()` is across separate sessions?
