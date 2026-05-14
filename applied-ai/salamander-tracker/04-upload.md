---
title: "Step 2: Upload & Playback"
order: 4
---

Next, the user will be able to pick a video file in the browser, the frontend ships it to the backend, the backend writes it to disk, and the frontend plays it back. No YOLO yet. The point of this step is to confirm the file actually moves between the two services and ends up somewhere you can read it from.

## Backend

You need three new things on the backend.

1. A place on disk to put the uploaded file.
2. A way to serve that file back over HTTP so the browser can load it.
3. An endpoint that accepts a multipart file upload.

Update `backend/main.py`:

```python
import time
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


VIDEOS_DIR = Path(__file__).parent / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)


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
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    return {
        "status": "received",
        "video_url": f"http://localhost:8000/videos/input.mp4?t={int(time.time())}",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Read the new pieces.

**`VIDEOS_DIR`** is just a folder next to `main.py`. `.mkdir(exist_ok=True)` creates it if it isn't there. The folder will hold the uploaded input and (later) the annotated output.

**`app.mount("/videos", StaticFiles(...))`** tells FastAPI: whenever a request comes in for a path starting with `/videos/`, look for a matching file in `VIDEOS_DIR` and serve it. The browser will use this to load the video file via a normal `<video src="...">` element.

**`@app.post("/track")`** is the upload endpoint. The `video: UploadFile = File(...)` parameter tells FastAPI: this route expects a multipart form, and the field named `video` will contain a file. FastAPI parses the multipart body for you and gives you an `UploadFile` object with a `.file` you can read from.

**`(VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())`** reads all the bytes from the upload and writes them to `videos/input.mp4`. Every upload overwrites the previous one.

**The response** is a small JSON object with the URL the frontend should use to play the video back. The `?t={int(time.time())}` is a browser cache buster. The file on disk is always `input.mp4`, but the URL is different each upload, so the browser fetches fresh instead of showing a cached previous video.

## Frontend

The page needs to do three things: let the user pick a file, send it to the backend on submit, and render the URL the backend returns in a `<video>` tag.

Most of this is normal React. State for the picked file, state for the response, a form with `onSubmit`, conditional render of the video element. You've done that shape before.

Two pieces of non-React-specific plumbing worth showing directly.

**Getting a file out of a file input.** A file `<input>`'s change event has `event.target.files`, which is a `FileList`. Grab the first one:

```js
onChange={(e) => setFile(e.target.files[0])}
```

**Posting a file as multipart form data.** Build a `FormData` and pass it as the `fetch` body. Don't set a `Content-Type` header yourself. The browser sets the right one (including the multipart boundary) automatically when the body is a FormData.

```js
const form = new FormData();
form.append("video", file);
fetch("http://localhost:8000/track", { method: "POST", body: form });
```

Wire those into a component that picks a file, submits, and renders `<video src={data.video_url} controls />` once you have a response.

## Verify

Run both services. Open the frontend in your browser. Pick a video file. Click upload. The video should appear below the form and be playable.

If you look in `backend/videos/`, you'll see `input.mp4` sitting there. Upload a different video. The file gets replaced. Refresh the browser if needed and the new video should play.

> **With your partner:** Open the browser's network tab and watch what happens when you click upload. What's the request method? What does the request payload look like? What's in the response? Where does the actual video file live at each moment in this round trip?
