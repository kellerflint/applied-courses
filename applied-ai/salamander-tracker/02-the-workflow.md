---
title: "The Workflow"
order: 2
---

This page walks through the phases of the project. Each phase tells you what needs to happen and why, and the implementation is yours to figure out.

The order matters. Skipping ahead is the most common reason teams hit walls late in a project like this. If your dataset is broken, your model can't learn. If your model can't detect salamanders, your web app has nothing to show. Build each piece, verify it works, then move on.

## Phase 1: Build your dataset

YOLO trains on labeled images, so you'll start by extracting frames from your video footage and labeling them.

**Extract frames.** A 5-second clip at 30fps is 150 frames. Sampling every 10-30 frames usually gives you plenty of variety. `ffmpeg` and OpenCV can both do this in a few lines of code.

**Label in Label Studio.** You set this up during the last pair program, so it should be running locally already. Create a new project, import your frames, and configure object detection labeling with a single label called `salamander`. Draw a tight bounding box around each salamander in each frame. Export in YOLO with Images format when you're done.

**Aim for around 150 labeled frames.** Mix easy ones (clear shot, salamander centered) with hard ones (motion blur, partial occlusion, salamander near the edge of frame, weird angles). The model only learns what you show it, so a dataset of all easy frames produces a model that fails on hard frames.

> **With your partner:** Before you start labeling, look through your footage. What kinds of frames are easy? What kinds will be hard? Make sure your labeled set includes a mix of both.

## Phase 2: Train the model

Use Ultralytics. The goal of the first training run is to confirm that the model is learning at all, not to get the best possible accuracy.

Watch the training output. Loss should be going down. Validation metrics should be reasonable. If training loss is dropping but validation isn't improving, you might be overfitting on a small dataset. If neither is improving, something is wrong with your data or pipeline.

Once you have a model that's actually learning, you can scale up: more epochs, more data, or a bigger model variant if needed.

> **With your partner:** Watch your first training run together. Is the loss going down? If yes, what does that tell you? If no, where would you start looking?

## Phase 3: Run inference

Before building the web app, run two inference checkpoints.

**Inference on a single image.** Load your trained model, pass in one frame, draw the bounding box on the output image, save it. Look at it. Does it find the salamander? Is the box in the right place? Stop here until this works.

**Inference on a video.** Loop over the frames of one of your videos. Save an annotated copy to disk to watch where it succeeds and where it fails.

## Phase 4: Choose your metrics and define your data contract

Before you build the app, pick your what metrics you're going to show (at least two) and figure out what data your backend needs to produce for them.

Your backend has two outputs: an annotated copy of the video with bounding boxes drawn onto the frames, and the metric data the frontend will display. The frontend plays the annotated video back and displays the metrics alongside it.

Think through, for each metric, what the frontend needs from the backend:

- **Per-frame metrics** (live coordinates) just need each frame's detections.
- **Aggregate metrics** (heatmap, total distance, time on screen) need the backend to compute them once across the whole video and ship the result alongside the per-frame data.
- **Anything per-individual** (per-salamander dwell time, per-salamander distance) needs tracking across frames. Switch from `model.predict()` to `model.track()` and you'll get a stable `track_id` on each detection.

The answers define your data contract. Settling this now saves you from reshaping data and rewriting components mid-build.

> **With your partner:** Pick at least two metrics and sketch the JSON shape your backend will return for each. That's your contract. Get it concrete before you write the backend or the frontend.

## Phase 5: Build the app

Backend takes a video, runs YOLO, draws boxes onto each frame, and returns an annotated video plus the metric data. Frontend uploads the video, plays back the annotated version, and displays the metrics.

## Phase 6: Compare to color masking

Compare your old color masking approach to YOLO. Where does each one win? Color masking is fast and dead simple. YOLO handles harder cases but needs labeled data and training time. Both are the right tools for different jobs.