---
title: "The Project"
order: 1
---

In prior quarters you tracked salamanders in video using color masking. That worked because the salamander stood out clearly from a plain backdrop. You picked a target color, masked the pixels in that range, computed the centroid, and logged a coordinate.

What happens when the backdrop has texture? When two salamanders show up? When the lighting shifts mid-recording? Color masking starts to fall apart. The next step up is a method that learns what a salamander looks like rather than relying on color contrast.

That's what you're building this unit. A YOLO model trained on the same kind of footage you used before, wired into a web app that plays back a video with detections drawn over it.

## What you're building

A web app that:

- Takes a video file as input
- Runs YOLO with tracking to detect salamanders in each frame and assign each one a stable ID across frames
- Plays the annotated video back with bounding boxes drawn over the salamanders
- Displays per-salamander metrics next to the video

The salamander footage will be available on Canvas. If you have your own videos from the original research project, those work too.

## Stack

Python backend with FastAPI handling the YOLO model and video processing. React frontend for the UI.

## How the pieces fit together

Before you write any code, you need a mental picture of what's happening when a user clicks "upload."

1. The **frontend** is a React app served by Vite at `localhost:5173`. The user picks a video file in the browser.
2. The frontend sends that file as a multipart upload to the **backend** at `localhost:8000/track`.
3. The backend saves the file to disk, then runs YOLO on every frame. For each detection it gets a bounding box, a class label, and a stable `track_id`.
4. The backend writes a new mp4 with the boxes drawn on top, and tallies per-individual metrics (like total time on screen).
5. Because that processing takes longer than the browser is willing to wait, the backend runs the work in a **background thread** and exposes a polling endpoint the frontend can hit every second or so for progress.
6. When the job is done, the backend's polling response includes a URL to the annotated mp4 and the metrics. The frontend renders the video and the metrics table.

> **With your partner:** Sketch the trip a single video takes. Where does it live at each step? What lives only in memory and what gets written to disk?

## Metrics

You'll be shown how to compute one metric end to end: **time on screen per individual salamander**. Once that's working, pick at least one additional metric to add yourself. Anything that pulls something meaningful out of the YOLO data. Some options:

- **Path trail.** A line drawn over the video showing where each salamander moved.
- **Position heatmap.** A heat overlay showing where salamanders spent the most time.
- **Dwell time per region.** Divide the frame into regions and measure how long each one held a salamander.
- **Detection count over time.** How many salamanders were on screen at each moment.
- **Total distance traveled.** Per salamander, summed across the video.
- **Max simultaneous detections.** The peak number of salamanders ever on screen at once.

Or pick your own that uses the data YOLO produces and shows something interesting.

## Deliverables

- A working app with clear run instructions in the README
- Your custom-trained YOLO model file committed to the repo
- A README that includes:
  - How many frames you labeled and a description of what your dataset and training pipeline looked like
  - How to run the app
  - One paragraph comparing color masking to YOLO. Provide specific recommendations for when to use which.

## How to use AI on this

You have AI access. Feel free to use it. The way you use it matters more than whether you use it.

**Build in small pieces.** Ask AI for one piece at a time. A single function. A single endpoint. A single component. Asking for the whole training pipeline or the whole web app at once produces something that mostly looks right and is very hard to debug.

**Read what it gives you.** Before running any AI-generated code, read through it. Can you explain what each line does? If you can't, that's the signal to slow down. AI will confidently produce code with subtle bugs that look fine until they don't.

**Verify before moving on.** Make one change, run it, confirm it works, then move on.

I can't emphasize this enough. The teams that have struggled most are the ones moving too fast, pasting in big chunks of AI code and trying to debug their way to something that works. Slow down. Build in small pieces. Verify each piece works before adding the next. If you need an extension, ask before 5pm on the day it's due. The fastest path through this project is the slow path: small pieces, fully understood, verified one at a time.
