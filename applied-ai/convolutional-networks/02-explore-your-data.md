---
title: "Explore Your Data"
order: 2
---

Today you are picking a new image dataset, building a flat network and a CNN on it, and comparing them. This page covers the first step: picking your data and understanding it.

Before writing any model code, you need to understand what you are working with. **Exploratory data analysis (EDA)** means looking at your data carefully before training anything: checking the shape, understanding the class distribution, and actually seeing what the samples look like. Skipping this step leads to models that are hard to interpret and problems that show up late and are hard to diagnose.

This is a habit worth building. Do it every time.

## Pick Your Dataset

You can use one of the provided options or find your own.

**Provided options:**

| Dataset | Classes | Image size | Notes |
|---------|---------|------------|-------|
| Fashion-MNIST | 10 | 28×28 | Clothing categories: T-shirt, trouser, dress, etc. |
| EMNIST Letters | 26 | 28×28 | Handwritten uppercase letters |

**Fashion-MNIST** loads directly from Keras:

```python
import tensorflow as tf
import numpy as np

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
```

**EMNIST Letters** uses `tensorflow_datasets`, which is pre-installed on Colab. The slice notation (`train[:10000]`) loads only a subset so it doesn't take forever:

```python
import tensorflow_datasets as tfds
import numpy as np

(ds_train, ds_test), info = tfds.load(
    'emnist/letters',
    split=['train[:10000]', 'test[:2000]'],
    as_supervised=True,
    with_info=True
)

X_train = np.array([x.numpy() for x, _ in ds_train])
y_train = np.array([y.numpy() for _, y in ds_train])
X_test  = np.array([x.numpy() for x, _ in ds_test])
y_test  = np.array([y.numpy() for _, y in ds_test])

# EMNIST labels are 1-based (1–26) — shift to 0-based
y_train = y_train - 1
y_test  = y_test  - 1
```

**Finding your own:** Browse [Kaggle datasets](https://www.kaggle.com/datasets) (filter by image format) or [Hugging Face datasets](https://huggingface.co/datasets). Look for an image classification problem with at least 5 classes. You have already loaded image datasets from files for the digit project. Apply the same approach.

**Constraints to keep in mind:**

- Images must be grayscale, or converted to grayscale
- Resize to 32×32 or smaller if images are large. Larger images produce much larger models.
- If training takes more than a few minutes later, stop and reduce something: fewer classes, fewer samples, or smaller images. Don't hang out waiting for giant models that will take an hour to train! Reduce the load so it takes a few minutes at most.

## Explore the Data

Answer these questions before building anything. Run each block, look at the output, and discuss with your partner.

### Shape and size

```python
print(f"Training samples:  {X_train.shape[0]}")
print(f"Test samples:      {X_test.shape[0]}")
print(f"Image size:        {X_train.shape[1:]}")
print(f"Number of classes: {len(np.unique(y_train))}")
print(f"Pixel value range: {X_train.min()} to {X_train.max()}")
```

### Class distribution

```python
import matplotlib.pyplot as plt

counts = np.bincount(y_train)
labels = class_names if 'class_names' in dir() else [str(i) for i in range(len(counts))]

plt.figure(figsize=(10, 4))
plt.bar(range(len(counts)), counts)
plt.xticks(range(len(counts)), labels, rotation=45, ha='right')
plt.ylabel("Count")
plt.title("Samples per class")
plt.tight_layout()
plt.show()
```

> **With your partner:** Is the dataset balanced across classes? How might a large imbalance affect model performance?

<details>
<summary>Reveal answer</summary>

An imbalanced dataset means the model sees some classes far more than others during training. It tends to bias predictions toward the majority class. Accuracy scores can be misleading in this case. A model that always predicts the most common class can look decent on paper while being nearly useless on rare classes.

</details>

### Sample images

Looking at actual examples from each class is one of the most useful things you can do before training. It helps you spot quality issues, understand how visually similar classes are, and predict where the model will struggle.

```python
num_classes = len(np.unique(y_train))
labels = class_names if 'class_names' in dir() else [str(i) for i in range(num_classes)]

fig, axes = plt.subplots(num_classes, 5, figsize=(8, num_classes * 1.6))
fig.suptitle("5 samples per class", fontsize=13)

for label in range(num_classes):
    idxs = np.where(y_train == label)[0][:5]
    for col in range(5):
        ax = axes[label][col]
        if col < len(idxs):
            ax.imshow(X_train[idxs[col]], cmap='gray_r')
        ax.axis('off')
        if col == 0:
            ax.set_ylabel(labels[label], fontsize=8, rotation=0, labelpad=50, va='center')

plt.tight_layout()
plt.show()
```

> **With your partner:** Which classes look most similar to each other? Where do you expect the model to make the most mistakes?

## Prepare for Training

Your data needs to be in a specific shape before training: `(samples, height, width, channels)`. The channel dimension is new. Grayscale images have 1 channel. Color images have 3 (RGB). The CNN needs this shape to understand the spatial structure of each image.

Two steps remain before training: normalize and reshape.

**Normalize** pixel values from 0–255 to 0–1. Neural networks train faster and more stably with small float inputs:

```python
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0
```

**Reshape** to add the channel dimension. CNNs expect input shape `(samples, height, width, channels)`. Grayscale images have 1 channel:

```python
H, W = X_train.shape[1], X_train.shape[2]

X_train = X_train.reshape(-1, H, W, 1)
X_test  = X_test.reshape(-1, H, W, 1)

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape:  {X_test.shape}")
```

The `-1` in reshape means "figure out this dimension automatically based on the total number of samples."

> **With your partner:** What does your final `X_train.shape` look like? What does each number represent?
