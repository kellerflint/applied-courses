---
title: "Step 5: Async + Progress"
order: 7
---

The app works, and it has a real usability problem. The POST `/track` request blocks for as long as inference takes. The browser sits there, the user can't tell whether anything is happening, and on a long enough video the browser may give up entirely with a network error.

The standard fix for long-running web jobs has three parts:

1. The POST endpoint returns immediately. It accepts the file, kicks off processing on a background thread, and tells the client "I started."
2. A separate GET endpoint reports the current state of the job.
3. The frontend polls the GET endpoint every second or so and updates a progress bar.

Every individual HTTP request is short. The browser is never holding a long connection open. The user gets visible progress.

## Import Thread

At the top of `main.py`:

```python
from threading import Thread
```

## Add a job dict at module scope

Below your `app.mount(...)` line:

```python
job = {"status": "idle"}
```

This is a single shared dict that holds the state of the current job. We'll update it from the worker and read it from the GET endpoint. One job at a time. A new upload overwrites the previous job's state.

## Extract the work into a separate function

Right now everything happens inside `start_track`. Lift it into a standalone function. Above `start_track`, add:

```python
def run_track_job():
    # All the existing processing code from start_track moves here:
    # opening the video, setting up the writer, the frame loop with
    # YOLO inference and the per-track aggregation, the cap/writer
    # release calls, building the tracks list.
```

Cut everything out of `start_track` except saving the upload and returning, and paste it inside the new function. The function takes no arguments because all the paths and constants it needs are module-level.

`start_track` for now becomes just:

```python
@app.post("/track")
def start_track(video: UploadFile = File(...)):
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    run_track_job()
    return {"status": "done"}
```

This still calls the worker synchronously. We'll change that shortly.

**Check it works.** Upload a clip. It should behave exactly the same as before, blocking for 30 to 60 seconds and then succeeding. Nothing has changed in behavior, only in shape.

## Track progress inside the worker

Inside `run_track_job`'s frame loop, after writing the annotated frame:

```python
job["percent"] = int((frame_idx + 1) / total * 100)
```

This updates the shared dict every frame.

## Mark the job done at the end

At the bottom of `run_track_job`, after the tracks list is built, instead of the old `return` statement, write the result into the job dict:

```python
job.clear()
job["status"] = "done"
job["percent"] = 100
job["result"] = {
    "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
    "tracks": tracks,
}
```

`job.clear()` wipes any stale keys from a previous run (like a leftover error message). Then we set the dict into the "done" shape with the result the frontend will render.

## Reset the job on a new upload

Back in `start_track`, before calling the worker, reset the job state:

```python
@app.post("/track")
def start_track(video: UploadFile = File(...)):
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    job.clear()
    job["status"] = "processing"
    job["percent"] = 0
    run_track_job()
    return {"status": "processing"}
```

## Add the GET endpoint

Below `start_track`:

```python
@app.get("/track")
def get_track():
    return job
```

This returns whatever's currently in the `job` dict.

**Check it works.** Upload a clip. After it finishes (still synchronous, still slow), hit GET /track from another terminal:

```bash
curl http://localhost:8000/track
```

You should see the full "done" state, including the result. If you hit it before uploading anything, you'll see `{"status": "idle"}` (the initial value).

## Run the worker on a thread

The single line change. Replace `run_track_job()` in `start_track` with:

```python
Thread(target=run_track_job, daemon=True).start()
```

`Thread(target=...)` creates a new thread that will call the function. `daemon=True` means the thread doesn't keep the process alive on its own. `.start()` runs the function in the background. Control returns to `start_track` immediately, the route returns `{"status": "processing"}` in milliseconds, and the worker keeps going.

**Check it works.** Upload a clip and immediately hit GET /track in another terminal a few times during processing:

```bash
curl http://localhost:8000/track
```

You should see `{"status": "processing", "percent": N}` with `N` increasing each time. After about a minute, the response transitions to `{"status": "done", "percent": 100, "result": {...}}`. That's the polling target the frontend will hit.

## Handle errors in the worker

If an exception escapes `run_track_job`, the job is stuck on "processing" forever and the frontend will poll forever. Wrap the whole worker body in try/except:

```python
def run_track_job():
    try:
        # all the existing code
        ...
    except Exception as e:
        print(f"error: {e}", flush=True)
        job.clear()
        job["status"] = "error"
        job["message"] = str(e)
```

## Frontend: poll instead of awaiting

The submit handler used to await the POST response and use it directly. Now it POSTs, confirms the response came back OK, then enters a loop that fetches `GET /track` until the job is `done` or `error`:

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

## Frontend: render a progress bar

HTML has a built-in `<progress>` element. Bind it to the percent state and show it while the loop is running:

```jsx
<progress value={percent} max={100} />
```

**Check it works.** Upload a clip. The submit button should disable, the progress bar should appear, and the percent should climb live as the backend works through the frames. The browser tab is fully responsive the entire time. When the job finishes, the progress bar reaches 100, the annotated video appears, and the metrics table renders.

If you try a longer video (a few minutes), it just works. The browser never holds a long connection open, so there's no timeout to hit.

## Your turn

The walkthrough showed one metric end to end: time on screen per individual. Now add at least one of your own. Some ideas:

- Total pixels traveled per individual, computed from frame-to-frame centroid movement.
- Number of unique salamanders ever seen.
- Peak number of salamanders on screen at the same time.
- Detection count over time, ready to plot as a line.

Pick something interesting and add it: a new piece of state in the backend's loop, the right shape in the response, and a way to display it on the page.
