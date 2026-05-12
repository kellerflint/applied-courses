# Salamander Tracker POC

Simplest possible end-to-end version of the midterm: React frontend, FastAPI backend, YOLO doing detection. Two pages, two endpoints, one for each "mode" of using the model.

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

## Two pages, two endpoints

- **`/detect` + Detect page** uses `model.predict()`. Each frame processed in isolation. Returns the annotated video plus per-frame detection data. The frontend shows live coordinates of every box in the current frame plus a small line chart of detection count over time.
- **`/track` + Track page** uses `model.track()`. Each detection gets a stable `track_id` across frames, so the backend can compute per-individual aggregate metrics (total distance traveled, time on screen).

Same model, same video, different inference call.

## Swapping in a trained salamander model

`backend/main.py` loads the model from a single `MODEL_PATH` constant near the top:

```python
MODEL_PATH = str(Path(__file__).parent.parent / "data" / "yolov8n.pt")
```

Point that at your trained `best.pt` (e.g. `runs/detect/train/weights/best.pt`) and restart `dev.sh`. Both endpoints use the same model.

## Running just the standalone CLI

See `data/README.md`. The CLI in `data/annotate.py` is the original POC the FastAPI backend grew out of. Useful for sanity-checking that YOLO + OpenCV are wired up correctly before you involve a web server.
