---
title: "Step 2: Upload & Playback"
order: 4
---

Next, the user picks a video file in the browser, the frontend ships it to the backend, the backend writes it to disk, and the frontend plays it back. No YOLO yet, just confirming a file can move between the two services.

## Add the imports

At the top of `backend/main.py`:

```python
import time
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
```

`UploadFile` and `File` are what FastAPI uses to receive uploaded files. `StaticFiles` lets us serve files from a folder over HTTP. `Path` is for filesystem work. `time` will be used in a cache buster later in this step.

## Make a folder for uploaded videos

Below your imports, before the FastAPI app:

```python
VIDEOS_DIR = Path(__file__).parent / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)
```

This creates a `videos/` folder next to `main.py` the first time the server starts.

**Check it works.** Restart the server. Look in `backend/`. There should be an empty `videos/` folder.

## Serve that folder over HTTP

After your `CORSMiddleware` setup:

```python
app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")
```

This tells FastAPI: any request for `/videos/<filename>` should look up that file in `VIDEOS_DIR` and return it.

**Check it works.** Drop any test file (a text file, image, anything) into `backend/videos/`. Hit `http://localhost:8000/videos/<filename>` in your browser. You should see the file served back. Delete the test file after.

## Add the upload endpoint

Below your `@app.get("/")` route:

```python
@app.post("/track")
def start_track(video: UploadFile = File(...)):
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    return {
        "status": "received",
        "video_url": f"http://localhost:8000/videos/input.mp4?t={int(time.time())}",
    }
```

`UploadFile = File(...)` is FastAPI's way of declaring "this route accepts a multipart form, and the field named `video` will contain a file." We read all the bytes and write them to `videos/input.mp4`. Every upload overwrites the previous one.

The `?t={int(time.time())}` is a browser cache buster: the file on disk is always `input.mp4`, but the URL is different each upload so the browser fetches fresh instead of showing a cached previous video.

**Check it works.** With the backend running, open another terminal and `cd` into a folder that contains some video file on your machine. Then:

```bash
curl -F "video=@your_video.mp4" http://localhost:8000/track
```

Replace `your_video.mp4` with the actual filename you have there. The `@` is curl's syntax for "send the contents of this file." You should get back the JSON response, and `backend/videos/input.mp4` should now exist.

## Build the frontend page

The page needs to let the user pick a file, send it to the backend on submit, and render the URL the backend returns in a `<video>` tag.

Most of this is normal React. State for the picked file, state for the response, a form with `onSubmit`, conditional render of the video element.

Two pieces of non-React-specific plumbing to be aware of.

**Getting a file out of a file input.** A file `<input>`'s change event has `event.target.files`, which is a `FileList`. Grab the first one:

```js
onChange={(e) => setFile(e.target.files[0])}
```

**Posting a file as multipart form data.** Build a `FormData` and pass it as the `fetch` body. Don't set a `Content-Type` header yourself. The browser sets the right things automatically when the body is a FormData object.

```js
const form = new FormData();
form.append("video", file);
fetch("http://localhost:8000/track", { method: "POST", body: form });
```

Wire those into a component that picks a file, submits, and renders `<video src={data.video_url} controls />` once you have a response.

**Check it works.** Open the frontend, pick a video, click upload. The video should appear below the form and be playable.

> **With your partner:** Open the inspector's network tab and watch what happens when you click upload. What's the request method? What does the request payload look like? What's in the response?
