---
title: "Augmentation"
order: 2
---

Your data is normalized. Now you'll add variety.

Your dataset has about 1,400 images, roughly 140 per digit. That's enough to train a model, but the model will only ever see each digit drawn the way one specific person drew it on one specific day. Real handwriting has a lot more variation: different angles, stroke widths, sizes, and styles.

**Data augmentation** addresses this by randomly transforming training images each time they're fed to the model. The model sees the same images repeatedly during training, but each pass they look slightly different. This teaches the model that a slightly tilted "3" is still a "3", using the same images you already have.

## See it in action

Draw a digit below and click Augment to see what different transformations look like.

{% activity "data-augmentation-demo.html", "Data Augmentation Demo", "460px" %}

> **With your partner:** Draw the same digit in different positions or sizes. Does augmentation make the variants look more similar to each other? What kinds of variation are still not covered?

## What the transforms are doing

The augmentation function applies a random combination of these transforms each time an image is fed to the model during training:

**Rotate** tilts the digit up to 15 degrees in either direction. People don't always write straight, and the model should handle that.

**Translate** shifts the digit a few pixels up, down, left, or right. Even after bbox normalization there's still some positional variation, and this teaches the model to handle it.

**Zoom** scales the digit in or out. Some students naturally draw larger or smaller, and this covers that range.

**Dilate** fattens the stroke slightly using a morphological operation. Different people press harder when they write, leaving thicker or thinner strokes. Dilation simulates the thicker end of that range.

**Cutout** blacks out a small random rectangle somewhere in the image. This forces the model to recognize digits even when part of the stroke is hidden, so recognition has to work across the whole shape rather than any single region.

## The augmentation functions

Add these to your notebook. They operate on 2D arrays (height × width) and are composed randomly during training.

```python
import scipy.ndimage as ndi

def augment(img):
    # img arrives as (28, 28, 1) from the data pipeline
    g = img[:, :, 0] if img.ndim == 3 else img

    def rotate(g):
        angle = np.random.uniform(8, 15) * np.random.choice([-1, 1])
        return ndi.rotate(g, angle, reshape=False, cval=0.0)

    def translate(g):
        shift = int(IMG_SIZE * 0.12)
        return ndi.shift(g, [np.random.randint(-shift, shift + 1),
                              np.random.randint(-shift, shift + 1)], cval=0.0)

    def zoom(g):
        factor = np.random.uniform(0.75, 1.25)
        zoomed = ndi.zoom(g, factor)
        h, w = zoomed.shape
        if h >= IMG_SIZE:
            y0 = (h - IMG_SIZE) // 2
            zoomed = zoomed[y0:y0 + IMG_SIZE, :]
        else:
            pad = (IMG_SIZE - h) // 2
            zoomed = np.pad(zoomed, ((pad, IMG_SIZE - h - pad), (0, 0)))
        if w >= IMG_SIZE:
            x0 = (w - IMG_SIZE) // 2
            zoomed = zoomed[:, x0:x0 + IMG_SIZE]
        else:
            pad = (IMG_SIZE - w) // 2
            zoomed = np.pad(zoomed, ((0, 0), (pad, IMG_SIZE - w - pad)))
        return zoomed[:IMG_SIZE, :IMG_SIZE]

    def dilate(g):
        return ndi.binary_dilation(g > 0.5, iterations=1).astype(np.float32)

    def cutout(g, max_size=5):
        g = g.copy()
        size = np.random.randint(2, max_size + 1)
        y0   = np.random.randint(0, IMG_SIZE - size + 1)
        x0   = np.random.randint(0, IMG_SIZE - size + 1)
        g[y0:y0 + size, x0:x0 + size] = 0.0
        return g

    ops   = [rotate, translate, zoom, dilate]
    probs = [0.6, 0.6, 0.7, 0.5]

    # Guarantee at least 2 transforms fire each pass
    fired = [np.random.rand() < p for p in probs]
    if sum(fired) < 2:
        extras = [i for i, f in enumerate(fired) if not f]
        for i in np.random.choice(extras, size=2 - sum(fired), replace=False):
            fired[i] = True

    for op, do in zip(ops, fired):
        if do:
            g = op(g)

    return cutout(g).reshape(IMG_SIZE, IMG_SIZE, 1).astype(np.float32)
```

Each transform has its own probability. Rotate fires 60% of the time, zoom fires 70%, and so on. The `if sum(fired) < 2` block guarantees that at least two transforms always apply, so every image is modified before the model sees it.

To plug this into the `tf.data` pipeline:

```python
def tf_augment(image, label):
    image = tf.py_function(lambda img: augment(img.numpy()), [image], tf.float32)
    image.set_shape([IMG_SIZE, IMG_SIZE, 1])
    return image, label
```

`tf.py_function` lets you call regular Python (and NumPy/SciPy) code inside a TensorFlow data pipeline. The pipeline is optimized for speed, but it needs this wrapper for functions that use NumPy or SciPy, which require regular Python rather than TensorFlow's compiled graph mode.

## Preview before you train

Same rule as preprocessing: look at your augmented images before you commit to training. Augmentation settings that are too aggressive will destroy digits. Settings that are too conservative won't help.

```python
# Pick one sample per digit (after bbox normalization)
aug_samples = {}
for img, lbl in zip(images, labels):
    if lbl not in aug_samples:
        aug_samples[lbl] = img
    if len(aug_samples) == 10:
        break

NUM_COLS = 5
fig, axes = plt.subplots(10, 1 + NUM_COLS, figsize=((1 + NUM_COLS) * 1.5, 18))
axes[0][0].set_title("Original")
for col in range(1, 1 + NUM_COLS):
    axes[0][col].set_title(f"Aug {col}")

for row in range(10):
    orig = aug_samples[row]
    axes[row][0].imshow(orig, cmap="gray_r", vmin=0, vmax=1)
    axes[row][0].set_ylabel(str(row), rotation=0, labelpad=12)
    for col in range(1, 1 + NUM_COLS):
        axes[row][col].imshow(augment(orig)[:, :, 0], cmap="gray_r", vmin=0, vmax=1)
    for ax in axes[row]:
        ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout()
plt.savefig("check_augmentation.png", dpi=120, bbox_inches="tight")
plt.show()
```

> **With your partner:** Open `check_augmentation.png`. Are all 10 digits still clearly readable after augmentation? If anything looks unrecognizable, the transforms are too strong. If every sample looks almost identical to the original, they're too weak.

> **With your partner:** Augmentation only applies to the training set. The validation set uses the original, unmodified images. Why? What would happen to your accuracy numbers if you applied augmentation to the validation set too?

## Want to go further?

Two more techniques worth looking into if you want to experiment:

**Block masking** erases a larger rectangular region of the image during training. It forces the model to recognize digits even when part of the stroke is hidden.

**Stroke thickness variation** randomly dilates or erodes the drawn strokes before training. This helps because different people press harder or draw thicker.

Both are optional on this dataset. On harder problems, either can push accuracy higher.
