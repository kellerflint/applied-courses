"""
V4: same pipeline as V3 (bbox norm, augmentation, 5s oversampled) but with a CNN instead of dense NN.
Run with: python3.11 digit_test_v4.py
"""

import os
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print(f"TensorFlow version: {tf.__version__}")

DATASET_PATH = os.path.join(os.path.dirname(__file__), "digit_dataset", "digits")
IMG_SIZE = 28
BBOX_PAD = 2

# ─── 1. Load + bbox-normalize ─────────────────────────────────────────────────
def bbox_normalize(arr):
    g = arr[:, :, 0]
    rows = np.any(g > 0.2, axis=1); cols = np.any(g > 0.2, axis=0)
    if not rows.any(): return arr
    r0, r1 = np.where(rows)[0][[0, -1]]
    c0, c1 = np.where(cols)[0][[0, -1]]
    r0=max(0,r0-BBOX_PAD); r1=min(IMG_SIZE-1,r1+BBOX_PAD)
    c0=max(0,c0-BBOX_PAD); c1=min(IMG_SIZE-1,c1+BBOX_PAD)
    cropped = g[r0:r1+1, c0:c1+1]
    pil = Image.fromarray((cropped*255).astype(np.uint8)).resize((IMG_SIZE,IMG_SIZE), Image.LANCZOS)
    return (np.array(pil, dtype=np.float32)/255.0).reshape(IMG_SIZE, IMG_SIZE, 1)

images, labels = [], []
for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir) or not label_name.isdigit(): continue
    for fname in os.listdir(label_dir):
        if not fname.endswith(".png"): continue
        img = Image.open(os.path.join(label_dir, fname)).convert("L").resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img, dtype=np.float32) / 255.0
        images.append(bbox_normalize(arr.reshape(IMG_SIZE, IMG_SIZE, 1)))
        labels.append(int(label_name))

X = np.array(images)
y = np.array(labels)
print(f"\nLoaded {len(X)} images (bbox-normalized)")
print(f"Label counts: { {d: int((y==d).sum()) for d in range(10)} }")

# ─── 2. Augmentation ──────────────────────────────────────────────────────────
def _rotate(g):
    return ndi.rotate(g, np.random.uniform(8,15)*np.random.choice([-1,1]), reshape=False, cval=0.0)

def _translate(g):
    s = int(IMG_SIZE*0.12)
    return ndi.shift(g, [np.random.randint(-s,s+1), np.random.randint(-s,s+1)], cval=0.0)

def _zoom(g):
    zoomed = ndi.zoom(g, np.random.uniform(0.75, 1.25))
    h, w = zoomed.shape
    if h >= IMG_SIZE:
        y0 = (h-IMG_SIZE)//2; zoomed = zoomed[y0:y0+IMG_SIZE, :]
    else:
        pad = (IMG_SIZE-h)//2; zoomed = np.pad(zoomed, ((pad, IMG_SIZE-h-pad), (0,0)))
    if w >= IMG_SIZE:
        x0 = (w-IMG_SIZE)//2; zoomed = zoomed[:, x0:x0+IMG_SIZE]
    else:
        pad = (IMG_SIZE-w)//2; zoomed = np.pad(zoomed, ((0,0), (pad, IMG_SIZE-w-pad)))
    return zoomed[:IMG_SIZE, :IMG_SIZE]

def _dilate(g):
    return ndi.binary_dilation(g > 0.5, iterations=1).astype(np.float32)

def _cutout(g, max_size=5):
    g = g.copy()
    size = np.random.randint(2, max_size+1)
    y0 = np.random.randint(0, IMG_SIZE-size+1)
    x0 = np.random.randint(0, IMG_SIZE-size+1)
    g[y0:y0+size, x0:x0+size] = 0.0
    return g

_OPS = [_rotate, _translate, _zoom, _dilate]
_BASE_PROBS = [0.6, 0.6, 0.7, 0.5]

