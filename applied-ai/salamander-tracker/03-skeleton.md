---
title: "Step 1: Skeleton"
order: 3
---

Before you upload any video, run any YOLO, or compute any metrics, you need two services that can talk to each other. A Python backend serving HTTP on one port. A React frontend running on another. A JSON payload making the round trip between them.

This step gets you there. By the end you'll have both services running on your machine, and a page in your browser that shows a response coming back from the backend.

## Project structure

Create a single project folder for the app. Inside it, make two subfolders: `backend/` and `frontend/`. You'll work on them in parallel from here on out.

```
salamander-tracker/
├── backend/
└── frontend/
```

You'll keep both terminals open while you work: one running the backend, one running the frontend.

## Backend

The Python side. You'll use **FastAPI**, a web framework that's compact and convention-driven. You write functions, decorate them with the route they should answer, and FastAPI handles the request parsing and JSON serialization. **Uvicorn** is the actual HTTP server that runs the FastAPI app.

### Set up the venv

In `backend/`, set up a Python virtual environment so the dependencies for this project don't get tangled up with anything else on your machine.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

### Install the dependencies

Create `backend/requirements.txt`:

```
fastapi
uvicorn[standard]
python-multipart
ultralytics
opencv-python
```

You don't need all of these yet. `python-multipart` shows up in step 2, `ultralytics` and `opencv-python` in step 3. They're all listed now so you only install once.

```bash
pip install -r requirements.txt
```

This takes a minute or two. `ultralytics` pulls in PyTorch which is large.

### Write the backend

Create `backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Salamander Tracker POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

**`FastAPI(...)`** creates the app. The `title` shows up in the auto-generated API docs FastAPI gives you for free at `/docs`.

**The CORS middleware** matters because your frontend will run on a different port (5173) than the backend (8000). Browsers treat those as different origins and block cross-origin requests unless the server says it's OK. For this POC, `allow_origins=["*"]` says "any origin is fine." That's appropriate for local development and inappropriate for production. We'll leave it as is.

**`@app.get("/")`** declares a GET route at the root path. When the browser hits `http://localhost:8000/`, FastAPI calls the `root()` function and returns whatever it returns as JSON. Right now that's the dict `{"ok": True}`.

**The `if __name__ == "__main__"` block** lets you boot the server by running `python main.py`. FastAPI itself can't serve HTTP. It needs an ASGI server, which is what Uvicorn is. The `uvicorn.run(app, ...)` call here is what actually accepts connections.

### Run it

```bash
python main.py
```

You should see Uvicorn print something like:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open <http://localhost:8000/> in your browser. You should see `{"ok":true}`.

## Frontend

The browser side. You'll use **Vite** to scaffold a React project. Vite is the build tool: it serves your source files during development with hot module reload, and bundles them for production when you ship.

### Scaffold the project

From the project root:

```bash
npm create vite@latest
cd frontend
npm install
```

### What this page needs to do

Open `frontend/src/App.jsx` and replace its contents with a component that fetches `http://localhost:8000/` on mount and renders the response so you can see it. Anything that gets the JSON visible on the page works (`<pre>{JSON.stringify(data, null, 2)}</pre>` is the lazy option).

Run it. The point is just confirming the frontend can reach the backend and read a response.
