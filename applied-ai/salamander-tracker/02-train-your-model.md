---
title: "Train Your Model"
order: 2
---

Before you build anything else, you need a YOLO model that can actually recognize salamanders. That work happens in a separate walkthrough repo I put together for this purpose. Go work through it end to end, then come back here.

**[Applied-AI-YOLO-Walkthrough](https://github.com/kellerflint/Applied-AI-YOLO-Walkthrough)**

The repo walks you through capturing images, labeling them, training a YOLO model on the result, and verifying it works against your webcam in real time. By the time you're done you should have a `best.pt` file (your trained model weights) sitting in a `runs/detect/train/weights/` folder, and you should have seen the model successfully detect salamanders in a live video feed.

You'll copy that `best.pt` into your project later and the backend will load it from there.

## Capturing your own data

You don't need to use the Canvas footage. The plastic salamanders work great for capturing your own data. The walkthrough repo has two scripts for this:

**`scripts/capture.py`** snaps individual frames (press SPACE on each one). This is what you'll feed into Label Studio for training. Position the salamander, snap, reposition, snap again. Vary angles, distances, lighting, and backgrounds. Aim for 50+ frames across a good range of setups.

**`scripts/record.py`** records video clips (press R to start, R again to stop). You don't label video frames, but you do need a video to upload to the tracker app once you've built it. Record a clip where you move a salamander around the frame, or move the camera around it. You want actual motion to track.

A model trained only on still-image captures still works on video at inference time. YOLO runs on one frame at a time regardless of whether the source was an image or a video, so a still-image training set is fine for a video-inference target.

## A few notes specific to the salamander case

**Use rectangle (axis-aligned) bounding boxes in Label Studio. Do not rotate them.** YOLO supports a separate "oriented bounding box" mode that uses a different model variant and a different label format. If you rotate your boxes in Label Studio while training a regular YOLO model, the labels and the model don't match and you can encounter issues during training. Stick to plain axis-aligned rectangles.

**Aim for at least 50 labeled frames (more is better).** Sample frames from across your videos rather than 150 consecutive frames of the same clip.

**Mix easy and hard frames.** Clear shots with the salamander centered are easy. Motion blur, partial occlusion, salamander near the edge of frame, weird angles, low light. A dataset of all easy frames produces a model that fails on hard frames. Look at your footage and pick a mix on purpose.

> **With your partner:** Before you start labeling, scroll through your footage. What kinds of frames will be easy for the model? What kinds will be hard? Make sure your labeled set has both.

## When you're done

You should have:

- A trained model file (the `best.pt` from the walkthrough)
- Confidence that it actually finds salamanders.

If your model doesn't recognize anything, go back and look at your training output and your dataset before moving on. Building the web app around a model that doesn't work means you'll have nothing to show in the end.
