---
title: "Improve the Pipeline"
order: 1
---

Last time you built a digit recognizer. The model worked, but accuracy left room for improvement. This unit goes deeper: you'll improve the training pipeline and then deploy the model to a web server.

## What you're here to learn

You'll see a lot of code on these pages. You could describe any of these steps to an AI assistant and get working code back. What matters is that you understand what the steps are, why each one exists, and how to check that it worked.

If you can explain "I need to crop each image to the bounding box of the drawn pixels and resize it back to 28×28 so all digits are centered," you know enough to build this. The AI handles the implementation.

By the end of this unit you should be able to walk through the full training-to-deployment pipeline and explain what's happening at each stage. That's the kind of thing that comes up in interviews, in projects, and in conversations with teammates.

## The full pipeline

Here's every stage you'll build across this unit.

{% activity "training-pipeline.html", "Training Pipeline Overview", "560px" %}

> **With your partner:** Before reading ahead, click through each step in the pipeline. Talk through what you think is happening at each stage. Which steps make sense already? Which ones are unclear?

## The preprocessing problem

When students draw digits on a canvas, they draw them in different places and at different sizes. One student draws a tight little "7" in the top-left corner. Another draws a big "7" centered in the canvas.

Both are the same digit, but when you resize the full canvas to 28×28, they look very different to the model. The model spends capacity on positional variation that has nothing to do with what the digit looks like. That makes the problem harder than it needs to be.

**Bbox normalization** fixes this. For each image, it finds the bounding box of the drawn pixels, crops to that region, then resizes the crop back to 28×28. Every digit ends up centered and scaled to fill the canvas, so the model can focus on shape rather than position.

```python
IMG_SIZE = 28
BBOX_PAD = 2   # small border so the digit doesn't touch the edge

def bbox_normalize(img):
    rows = np.any(img > 0.2, axis=1)
    cols = np.any(img > 0.2, axis=0)

    if not rows.any():
        return img   # blank image, nothing to crop

    r0, r1 = np.where(rows)[0][[0, -1]]
    c0, c1 = np.where(cols)[0][[0, -1]]

    r0 = max(0, r0 - BBOX_PAD);  r1 = min(IMG_SIZE - 1, r1 + BBOX_PAD)
    c0 = max(0, c0 - BBOX_PAD);  c1 = min(IMG_SIZE - 1, c1 + BBOX_PAD)

    cropped = img[r0:r1+1, c0:c1+1]
    resized = Image.fromarray((cropped * 255).astype(np.uint8)).resize(
        (IMG_SIZE, IMG_SIZE), Image.LANCZOS
    )
    return np.array(resized, dtype=np.float32) / 255.0
```

The first two lines find which rows and columns contain any pixel above a brightness threshold. `np.where(rows)[0][[0, -1]]` picks the first and last row that had content, giving you the top and bottom of the bounding box. Same logic for columns gives you left and right. Then `BBOX_PAD` adds a small margin so the digit isn't flush against the edge after cropping.

Apply it when loading the dataset:

```python
raw_images, labels = [], []

for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir) or not label_name.isdigit():
        continue
    for fname in os.listdir(label_dir):
        if not fname.endswith(".png"):
            continue
        img = Image.open(os.path.join(label_dir, fname)).convert("L").resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img, dtype=np.float32) / 255.0
        raw_images.append(arr)
        labels.append(int(label_name))

raw_images = np.array(raw_images)
labels     = np.array(labels)

# Apply bbox normalization to every image
images = np.array([bbox_normalize(img) for img in raw_images])
```

## Always verify your preprocessing

**Verify every transform you apply before you train.** This habit will save you a lot of pain.

It is very easy to introduce a bug in preprocessing and not notice until hours later. Maybe you accidentally inverted the pixel values. Maybe the crop is slightly off. Maybe an edge case in the padding logic is corrupting some images. The only way to catch it is to look.

After any preprocessing step, visualize a sample of your data. Ask whether it looks right and whether it matches what the model should actually see.

```python
# Pick one sample per digit
samples = {}
for img, lbl in zip(raw_images, labels):
    if lbl not in samples:
        samples[lbl] = img
    if len(samples) == 10:
        break

fig, axes = plt.subplots(10, 2, figsize=(4, 22))
axes[0][0].set_title("Original")
axes[0][1].set_title("Bbox normalized")

for row in range(10):
    orig = samples[row]
    norm = bbox_normalize(orig)
    axes[row][0].imshow(orig, cmap="gray_r", vmin=0, vmax=1)
    axes[row][1].imshow(norm, cmap="gray_r", vmin=0, vmax=1)
    axes[row][0].set_ylabel(str(row), rotation=0, labelpad=12)
    for ax in axes[row]:
        ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout()
plt.savefig("check_bbox.png", dpi=120, bbox_inches="tight")
plt.show()
```

Open `check_bbox.png`. The right column should show each digit centered and scaled to fill the frame.

> **With your partner:** Do your normalized images look right? Pick a digit that was off-center or small in the original and check that the bounding box brought it in. Is there anything that looks broken?

> **With your partner:** This preprocessing step runs before training. But it also has to run at inference time, when a user draws a digit in the deployed app. Why? What would happen if you applied bbox normalization during training but skipped it in deployment?
