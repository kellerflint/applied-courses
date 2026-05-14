---
title: "Step 3: Run YOLO"
order: 5
---

Now the interesting part. The uploaded video gets read frame by frame, YOLO runs on each one, and an annotated copy gets written to disk. By the end of this step, an upload produces a new mp4 with bounding boxes drawn over every detected salamander.

## Add OpenCV and Ultralytics

```python
import cv2
from ultralytics import YOLO
```

OpenCV reads and writes video files frame by frame. The `YOLO` class loads the model and runs inference.

## Load the model at startup

Below your app setup:

```python
model = YOLO(str(Path(__file__).parent.parent / "data" / "yolov8n.pt"))
```

At module scope, not inside the route. The model file is roughly 6 MB and loading it isn't free, so you want it to happen once when the server boots. Every request reuses the same `model` object. Point the path at your trained `best.pt`.

**Check it works.** Restart the server. You should see Ultralytics print a model summary on startup. To see what classes your model knows, temporarily add a print and restart:

```python
print(model.names)
```

For a model trained on one class called `salamander`, you'll see `{0: 'salamander'}`. For the default `yolov8n.pt` (the generic COCO model), you'll see a long dict of 80 classes. Remove the print after you've looked at it.

## Open the uploaded video

Inside the `/track` handler, after the line that saves the upload, add:

```python
input_path = VIDEOS_DIR / "input.mp4"
cap = cv2.VideoCapture(str(input_path))
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"fps={fps} dims={width}x{height} frames={total}")
```

The `.get()` calls pull metadata from the video. The print is so you can verify it worked.

**Check it works.** Upload a video through the frontend (the existing form still works, the response will be stale but that's fine). The backend terminal should print something like `fps=24.0 dims=1920x1080 frames=722`. If you see zeros or weird values, the file didn't save right.

## Try YOLO on a single frame

Before running the model over every frame, prove it works on one. Below the metadata block:

```python
ok, frame = cap.read()
result = model.track(frame, persist=True, verbose=False)[0]
print("detections in frame 0:", len(result.boxes), "classes:", result.boxes.cls.tolist())
cap.release()
```

**Check it works.** Upload again. You should see something like `detections in frame 0: 1 classes: [0.0]`. If you get `0` detections, either the model isn't finding anything (a problem with training) or that frame happens to be empty (try a different clip). Either way, you want to know now before writing the whole loop.

Remove this test block when you've verified it. You're about to replace it.

## Set up the output writer

```python
output_path = VIDEOS_DIR / "output.mp4"
writer = cv2.VideoWriter(
    str(output_path),
    cv2.VideoWriter_fourcc(*"avc1"),
    fps,
    (width, height),
)
```

`avc1` is the H.264 codec. Browsers play H.264 reliably in `<video>` tags.

## The frame loop

In place of the single-frame test you just removed:

```python
for frame_idx in range(total):
    ok, frame = cap.read()
    if not ok:
        break
    result = model.track(frame, persist=True, verbose=False)[0]
    writer.write(result.plot())
    if frame_idx % 30 == 0:
        print(f"frame {frame_idx}/{total}")

cap.release()
writer.release()
```

`cap.read()` returns `(ok, frame)`. When the video ends, `ok` is `False` and the loop breaks.

`model.track(... persist=True)` is what makes this `track` instead of `predict`: the tracker keeps state between calls, so the same salamander keeps the same `track_id` across frames.

`result.plot()` returns the frame with bounding boxes drawn on top. That's what gets written to the output.

The `if frame_idx % 30` print fires every 30 frames so you see progress in the terminal. Without releasing the writer at the end, the output mp4 won't actually play.

**Check it works.** Upload a clip. The terminal should print `frame 0/722`, `frame 30/722`, ... for 30 to 60 seconds. When it finishes, look in `backend/videos/`. There should be an `output.mp4` next to `input.mp4`. Open it directly with QuickTime or VLC and confirm it plays and has boxes drawn on it.

## Return the output URL

Update the response to point at the annotated output:

```python
return {
    "status": "done",
    "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
}
```

## Update the frontend

Two small changes to the page from the previous step:

- Track whether a request is in flight. While it is, disable the submit button and show a "Processing" message under the form so the user knows the page didn't break.
- The `data.video_url` already points at the output, so the existing `<video>` tag works without changes.

**Check it works.** Upload a clip through the page. You should see the loading indicator, a 30 to 60 second wait, then the annotated video with boxes drawn on top. Notice that the browser tab is unresponsive while it waits. That's a real problem we'll fix later.

> **With your partner:** Open the inspector's network tab while you upload. Find the `/track` request. What's its status while inference is running? What happens if you refresh the page partway through?
