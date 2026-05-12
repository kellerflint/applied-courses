# Salamander Tracker, data & CLI POC

This folder holds the test videos, model weights, and the original standalone CLI from before the web app existed. The FastAPI backend pulls `yolov8n.pt` from here by default.

## Files

- `annotate.py`: original CLI script. Reads a video frame by frame, runs YOLO, writes an annotated copy.
- `yolov8n.pt`: default YOLO model (COCO classes). Swap in your trained `best.pt` for the salamander model.
- `ensantina.mp4`: full source footage.
- `ensantina_short.mp4`: first 30 seconds of the same video. Use this while iterating so you're not waiting on the full clip.
- `output.mp4`: last annotated output written by `annotate.py`.
- `requirements.txt`: just `ultralytics` + `opencv-python`. The backend venv already has both; if you'd rather not reuse it, you can make a separate venv here.

## Running `annotate.py`

The backend venv has everything `annotate.py` needs. Reuse it:

```bash
source ../backend/venv/bin/activate
python annotate.py ensantina_short.mp4
```

Annotated output goes to `output.mp4` in this folder.

### Options

- `-o annotated.mp4`: set the output path.
- `-m yolov8n.pt`: use a different YOLO model. Point this at your salamander `best.pt` when you have one.
- `-s 10`: only process the first N seconds of the input.

Example with a custom-trained model:

```bash
python annotate.py ensantina.mp4 -m runs/detect/train/weights/best.pt -o annotated.mp4
```

## What the script does

1. Opens the input video and reads its dimensions and frame rate.
2. Loops through frames one at a time.
3. Runs YOLO on each frame.
4. Uses Ultralytics' built-in `plot()` to draw boxes and labels onto the frame.
5. Writes each annotated frame to a new video file with the same dimensions and frame rate.

This is the same loop the FastAPI `/detect` endpoint uses, just without the metric extraction or the HTTP wrapping.
