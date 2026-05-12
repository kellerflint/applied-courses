# Salamander Tracker app (POC)

Simplest possible end-to-end version of the midterm: React frontend, FastAPI backend, YOLO doing the work. Two pages, two endpoints, one for each "mode" of using the model.

```
testing/salamander-poc/
├── annotate.py          ← the original CLI POC (unchanged)
├── yolov8n.pt           ← the default model (auto-downloads if missing)
├── backend/             ← FastAPI app
│   ├── main.py
│   └── requirements.txt
└── frontend/            ← Vite + React app
    ├── package.json
    └── src/
        ├── App.jsx
        ├── api.js
        ├── styles.css
        └── pages/
            ├── Detect.jsx
            └── Track.jsx
```

## How the two modes differ

- **`/detect` + Detect page** uses `model.predict()`. Each frame is processed in isolation. The response carries per-frame detection data (bounding boxes + centroids + confidence). Good for live-coordinate readouts and per-frame counts. No identity across frames.
- **`/track` + Track page** uses `model.track()`. Ultralytics assigns each detection a stable `track_id` across frames, so the backend can sum per-individual metrics (total distance traveled, time on screen).

Same model. Same video. Different inference call.

## Run the backend

```bash
cd testing/salamander-poc/backend
python3 -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

FastAPI needs an ASGI server to actually serve requests, so `main.py` boots `uvicorn` at the bottom of the file. Run `python main.py` like any other script and you're set. If you want auto-reload during development, run `uvicorn main:app --reload --port 8000` from this same folder instead.

First run downloads `yolov8n.pt` (~6 MB) if it isn't sitting at the poc root already.

API check: visit <http://localhost:8000/>. You should see `{"ok": true, "endpoints": ["/detect", "/track"]}`.

Annotated videos are written to `backend/outputs/` and served at `http://localhost:8000/outputs/<name>.mp4`.

## Run the frontend

```bash
cd testing/salamander-poc/frontend
npm install
npm run dev
```

Open <http://localhost:5173>. Two pages, linked in the header:

- **Detect** (`/`) — upload a video, watch the annotated playback, see live coordinates of every box in the current frame, and a small line chart of detection count over time.
- **Track** (`/track`) — upload a video, watch the annotated playback with track IDs, see a per-individual table of total distance and time on screen.

## Swapping in a trained salamander model

`backend/main.py` loads the model from a single `MODEL_PATH` constant near the top:

```python
MODEL_PATH = str(Path(__file__).parent.parent / "yolov8n.pt")
```

Point that at your trained `best.pt` (e.g. `runs/detect/train/weights/best.pt`) and restart the server. Both endpoints use the same model.

## Data contracts

The shape the backend returns for each endpoint is documented in the docstrings at the top of each route in `backend/main.py`. Worth reading before writing frontend code that depends on it.
