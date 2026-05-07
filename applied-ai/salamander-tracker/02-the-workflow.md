---
title: "The Workflow"
order: 2
---

This page walks through the phases of the project. Each phase tells you what needs to happen and why, and the implementation is yours to figure out.

The order matters. Skipping ahead is the most common reason teams hit walls late in a project like this. If your dataset is broken, your model can't learn. If your model can't detect salamanders, your web app has nothing to show. Build each piece, verify it works, then move on.

## Phase 1: Build your dataset

YOLO trains on labeled images, so you'll start by extracting frames from your video footage and labeling them.

**Extract frames.** A 5-second clip at 30fps is 150 frames. Sampling every 10-30 frames usually gives you plenty of variety. `ffmpeg` and OpenCV can both do this in a few lines of code.

**Label in Label Studio.** You set this up during the last pair program, so it should be running locally already. Create a new project, import your frames, and configure object detection labeling with a single label called `salamander`. Draw a tight bounding box around each salamander in each frame. Export in YOLO format when you're done.

**Aim for around 150 labeled frames.** Mix easy ones (clear shot, salamander centered) with hard ones (motion blur, partial occlusion, salamander near the edge of frame, weird angles). The model only learns what you show it, so a dataset of all easy frames produces a model that fails on hard frames.

> **With your partner:** Before you start labeling, look through your footage. What kinds of frames are easy? What kinds will be hard? Make sure your labeled set includes a mix of both.

## Phase 2: Train the model

Use Ultralytics. Start with the smallest model (`yolov8n`) and a small number of epochs. The goal of the first training run is to confirm that the model is learning at all, not to get the best possible accuracy.

Watch the training output. Loss should be going down. Validation metrics should be reasonable. If training loss is dropping but validation isn't improving, you might be overfitting on a small dataset. If neither is improving, something is wrong with your data.

Once you have a model that's actually learning, you can scale up: more epochs, more data, or a bigger model variant if needed.

> **With your partner:** Watch your first training run together. Is the loss going down? If yes, what does that tell you? If no, where would you start looking?

## Phase 3: Run inference

Before building the web app, run two inference checkpoints.

**Inference on a single image.** Load your trained model, pass in one frame, draw the bounding box on the output image, save it. Look at it. Does it find the salamander? Is the box in the right place? Stop here until this works.

**Inference on a video.** Loop over the frames of one of your videos. Either save an annotated copy to disk to watch, or print the detections to the console. Watch where it succeeds and where it fails.

These two steps are five-minute scripts each. They save you from chasing bugs in your web app that turn out to be model bugs.

## Phase 4: Build the web app with mocks first

Build the web app in pieces, with mock data first. Each step below should work on its own before you move to the next.

**Start with a fake backend.** Make your `/process` endpoint return hardcoded detection data: a JSON array with a few fake bounding boxes per frame. The frontend treats this the same way it would treat real data. You can build the entire video playback and box overlay against this mock.

**Get one box drawn first.** Display the video. Draw a single hardcoded box on top of it. When that works, sync it to playback time. When that works, swap the hardcoded box for boxes from your fake backend. When that works, swap the fake backend for your real YOLO model.

Each of those four steps is small. Each one is testable on its own. When something breaks (and it will), you'll know exactly which step caused it.

The teams that try to wire everything up at once spend most of the week trying to figure out which of five things is broken. The teams that build in steps spend the same time actually moving forward.

> **With your partner:** Sketch the data flow before writing any code. The frontend uploads a video, then what? What does the backend send back? When does the frontend draw boxes? Get this clear in your heads before you build it.

## Phase 5: Add your metrics

Once basic playback with boxes is working, add your two metrics.

For metrics that need data across all frames (heatmap, total distance, time on screen), you'll want the backend to compute them once during processing and send them with the detections. For per-frame metrics (live coordinates, current speed), the frontend can compute them as the video plays.

If your metrics need individual salamander tracking, switch from `model.predict()` to `model.track()` in your inference code. Ultralytics adds a `track_id` to each detection automatically. From there, grouping detections by ID is straightforward.

## Phase 6: Compare to color masking

Take your old color masking code and run it on the same video you tested YOLO with. A scrappy script that prints centroids per frame is enough.

Now compare. Where does each one win? Be honest. Color masking is fast and dead simple. YOLO handles harder cases but needs labeled data and training time. Both are right tools for different jobs. The README reflection should make this concrete with examples from your actual videos.

## How to use AI on this

You have AI access. Use it. The way you use it matters more than whether you use it.

**Build in small pieces.** Ask AI for one piece at a time. A single function. A single endpoint. A single component. Asking for the whole training pipeline or the whole web app at once produces something that mostly looks right and is very hard to debug.

**Read what it gives you.** Before running any AI-generated code, read through it. Can you explain what each line does? If you can't, that's the signal to slow down. AI will confidently produce code with subtle bugs that look fine until they don't.

**Verify before moving on.** Make one change, run it, confirm it works, then move on. This is the habit that separates teams that finish from teams that don't.

I can't emphasize this enough. Some teams keep pasting in big chunks of AI code and trying to debug their way to something that works. The fastest path through this project is the slow path: small pieces, verified one at a time.
