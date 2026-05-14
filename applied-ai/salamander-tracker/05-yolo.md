---
title: "Step 3: Run YOLO"
order: 5
---

Now the interesting part. The uploaded video gets read frame by frame, YOLO runs on each one, and an annotated copy gets written to disk. The frontend plays that copy back instead of the raw upload.

By the end of this step, an upload produces a new mp4 with bounding boxes drawn over every detected salamander. That's the core of the app. Everything after this is just structure around it.

## Backend

Update `backend/main.py`:

```python
import time
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

    for frame_idx in range(total):
        ok, frame = cap.read()
        if not ok:
            break
        # persist=True keeps track IDs stable across frames.
        result = model.track(frame, persist=True, verbose=False)[0]
        writer.write(result.plot())

    cap.release()
    writer.release()
    print("done", flush=True)

    return {
        "status": "done",
        "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Walk through the new pieces.

**`model = YOLO(...)`** at module scope, not inside the route. The model file is roughly 6 MB and loading it parses a fair amount of data. You want this to happen once when the server boots. Every request reuses the same `model` object. Point the path at your trained `best.pt` from the YOLO walkthrough.

**`cv2.VideoCapture(...)`** opens the input video for reading. The `.get(cv2.CAP_PROP_*)` calls pull metadata you need next: fps and dimensions to set up the writer, and `total` to use as the loop bound.

**`cv2.VideoWriter(...)`** opens the output mp4 for writing. Its fps and dimensions match the input so the result plays back at the right speed. `avc1` is the H.264 codec. Browsers play H.264 reliably in `<video>` tags.

**The frame loop.** `cap.read()` returns `(ok, frame)`. When the video ends, `ok` is `False` and the loop breaks.

`model.track(frame, persist=True, verbose=False)` runs YOLO and returns a list (one result per input frame, so we take `[0]`). The `persist=True` is what makes this `track` instead of `predict`: the tracker keeps state between calls, so the same salamander keeps the same `track_id` across frames.

`result.plot()` returns the frame with bounding boxes drawn on top. That's what gets written to the output.

**`cap.release()` and `writer.release()`** flush their resources. Without releasing the writer, the output mp4 gets created but won't play.

**The response** points at `videos/output.mp4` now, not `input.mp4`. Same cache buster pattern.

## Frontend

Two small additions to the page from the previous step.

**A loading flag.** Track whether a request is in flight. While it is, disable the submit button and show a "Processing" message under the form so the user knows the page didn't break.

**Render the output URL.** Same `<video>` tag, but `data.video_url` now points at the annotated mp4 instead of the raw upload.

That's it. The form, the file input, and the submit handler are all the same shape.

## Verify

Run both services. Upload a short video clip (under a minute is best for now). After roughly 30 to 60 seconds, the annotated video should appear and you should see bounding boxes drawn over anything the model detects.

Two things to notice while you wait.

In the backend terminal, you should see `processing N frames` print right after the upload arrives, then `done` after inference finishes. That tells you the loop is running.

In the browser tab, your page hangs. The submit button is disabled and your "Processing" message is showing, but if you try to click anywhere or navigate, nothing responds. That's because the browser is waiting for an HTTP response that takes 30 to 60 seconds to arrive. We'll deal with that in a couple of steps.

> **With your partner:** Open the browser's dev tools and watch the Network tab while you upload. Find the `/track` request. What's its status while inference is running? How long does it sit in that state? What happens if you refresh the page partway through?