def augment(img):
    g = img[:, :, 0]
    fired = [np.random.rand() < p for p in _BASE_PROBS]
    if sum(fired) < 2:
        not_fired = [i for i,f in enumerate(fired) if not f]
        for i in np.random.choice(not_fired, size=2-sum(fired), replace=False):
            fired[i] = True
    for op, do in zip(_OPS, fired):
        if do: g = op(g)
    return _cutout(g).reshape(IMG_SIZE, IMG_SIZE, 1).astype(np.float32)

def tf_augment(image, label):
    image = tf.py_function(lambda img: augment(img.numpy()), [image], tf.float32)
    image.set_shape([IMG_SIZE, IMG_SIZE, 1])
    return image, label

# ─── 3. Augmentation preview ──────────────────────────────────────────────────
_preview_samples = {}
for _img, _lbl in zip(X, y):
    if _lbl not in _preview_samples: _preview_samples[_lbl] = _img
    if len(_preview_samples) == 10: break

AUG_COLS = 6
fig, axes = plt.subplots(10, 1+AUG_COLS, figsize=((1+AUG_COLS)*1.4, 18))
for col, title in enumerate(["bbox'd"] + [f"aug {i+1}" for i in range(AUG_COLS)]):
    axes[0][col].set_title(title, fontsize=8)
for row in range(10):
    orig = _preview_samples[row]
    axes[row][0].imshow(orig[:,:,0], cmap="gray_r", vmin=0, vmax=1)
    axes[row][0].set_ylabel(str(row), fontsize=10, rotation=0, labelpad=12)
    for col in range(1, 1+AUG_COLS):
        axes[row][col].imshow(augment(orig)[:,:,0], cmap="gray_r", vmin=0, vmax=1)
    for ax in axes[row]: ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("V4 augmentation preview (CNN, bbox-normalized)", fontsize=11, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "augmentation_preview_v4.png"), dpi=120, bbox_inches="tight")
plt.close()
print("Saved augmentation preview")

# ─── 4. Train / test split + oversample 5s ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
val_size = max(1, int(len(X_train) * 0.1))
X_val, y_val = X_train[-val_size:], y_train[-val_size:]
X_tr,  y_tr  = X_train[:-val_size], y_train[:-val_size]

fives_mask = y_tr == 5
X_tr = np.concatenate([X_tr, X_tr[fives_mask], X_tr[fives_mask]])
y_tr = np.concatenate([y_tr, y_tr[fives_mask], y_tr[fives_mask]])

print(f"\nTrain: {len(X_tr)} (5s oversampled 3x), Val: {len(X_val)}, Test: {len(X_test)}")

BATCH_SIZE = 32
train_ds = (
    tf.data.Dataset.from_tensor_slices((X_tr, y_tr))
    .shuffle(len(X_tr), reshuffle_each_iteration=True)
    .map(tf_augment, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)
val_ds = (
    tf.data.Dataset.from_tensor_slices((X_val, y_val))
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

# ─── 5. Build CNN ─────────────────────────────────────────────────────────────
# Two conv blocks to learn local stroke features, then a small dense head.
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 1))

