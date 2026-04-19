"""
Review raw input images: show actual pixel value distributions and samples without any processing.
"""
import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATASET_PATH = os.path.join(os.path.dirname(__file__), "digit_dataset", "digits")
IMG_SIZE = 28

# Grab 5 raw samples per digit
samples = {d: [] for d in range(10)}
for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir) or not label_name.isdigit():
        continue
    d = int(label_name)
    for fname in sorted(os.listdir(label_dir))[:5]:
        if fname.endswith(".png"):
            img = Image.open(os.path.join(label_dir, fname)).convert("L")
            img = img.resize((IMG_SIZE, IMG_SIZE))
            samples[d].append(np.array(img, dtype=np.float32))

# ─── 1. Show raw images (no normalization) ───────────────────────────────────
fig, axes = plt.subplots(10, 5, figsize=(8, 16))
fig.suptitle("Raw input images (no processing)", fontsize=13)
for d in range(10):
    for col, arr in enumerate(samples[d]):
        ax = axes[d][col]
        ax.imshow(arr, cmap="gray_r", vmin=0, vmax=255)
        ax.set_xticks([]); ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(str(d), fontsize=10, rotation=0, labelpad=15)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "raw_inputs.png"), dpi=120, bbox_inches="tight")
plt.close()

# ─── 2. Pixel value histograms per digit ─────────────────────────────────────
fig, axes = plt.subplots(2, 5, figsize=(14, 6))
fig.suptitle("Pixel value distributions (raw 0–255)", fontsize=13)
for d in range(10):
    ax = axes[d // 5][d % 5]
    all_pixels = np.concatenate([a.flatten() for a in samples[d]])
    ax.hist(all_pixels, bins=50, color="steelblue", edgecolor="none")
    ax.set_title(f"digit {d}")
    ax.set_xlabel("pixel value")
    frac_binary = ((all_pixels < 20) | (all_pixels > 235)).mean()
    ax.set_title(f"digit {d}  |  {frac_binary:.0%} near-binary")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "pixel_histograms.png"), dpi=120, bbox_inches="tight")
plt.close()

# ─── 3. Print stats ──────────────────────────────────────────────────────────
print("Per-digit pixel stats (raw 0-255):")
print(f"{'digit':>6}  {'mean':>6}  {'std':>6}  {'min':>5}  {'max':>5}  {'% near-binary':>14}")
for d in range(10):
    all_pixels = np.concatenate([a.flatten() for a in samples[d]])
    frac = ((all_pixels < 20) | (all_pixels > 235)).mean()
    print(f"{d:>6}  {all_pixels.mean():>6.1f}  {all_pixels.std():>6.1f}  {all_pixels.min():>5.0f}  {all_pixels.max():>5.0f}  {frac:>14.1%}")

print("\nSaved: raw_inputs.png, pixel_histograms.png")
