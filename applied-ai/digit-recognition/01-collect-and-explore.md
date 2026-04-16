---
title: "Collect and Explore"
order: 1
---

This unit is a class-wide project. Everyone contributes training data, and everyone trains a model on it. At the end you'll have a working digit recognizer and a leaderboard to see whose model scores highest.

Before you write a single line of code, you need to help build the dataset.

## Collect Your Digits

Go to **[http://64.23.245.76/](http://64.23.245.76/)** and click the **Collect Data** tab.

Enter your name and select your class from the dropdown. Then draw each digit five times. The site will prompt you through 0 to 9 in order. Take your time and draw clearly. Your handwriting becomes training data for everyone in the class.

When you've drawn all 50 digits, click submit.

> **With your partner:** What makes for a good training sample?

## Download the Dataset

Once the class has finished collecting, go to the **Data Review** tab. Click the **Download Training Zip** button in the top right. Save the zip somewhere you can find it. You'll upload it to Colab in the next step.

## Set Up Your Colab Notebook

Go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook. Share it with your partner.

Run this in the first cell to upload and extract the dataset:

```python
from google.colab import files
import zipfile

# Opens a file picker - select the zip you downloaded
uploaded = files.upload()

# Extract it
zip_name = list(uploaded.keys())[0]
with zipfile.ZipFile(zip_name, "r") as z:
    z.extractall("digit_dataset")

print("Done! Extracted to digit_dataset/")
```

After this runs, your notebook will have a `digit_dataset/` folder. Inside it is a `digits/` folder with subfolders named `0` through `9`, each containing PNG images of that digit drawn by your classmates.

## Load the Images

Now load those images into arrays. This is the same approach you'll use throughout the unit.

```python
import os
import numpy as np
from PIL import Image

DATASET_PATH = "digit_dataset/digits"
IMG_SIZE = 28

images = []
labels = []

for label_name in sorted(os.listdir(DATASET_PATH)):
    label_dir = os.path.join(DATASET_PATH, label_name)
    if not os.path.isdir(label_dir):
        continue
    for fname in os.listdir(label_dir):
        if not fname.endswith(".png"):
            continue
        img_path = os.path.join(label_dir, fname)
        img = Image.open(img_path).convert("L")   # convert to grayscale
        img = img.resize((IMG_SIZE, IMG_SIZE))     # make sure it's 28×28
        arr = np.array(img, dtype=np.float32) / 255.0  # normalize to 0-1
        images.append(arr.flatten())   # flatten 28×28 into a list of 784 numbers
        labels.append(int(label_name))

X = np.array(images)   # shape: (N, 784)
y = np.array(labels)   # shape: (N,)

print(f"Loaded {len(X)} images")
print(f"Shape: {X.shape}")
```

A few things to notice:

- `convert("L")` converts to grayscale. Each pixel becomes a single brightness value instead of separate red, green, and blue values.
- `/ 255.0` scales pixel values from 0–255 to 0–1. Neural networks train much better when inputs are small numbers.
- `flatten()` turns the 28×28 grid into a single list of 784 numbers. This is what the network receives as input.

## Images Are Just Numbers

Before you go any further, stop and make sure this idea is concrete.

{% activity "pixel-grid.html", "Pixels as Numbers", "780px" %}

Draw a digit in the grid above. Watch what happens to the numbers on the right. That list of values is what you just loaded into `X`. Every image in your dataset is one row of that array, and every value in that row is one pixel.

> **With your partner:** How many numbers does one 28×28 image produce when you flatten it?

<details>
<summary>Reveal answer</summary>

One image: 28 × 28 = **784 numbers**

</details>

## Visualize the Dataset

Run this to plot the first five samples of each digit class. You want to see what you're working with before training anything.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(10, 5, figsize=(8, 16))
fig.suptitle("First 5 samples per digit class", fontsize=13)

for digit in range(10):
    # find all images with this label
    digit_indices = np.where(y == digit)[0]
    for col in range(5):
        ax = axes[digit][col]
        if col < len(digit_indices):
            ax.imshow(X[digit_indices[col]].reshape(28, 28), cmap="gray_r")
        ax.set_xticks([])
        ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(str(digit), fontsize=10, rotation=0, labelpad=15)

plt.tight_layout()
plt.show()
```

`reshape(28, 28)` does the reverse of `flatten()`. It turns the list of 784 numbers back into a 2D grid so matplotlib can display it as an image. The data itself hasn't changed.

> **With your partner:** Look at the samples. Which digits look most similar to each other? Which ones do you expect the model to confuse most often?

On to training.