x = tf.keras.layers.Conv2D(32, 3, padding="same")(inputs)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation("relu")(x)
x = tf.keras.layers.Conv2D(32, 3, padding="same")(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation("relu")(x)
x = tf.keras.layers.MaxPooling2D(2)(x)   # 28x28 -> 14x14
x = tf.keras.layers.Dropout(0.25)(x)

x = tf.keras.layers.Conv2D(64, 3, padding="same")(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation("relu")(x)
x = tf.keras.layers.Conv2D(64, 3, padding="same")(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation("relu")(x)
x = tf.keras.layers.MaxPooling2D(2)(x)   # 14x14 -> 7x7
x = tf.keras.layers.Dropout(0.25)(x)

x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(128)(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Activation("relu")(x)
x = tf.keras.layers.Dropout(0.5)(x)

outputs = tf.keras.layers.Dense(10, activation="softmax")(x)

model = tf.keras.Model(inputs, outputs)
model.summary()
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ─── 6. Callbacks ─────────────────────────────────────────────────────────────
callbacks = [
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=8, min_lr=1e-5, verbose=1
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=30, restore_best_weights=True, verbose=1
    ),
]

# ─── 7. Train ─────────────────────────────────────────────────────────────────
print("\nTraining...")
history = model.fit(
    train_ds,
    epochs=300,
    validation_data=val_ds,
    callbacks=callbacks,
    verbose=1
)

# ─── 8. Evaluate ──────────────────────────────────────────────────────────────
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nBaseline test accuracy: {test_acc:.4f}")
print(f"Baseline test loss:     {test_loss:.4f}")

# ─── 8b. TTA ──────────────────────────────────────────────────────────────────
TTA_ROUNDS = 25
print(f"\nRunning TTA ({TTA_ROUNDS} rounds)...")
softmax_accum = model.predict(X_test, verbose=0)
for r in range(TTA_ROUNDS - 1):
    softmax_accum += model.predict(np.array([augment(img) for img in X_test]), verbose=0)
    if (r+2) % 5 == 0: print(f"  round {r+2}/{TTA_ROUNDS}")

tta_preds = np.argmax(softmax_accum, axis=1)
tta_acc   = (tta_preds == y_test).mean()
print(f"TTA test accuracy:      {tta_acc:.4f}  ({tta_acc - test_acc:+.4f} vs baseline)")

# ─── 9. Confusion matrix ──────────────────────────────────────────────────────
y_pred = tta_preds
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(cm, cmap="Blues")
plt.colorbar(im, ax=ax)
ax.set_xticks(range(10)); ax.set_yticks(range(10))
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
ax.set_title(f"V4 CNN  |  TTA acc {tta_acc:.1%}  (baseline {test_acc:.1%})")
for i in range(10):
    for j in range(10):
        ax.text(j, i, str(cm[i,j]), ha="center", va="center",
                color="white" if cm[i,j] > cm.max()*0.5 else "black", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "confusion_matrix_v4.png"), dpi=120, bbox_inches="tight")
plt.close()
print("Saved confusion matrix")

# ─── 9b. Misclassified images ─────────────────────────────────────────────────
wrong_idx = np.where(y_pred != y_test)[0]
print(f"\nMisclassified: {len(wrong_idx)} / {len(y_test)}")

if len(wrong_idx) > 0:
    cols = min(len(wrong_idx), 10)
    rows = (len(wrong_idx) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols*1.8, rows*2.4))
    if rows == 1: axes = axes[np.newaxis, :]
    for ax in axes.flat: ax.axis("off")
    confidences = softmax_accum / TTA_ROUNDS
    for i, idx in enumerate(wrong_idx):
        ax = axes[i//cols][i%cols]
        ax.imshow(X_test[idx,:,:,0], cmap="gray_r", vmin=0, vmax=1)
        conf = confidences[idx, y_pred[idx]]
        ax.set_title(f"true: {y_test[idx]}\npred: {y_pred[idx]}  ({conf:.0%})", fontsize=9, color="red")
        ax.axis("off")
    plt.suptitle(f"V4 misclassified ({len(wrong_idx)} / {len(y_test)})", fontsize=12, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "misclassified_v4.png"), dpi=140, bbox_inches="tight")
    plt.close()
    print(f"Saved misclassified images")

# ─── 10. Training curve ───────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history.history["accuracy"], label="train")
ax1.plot(history.history["val_accuracy"], label="val")
ax1.set_title("Accuracy"); ax1.set_xlabel("Epoch"); ax1.legend()
ax2.plot(history.history["loss"], label="train")
ax2.plot(history.history["val_loss"], label="val")
ax2.set_title("Loss"); ax2.set_xlabel("Epoch"); ax2.legend()
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "training_curve_v4.png"), dpi=100, bbox_inches="tight")
plt.close()

# ─── 11. Export ───────────────────────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), "digit_model_v4.keras")
model.save(model_path)
print(f"\nModel saved -> {model_path}")

loaded = tf.keras.models.load_model(model_path)
preds = np.argmax(loaded.predict(X_test[:3], verbose=0), axis=1)
print(f"\nSample predictions: {preds}")
print(f"Actual labels:      {y_test[:3]}")
print("\nAll done.")
