"""
Visualize augmentation effects: show original + 6 augmented versions per sample.
Run with: python3.11 visualize_augmentation.py
"""

import os
import numpy as np
from PIL import Image
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATASET_PATH = os.path.join(os.path.dirname(__file__), "digit_dataset", "digits")
IMG_SIZE = 28

# Load one sample per digit class
samples = {}
for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir) or not label_name.isdigit():
        continue
    for fname in sorted(os.listdir(label_dir)):
        if fname.endswith(".png"):
            img = Image.open(os.path.join(label_dir, fname)).convert("L")
            img = img.resize((IMG_SIZE, IMG_SIZE))
            arr = np.array(img, dtype=np.float32) / 255.0
            samples[int(label_name)] = arr.reshape(1, IMG_SIZE, IMG_SIZE, 1)
            break

augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomRotation(0.042),
    tf.keras.layers.RandomTranslation(0.12, 0.12),
    tf.keras.layers.RandomZoom(0.12),
])

AUGMENTED_COLS = 6
digits = sorted(samples.keys())
fig, axes = plt.subplots(len(digits), 1 + AUGMENTED_COLS, figsize=(14, 18))
fig.suptitle("Original  |  6 augmented versions per digit", fontsize=13, y=1.01)

for row, digit in enumerate(digits):
    original = samples[digit]

    ax = axes[row][0]
    ax.imshow(original[0, :, :, 0], cmap="gray_r", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel(str(digit), fontsize=11, rotation=0, labelpad=15)
    if row == 0:
        ax.set_title("original", fontsize=9)

    for col in range(AUGMENTED_COLS):
        aug = augmentation(original, training=True).numpy()
        ax = axes[row][col + 1]
        ax.imshow(aug[0, :, :, 0], cmap="gray_r", vmin=0, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        if row == 0:
            ax.set_title(f"aug {col+1}", fontsize=9)

plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), "augmentation_samples.png")
plt.savefig(out, dpi=120, bbox_inches="tight")
plt.close()
print(f"Saved -> {out}")
