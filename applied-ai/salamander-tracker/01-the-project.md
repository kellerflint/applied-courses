---
title: "The Project"
order: 1
---

Last quarter you tracked salamanders in video using color masking. That worked because the salamander stood out clearly from a plain backdrop. You picked a target color, masked the pixels in that range, computed the centroid, and logged a coordinate.

What happens when the backdrop has texture? When two salamanders overlap? When the lighting shifts mid-recording? Color masking starts to fall apart. The next step up is a method that learns what a salamander looks like rather than relying on color contrast.

That's what you're building this unit. A YOLO model trained on the same kind of footage you used before, wired into a web app that plays back a video with detections drawn over it.

This is your **midterm mini-project**. You have a week and a half. Work in pairs.

## What you're building

A web app that:

- Takes a video file as input
- Runs YOLO to detect salamanders in each frame
- Plays the video back with bounding boxes drawn over the salamanders
- Displays at least two metrics about what's being detected
- Exports the detection data as CSV or JSON

The salamander footage will be available on Canvas. If you have your own videos from the original research project, those work too.

## Stack

Python backend handling the YOLO model and video processing. React frontend for the UI. The Python piece is small: load a model, process a video, return data. Most of your work happens in React, which is your comfort zone.

You can use Flask or FastAPI on the Python side. Both work. Flask is simpler. FastAPI is more modern. Pick one and move on.

## Metrics: pick at least two

Your app needs to display at least two of these. You can substitute your own idea (run it by me first):

- **Live coordinates readout.** The bounding box centers from the current frame, shown in real time as the video plays.
- **Path trail.** A line drawn over the video showing where each salamander has moved.
- **Position heatmap.** A heat overlay showing where salamanders spent the most time across the whole video.
- **Dwell time per region.** Divide the frame into regions and show how much time was spent in each.
- **Speed over time.** Pixels per second, plotted as a chart that updates with playback.
- **Detection count over time.** How many salamanders were on screen at each moment.
- **Total distance traveled.** Per salamander, summed across the video.
- **Time on screen.** Per salamander, how long they were visible.

The last several require tracking individual salamanders across frames. Ultralytics has a `model.track()` method that handles ID assignment with a one-line code change, so this is easier than you might think.

> **With your partner:** Pick your two metrics now. Each one tells you something different about what the salamander did. What story do you want your app to tell?

## Deliverables

- A working app with clear run instructions in the README
- Your custom-trained YOLO model file committed to the repo
- A README that includes:
  - How many frames you labeled and what your dataset looked like
  - How to run the app
  - One paragraph comparing color masking to YOLO. Be specific about cases where each one would win.
- A 2-3 minute demo video, or a live demo in class

## On pace

You have a week and a half. The teams that have struggled most this term were the ones moving fastest with the least understanding. Slow down. Build in small pieces. Verify each piece works before adding the next. If you need an extension, ask before 5pm on the day it's due.
