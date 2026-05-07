---
title: "The Project"
order: 1
---

Last quarter you tracked salamanders in video using color masking. That worked because the salamander stood out clearly from a plain backdrop. You picked a target color, masked the pixels in that range, computed the centroid, and logged a coordinate.

What happens when the backdrop has texture? When two salamanders show up? When the lighting shifts mid-recording? Color masking starts to fall apart. The next step up is a method that learns what a salamander looks like rather than relying on color contrast.

That's what you're building this unit. A YOLO model trained on the same kind of footage you used before, wired into a web app that plays back a video with detections drawn over it.

## What you're building

A web app that:

- Takes a video file as input
- Runs YOLO to detect salamanders in each frame
- Plays the video back with bounding boxes drawn over the salamanders
- Displays at least two metrics about what's being detected

The salamander footage will be available on Canvas. If you have your own videos from the original research project, those work too.

## Stack

Python backend handling the YOLO model and video processing. React frontend for the UI.

You can use Flask or FastAPI on the Python side. Both work. Flask is simpler. FastAPI is more modern. Pick one.

## Metrics: pick at least two

Your app needs to display at least two of these or you can substitute your own idea.

- **Live coordinates readout.** The bounding box centers from the current frame, shown in real time as the video plays.
- **Path trail.** A line drawn over the video showing where each salamander has moved.
- **Position heatmap.** A heat overlay showing where salamanders spent the most time across the whole video.
- **Dwell time per region.** Divide the frame into regions and show how much time was spent in each.
- **Detection count over time.** How many salamanders were on screen at each moment.
- **Total distance traveled.** Per salamander, summed across the video.
- **Time on screen.** Per salamander, how long they were visible.

The last several require tracking individual salamanders across frames. Ultralytics has a `model.track()` method that handles ID assignment, so this is easier than you might think.

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

I can't emphasize this enough. The teams that have struggled most are the ones moving too fast, pasting in big chunks of AI code and trying to debug their way to something that works. Slow down. Build in small pieces. Verify each piece works before adding the next. If you need an extension, ask before 5pm on the day it's due. The fastest path through this project is the slow path: small pieces, fully understood, and verified one at a time.
