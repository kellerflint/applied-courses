---
title: "Compare & Submit"
order: 5
---

You have three trained models. Now you're going to put their results side by side and actually think about what the differences mean.

## Confusion Matrices

Accuracy is a single number. A confusion matrix shows you where the model is making mistakes, which is much more useful.

Each row in a confusion matrix represents the actual class. Each column represents what the model predicted. The diagonal is where the model got it right. Everything off the diagonal is an error.

```python
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

class_names = [str(c) for c in sorted(set(y_test))]  # works whether y is a Series or array
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, (model_name, model_results) in zip(axes, results.items()):
    cm = confusion_matrix(y_test, model_results["predictions"])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(model_name)

plt.tight_layout()
plt.show()
```

> **With your partner:** Look at the three matrices side by side. For each model, identify:
> - Which class does it struggle with most?
> - Are the errors symmetric (does it confuse A for B as often as B for A), or does it lean one direction?
> - If your model were being used in a real application, which type of error would be more costly: false positives or false negatives?

## Accuracy Comparison

```python
model_names = list(results.keys())
accuracies = [results[m]["accuracy"] for m in model_names]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(model_names, accuracies, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylabel("Accuracy")
ax.set_title("Model Accuracy")
ax.set_ylim(min(accuracies) - 0.05, 1.0)

for bar, acc in zip(bars, accuracies):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.003,
        f"{acc:.3f}",
        ha="center", va="bottom", fontsize=11
    )
plt.tight_layout()
plt.show()
```

## Prediction Speed

How fast is each model when it actually needs to make predictions? This matters in production: a model that takes 200ms per request feels slow. Time each model predicting 100 samples.

```python
import time

sample_100 = X_test_scaled[:100]
REPEATS = 50  # repeat to get a stable average

def time_predict(model, X, repeats=REPEATS):
    start = time.perf_counter()
    for _ in range(repeats):
        model.predict(X)
    elapsed = (time.perf_counter() - start) / repeats
    return elapsed * 1000  # convert to milliseconds

models = [lr, rf, mlp]
times_ms = [time_predict(m, sample_100) for m in models]

for name, t in zip(model_names, times_ms):
    print(f"{name}: {t:.3f} ms")

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(model_names, times_ms, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylabel("Time (ms) for 100 predictions")
ax.set_title("Prediction Speed")
plt.tight_layout()
plt.show()
```

> **With your partner:** Before running this, guess the order: which model do you think is fastest? Which is slowest? Run it, then check. Were you surprised?

The result might not be what you expect. Random forest has to run every tree in the forest before it can return a prediction. On a forest of 100 trees, that adds up.

## Model Size

How much space does each model take up when saved? This matters for deployment: a model you ship to a mobile app or an edge device has real storage constraints.

```python
import pickle

def model_size_bytes(model):
    return len(pickle.dumps(model))

def human_size(b):
    if b < 1024:
        return f"{b} B"
    elif b < 1024 ** 2:
        return f"{b / 1024:.1f} KB"
    else:
        return f"{b / 1024 ** 2:.2f} MB"

sizes = [model_size_bytes(m) for m in models]
sizes_kb = [s / 1024 for s in sizes]

for name, s in zip(model_names, sizes):
    print(f"{name}: {human_size(s)}")

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(model_names, sizes_kb, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylabel("Size (KB)")
ax.set_title("Serialized Model Size")
for bar, s in zip(bars, sizes):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        human_size(s),
        ha="center", va="bottom", fontsize=10
    )
plt.tight_layout()
plt.show()
```

Logistic regression is tiny: it only stores one coefficient per feature. Random forest stores every node of every tree, which adds up fast. The neural network stores all its weights, which puts it somewhere in between.

> **With your partner:** Given everything you've seen across accuracy, speed, and size: which model would you actually deploy if this were a real project? What additional information would you want before making that call?

## Submit

**Share your notebook:**

1. Click **Share** in the top right of your Colab notebook
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**
3. Copy the link

**Each partner submits separately on Canvas.** Paste your shared Colab link into the submission. Both of you need to submit individually, even though it's the same notebook.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Comparing+ML+Models" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
