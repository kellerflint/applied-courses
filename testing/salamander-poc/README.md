# Salamander Tracker POC

Simplest possible end-to-end version of the midterm: React frontend, FastAPI backend, YOLO doing detection on a single page.

## Run

```bash
./dev.sh
```

That script:

- Creates the backend Python venv if it doesn't exist and installs deps from `backend/requirements.txt`.
- Runs `npm install` if `frontend/node_modules` is missing.
- Boots the FastAPI server on <http://localhost:8000>.
- Boots the Vite dev server on <http://localhost:5173>.
- Streams both consoles into one, with each line prefixed `[backend ]` or `[frontend]` so you can see what's coming from where.

Ctrl-C stops both.

The first run will also auto-download `yolov8n.pt` into `data/` if it isn't already there (about 6 MB).

## Structure

```
testing/salamander-poc/
├── README.md            ← you are here
├── dev.sh               ← one-command boot
├── backend/             ← FastAPI app (Python)
│   ├── main.py
│   └── requirements.txt
├── frontend/            ← Vite + React
│   ├── package.json
│   └── src/...
└── data/                ← model weights, test videos, original CLI
    ├── annotate.py
    ├── yolov8n.pt
    ├── ensantina.mp4
    ├── ensantina_short.mp4
    └── requirements.txt
```

## How it works

The frontend uploads a video to the backend, which runs YOLO with tracking on every frame and produces an annotated copy of the video plus aggregate metrics per detected individual (total pixels traveled, time on screen, frames seen).

Inference can take longer than the source video itself, so the backend runs the job on a background thread and the frontend polls for progress instead of holding a long HTTP connection open:

- `POST /track` accepts the upload, starts the job on a thread, returns `{job_id, status: "processing"}` immediately.
- `GET /track/{job_id}` returns the current state. Either `{"status": "processing", "percent": 47}`, `{"status": "done", "percent": 100, "result": {...}}`, or `{"status": "error", "message": "..."}`.

The frontend polls every 1.5 seconds and renders a progress bar. When `status === "done"` it stops polling and shows the annotated video and metrics table.

For quick iteration use `data/ensantina_short.mp4` (30 seconds, processes in ~40 seconds). The full `data/ensantina.mp4` is 8 minutes long, so processing takes around 10 minutes.

## Swapping in a trained salamander model

`backend/main.py` loads the model from a single `MODEL_PATH` constant near the top:

```python
MODEL_PATH = str(Path(__file__).parent.parent / "data" / "yolov8n.pt")
```

Point that at your trained `best.pt` (e.g. `runs/detect/train/weights/best.pt`) and restart `dev.sh`.

## Running just the standalone CLI

See `data/README.md`. The CLI in `data/annotate.py` is the original POC the FastAPI backend grew out of. Useful for sanity-checking that YOLO + OpenCV are wired up correctly before you involve a web server.
