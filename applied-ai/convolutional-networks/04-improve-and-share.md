---
title: "Improve and Share"
order: 4
---

You have a working CNN and a comparison baseline. Before improving anything, look at your learning curves. They tell you what kind of problem you actually have.

Here is an example from the same datasets you just trained on:

{% image "overfitting-example.png", "Learning curves — overfitting example" %}

Both models show the same pattern: training accuracy keeps climbing while validation accuracy flattens out or drops. That gap is overfitting. The model is memorizing the training data rather than learning patterns that generalize.

This is normal and expected. The techniques below are possible options for addressing this pattern.

Now push the CNN accuracy higher. Try at least two techniques, keep track of what changed, and be ready to explain what worked and what didn't.

## Techniques to Try

**Dropout** reduces overfitting by randomly disabling a fraction of nodes on each training pass. This forces the network to build redundant pathways rather than relying on any single one. Add it after a conv block or dense layer:

```python
tf.keras.layers.Dropout(0.3)
```

Values between 0.2 and 0.5 are common starting points. If your training accuracy is much higher than your validation accuracy, dropout can help close that gap.

**Early stopping** lets the model stop automatically when validation accuracy stops improving. This means you can set a high epoch ceiling and let training end at the right point:

```python
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=5,
    restore_best_weights=True
)

model.fit(..., epochs=100, callbacks=[early_stop])
```

`restore_best_weights=True` rolls the model back to its best checkpoint, so you end up with the version that performed best even if accuracy dipped slightly in later epochs.

**Data augmentation** generates new training samples by applying random transformations to existing images. The underlying label stays the same. Only the presentation changes. This teaches the model that a slightly rotated or shifted version of a class still belongs to that class:

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1
)

model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    epochs=20,
    validation_data=(X_test, y_test)
)
```

Augmentation is most useful when your dataset is small. With a large dataset the variety is usually already there.

**Deeper architecture** helps when the model is underfitting (both training and validation accuracy are low and still climbing). Try a third conv block or increase the filter counts:

```python
tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
tf.keras.layers.MaxPooling2D((2, 2)),
```

> **With your partner:** After each change, look at your learning curves. Which technique had the biggest impact? Did anything make things worse? What would you try next if you had more time?

## Share-Out

Find a group that worked with a different dataset. Walk each other through:

- What dataset you picked
- What preprocessing steps you needed
- How the flat network and CNN compared on your data
- What you tried to improve the CNN and what actually helped

**Stay for the share-out. We'll start at 2:30.**

## Submit

When you are done, share your notebook:

1. Click **Share** in the top right of Colab
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**
3. Copy the link

**Both partners submit individually on Canvas** with the shared notebook link.

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Convolutional+Networks" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
