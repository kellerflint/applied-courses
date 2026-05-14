---
title: "Step 4: Per-Track Metrics"
order: 6
---

The annotated video shows where the salamanders are. This step turns that into numbers per individual: how many frames each tracked salamander was visible in, converted to seconds.

The mechanism: `model.track()` stamps each detection with a `track_id` that stays consistent for the same individual across frames. We collect data keyed by that id.

## Import defaultdict

At the top of `main.py`:

```python
from collections import defaultdict
```

It's a dict that returns a default value for missing keys, which makes counting much simpler than checking "is this key already there?" every time.

## Initialize the per-track state

Inside the `/track` handler, right before the frame loop:

```python
frames_seen = defaultdict(int)
label_for = {}
```

`frames_seen` will count how many frames each track id appeared in. `label_for` will store each track id's class label (like `"salamander"`).

## Update state inside the loop

Inside the frame loop, after `writer.write(result.plot())`:

```python
boxes = result.boxes
if boxes is not None and boxes.id is not None:
    for tid, cls_id in zip(boxes.id.tolist(), boxes.cls.tolist()):
        frames_seen[int(tid)] += 1
        label_for[int(tid)] = model.names[int(cls_id)]
```

`result.boxes` is `None` when there were no detections in this frame. `boxes.id` is `None` when there are detections but tracking hasn't assigned IDs yet, which can happen on the first frame or two. Skip both cases.

`boxes.id` and `boxes.cls` come back as torch tensors. `.tolist()` turns them into plain Python lists you can iterate.

`model.names` is a dict that maps class index to label string. If your model has one class, it's `{0: "salamander"}`.

**Check it works.** After the loop and the `release()` calls, before the `return`, add:

```python
print("frames_seen:", dict(frames_seen))
print("label_for:", label_for)
```

Upload a clip and watch the terminal. After the loop finishes, you should see something like:

```
frames_seen: {1: 454, 4: 9}
label_for: {1: 'salamander', 4: 'salamander'}
```

## Build the tracks list

In the same spot the prints were:

```python
tracks = [
    {
        "track_id": tid,
        "time_on_screen_s": round(count / fps, 2),
        "label": label_for[tid],
    }
    for tid, count in frames_seen.items()
]
```

This turns `frames_seen` into a list of one dict per unique track id, converting frame count to seconds using the source video's `fps`.

## Add it to the response

Update the return:

```python
return {
    "status": "done",
    "video_url": f"http://localhost:8000/videos/output.mp4?t={int(time.time())}",
    "tracks": tracks,
}
```

**Check it works.** Upload via the existing frontend, then look at the network tab. The JSON response should now include a `tracks` array like:

```json
{
  "status": "done",
  "video_url": "http://localhost:8000/videos/output.mp4?t=...",
  "tracks": [
    {"track_id": 1, "time_on_screen_s": 18.94, "label": "salamander"},
    {"track_id": 4, "time_on_screen_s": 0.38, "label": "salamander"}
  ]
}
```

## Render the table on the frontend

After the `<video>` tag, add a `<table>` with one row per entry in `data.tracks`. Columns: track id, label, time on screen.

**Check it works.** Upload through the page. You should see the video and a small table next to it, one row per tracked individual.