---
title: "Step 5: Async + Progress"
order: 7
---

The app works, and it has a real usability problem. The POST `/track` request blocks for as long as inference takes. The browser sits there, the user can't tell whether anything is happening, and on a long enough video the browser may give up entirely with a network error.

The fix is the standard pattern for long-running web jobs:

1. The POST endpoint returns immediately. It accepts the file, kicks off processing on a background thread, and tells the client "I started." That's all.
2. A separate GET endpoint reports the current state of the job.
3. The frontend polls the GET endpoint every second or so until the job is done, and uses the responses to update a progress bar.

This way every individual HTTP request is short. The browser is never holding a long connection open. The user gets visible progress.

## Backend

The backend grows a `job` dict that holds state, a background worker function, and a second route. The route handlers become very small.

```python
import time
from collections import defaultdict
from pathlib import Path
from threading import Thread

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
```

That's a substantial refactor. Read it top to bottom and trace what moved.

**`job = {"status": "idle"}`** is a module-level dict that holds the state of the current job. Three possible shapes at runtime:

- `{"status": "processing", "percent": 47}` while inference is running
- `{"status": "done", "percent": 100, "result": {...}}` when the job completes
- `{"status": "error", "message": "..."}` if something blew up

There's only one job at a time. A new upload overwrites the previous job's state. That's a real limitation, and the right call for a single-user POC. A production version would key state by job id and probably back it with Redis or a database.

**`run_track_job()`** is everything that used to live inside `start_track`, lifted into a function that takes no arguments. It reads the input file, runs the frame loop, writes the output, aggregates the metrics, and updates `job` along the way. Notice `job["percent"]` getting set inside the loop on every frame, which is what the progress bar reads.

The function is wrapped in `try/except` so an uncaught exception sets `job["status"] = "error"` instead of leaving the job stuck in `"processing"` forever.

**`Thread(target=run_track_job, daemon=True).start()`** spawns a new OS thread that calls the worker function. `daemon=True` means the thread dies if the main process exits, which is what you want for a server. The `.start()` is non-blocking. Control returns to `start_track` immediately, the route returns `{"status": "processing"}`, the client gets its response in milliseconds. The worker keeps running.

**`@app.get("/track")`** is the polling endpoint. All it does is return whatever's in `job` right now. The frontend hits this on a timer.

**`job.clear()` followed by setting keys** is the pattern for transitioning state. Without the `clear()`, old keys from the previous state would stick around. For example, on a successful completion we set `status` to `done` and add a `result`, but the `message` from a previous failed run would still be in the dict. `clear()` keeps the shapes clean.

## Frontend

Two real changes to the page.

**Poll instead of awaiting the POST response.** The submit handler now POSTs, confirms the response, then enters a loop that waits a moment and fetches `GET /track` until the job is `done` or `error`. The shape:

```js
while (true) {
  await new Promise(r => setTimeout(r, 1500));
  const job = await (await fetch(`${API_BASE}/track`)).json();
  if (job.status === "done") { setData(job.result); break; }
  if (job.status === "error") throw new Error(job.message);
  setPercent(job.percent ?? 0);
}
```

About 1.5 seconds between polls is a good default. Faster floods the backend, slower makes the progress bar feel janky.

**Render a progress bar.** HTML has a built-in `<progress>` element. Bind it to a piece of state that gets updated from each poll response:

```jsx
<progress value={percent} max={100} />
```

Show it while the loop is running, hide it when it finishes.

## Verify

Run both services. Upload a clip.

The submit button should disable, the progress bar should appear, and you should see the percent climb live as the backend works through the frames. The browser tab is fully responsive the entire time. You can switch tabs, scroll the page, do whatever.

When the job finishes, the progress bar reaches 100, the annotated video appears, and the metrics table renders.

If you try this with a much longer video (a few minutes), it just works. The browser never holds a long connection open, so there's no timeout to hit.

> **With your partner:** Stop the backend mid-job by hitting Ctrl-C while a video is processing. What happens to the frontend's progress bar? What state is it in? What would need to change to handle this more gracefully?

## Your turn

The walkthrough showed one metric end to end: time on screen per individual. Now add at least one of your own. Some ideas:

- Total pixels traveled per individual, computed from frame-to-frame centroid movement.
- Number of unique salamanders ever seen.
- Peak number of salamanders on screen at the same time.
- Detection count over time, ready to plot as a line.

Pick something interesting and add it: a new piece of state in the backend's loop, the right shape in the response, and a way to display it on the page. Use what you've built.
