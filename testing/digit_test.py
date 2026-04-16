"""
Digit recognition test script using TensorFlow + Keras.
Validates the full pipeline against the local digit_dataset before writing lesson content.

Run with: python3.11 digit_test.py
"""

import os
import numpy as np
from PIL import Image
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

print(f"TensorFlow version: {tf.__version__}")

# ─── 1. Load dataset ──────────────────────────────────────────────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "digit_dataset", "digits")
IMG_SIZE = 28

images = []
labels = []

for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir) or not label_name.isdigit():
        continue
    for fname in os.listdir(label_dir):
        if not fname.endswith(".png"):
            continue
        img_path = os.path.join(label_dir, fname)
        # Open, convert to grayscale, resize to 28x28
        img = Image.open(img_path).convert("L")
        img = img.resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img, dtype=np.float32) / 255.0  # normalize to [0, 1]
        images.append(arr.flatten())  # flatten 28x28 -> 784
        labels.append(int(label_name))

X = np.array(images)   # shape: (N, 784)
y = np.array(labels)   # shape: (N,)

print(f"\nLoaded {len(X)} images")
print(f"Feature shape: {X.shape}")
print(f"Label counts: { {d: int((y==d).sum()) for d in range(10)} }")
print(f"Pixel value range: [{X.min():.2f}, {X.max():.2f}]")

# ─── 2. Visualize first 5 of each digit ──────────────────────────────────────
fig, axes = plt.subplots(10, 5, figsize=(8, 16))
fig.suptitle("First 5 samples of each digit class", fontsize=13, y=1.01)

for digit in range(10):
    digit_indices = np.where(y == digit)[0]
    shown = digit_indices[:5]
    for col in range(5):
        ax = axes[digit][col]
        if col < len(shown):
            ax.imshow(X[shown[col]].reshape(IMG_SIZE, IMG_SIZE), cmap="gray_r")
        ax.set_xticks([])
        ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(str(digit), fontsize=10, rotation=0, labelpad=15)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "sample_visualization.png")
plt.savefig(out_path, dpi=100, bbox_inches="tight")
plt.close()
print(f"\nSaved sample visualization -> {out_path}")

# ─── 3. Train / test split ────────────────────────────────────────────────────
# With only ~63 samples the test set will be small; that's expected.
# The real dataset will have many more once the whole class contributes.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTrain samples: {len(X_train)}, Test samples: {len(X_test)}")

# ─── 4. Build model ───────────────────────────────────────────────────────────
# Simple feedforward (fully-connected) network.
# Input: 784 pixel values (one per pixel of the 28x28 image)
# Hidden: two dense layers with ReLU activation
# Output: 10 nodes (one per digit class), softmax gives class probabilities

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(784,)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

model.summary()

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ─── 5. Train ─────────────────────────────────────────────────────────────────
print("\nTraining...")
history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=8,          # small batch for small dataset
    validation_split=0.1,
    verbose=1
)

# ─── 6. Evaluate ──────────────────────────────────────────────────────────────
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest accuracy: {test_acc:.4f}")
print(f"Test loss:     {test_loss:.4f}")

# ─── 7. Export model ──────────────────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), "digit_model.keras")
model.save(model_path)
print(f"\nModel saved -> {model_path}")

# ─── 8. Verify model can be reloaded and predict ──────────────────────────────
loaded = tf.keras.models.load_model(model_path)
sample = X_test[:3]
preds = np.argmax(loaded.predict(sample, verbose=0), axis=1)
print(f"\nSample predictions (should be digits): {preds}")
print(f"Actual labels:                         {y_test[:3]}")
print("\nAll done. Pipeline validated.")
