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

**`app.mount("/videos", StaticFiles(...))`** tells FastAPI: whenever a request comes in for a path starting with `/videos/`, look for a matching file in `VIDEOS_DIR` and serve it. The browser will use this to load the video file via a normal `<video src="...">`. The backend never has to write a custom "send me the bytes" endpoint.

**`@app.post("/track")`** is the upload endpoint. The `video: UploadFile = File(...)` parameter tells FastAPI: this route expects a multipart form, and the field named `video` will contain a file. FastAPI parses the multipart body for you and gives you an `UploadFile` object with a `.file` you can read from.

**`(VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())`** reads all the bytes from the upload and writes them to `videos/input.mp4`. Every upload overwrites the previous one. That's fine for now.

**The response** is a small JSON object with the URL the frontend should use to play the video back. The `?t={int(time.time())}` is a browser cache buster: the file on disk is always `input.mp4`, but the URL is different each upload, so the browser fetches fresh instead of showing a cached previous video.

## Frontend

The page needs to do four new things:

1. Hold the selected file in component state. Use `useState(null)` and update it from the file input's `onChange` (the file is on `e.target.files[0]`).
2. Hold the backend's response in another piece of state. Use a separate `useState(null)`.
3. On submit, build a `FormData` object, `append` the file under the field name `video`, and POST it to `http://localhost:8000/track`. Don't set a `Content-Type` header yourself, the browser will set it correctly with the right multipart boundary when you pass a FormData as the request body.
4. When the response comes back, render a `<video src={data.video_url} controls />` tag using the URL from the response.

A file input looks like `<input type="file" accept="video/*" onChange={...} />`. The `accept="video/*"` is just a hint to the OS file picker, it doesn't enforce the file type.

Wrap the input and a submit button in a `<form>` with an `onSubmit` handler. Call `e.preventDefault()` at the top of the handler so the form doesn't try to do a regular page-navigating submission.

## Verify

Run both services. Open the frontend in your browser. Pick a video file. Click upload. The video should appear below the form and be playable.

If you look in `backend/videos/`, you'll see `input.mp4` sitting there. Upload a different video. The file gets replaced. Refresh the browser if needed and the new video should play.

> **With your partner:** Open the browser's network tab and watch what happens when you click upload. What's the request method? What does the request payload look like? What's in the response? Where does the actual video file live at each moment in this round trip?
