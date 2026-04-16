---
title: "Improving Your Model"
order: 3
---

You have a working baseline. Now you're going to try to push it higher on the leaderboard.

There's no single right answer here. Different techniques work better or worse depending on your data, and part of learning is figuring out what helps and what doesn't. For each technique below, read through the concept, look at the code, then decide whether and how to apply it to your model.

After you make changes, retrain, re-export, and resubmit to see if your score improves.

## Dropout

Your model will likely overfit if you train it for too many epochs. **Overfitting** means the model has memorized the training data. It learns to recognize the exact samples it trained on, and those patterns break down on new samples. Training accuracy looks great while test accuracy stays low.

**Dropout** is one of the simplest tools for fighting overfitting. During training, dropout randomly disables a fraction of the nodes in a layer on each pass. Those nodes are excluded from the output for that sample.

This forces the model to spread its learning across all nodes. It builds multiple redundant pathways to the right answer, which makes the patterns it learns more robust and general.

At test time, all nodes are active. Keras switches this automatically during evaluation.

Here's how to add it:

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(784,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),     # randomly disable 30% of nodes during training
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),     # 20% dropout on the second hidden layer
    tf.keras.layers.Dense(10, activation='softmax')
])
```

The number you pass to `Dropout` is the fraction of nodes to disable. `0.3` means 30% of nodes are turned off on each training pass. Values between 0.2 and 0.5 are common starting points.

If your validation accuracy is close to your training accuracy, you probably don't need dropout. If training accuracy is much higher than validation accuracy, dropout can help close that gap.

> **With your partner:** Try dropout with a few different values (0.1, 0.3, 0.5). Does higher dropout always help? What happens when you set it too high?

## Data Augmentation

Your model has only seen each digit drawn exactly once by each student. In the real world, the same digit will look different depending on how someone draws it: shifted left, slightly rotated, bigger or smaller.

**Data augmentation** generates new training samples by applying random transformations to your existing images. Augmentation shows the model the same data in more varied forms. The underlying information is the same; the presentation changes. This teaches the model to recognize digits regardless of small positional or size differences.

{% activity "data-augmentation-demo.html", "Data Augmentation", "660px" %}

Draw a digit above and click Augment. Each panel shows a different transformation of the same drawing. In a real training pipeline, your model would see all of these, effectively multiplying your dataset size.
Here's how to add augmentation to your training pipeline using Keras:

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define what kinds of augmentations to apply
datagen = ImageDataGenerator(
    rotation_range=10,       # randomly rotate up to 10 degrees
    width_shift_range=0.1,   # randomly shift left/right by up to 10% of width
    height_shift_range=0.1,  # randomly shift up/down by up to 10% of height
    zoom_range=0.1           # randomly zoom in or out by up to 10%
)

# Reshape X_train to (N, 28, 28, 1) - ImageDataGenerator expects image shape
X_train_img = X_train.reshape(-1, 28, 28, 1)

# Fit the generator to your training data
datagen.fit(X_train_img)
```

Then update your model's input to match and train using the generator:

```python
# Update the model to accept image input
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

X_test_img = X_test.reshape(-1, 28, 28, 1)

model.fit(
    datagen.flow(X_train_img, y_train, batch_size=32),
    epochs=20,
    validation_data=(X_test_img, y_test)
)
```

Augmentation is most useful when your dataset is small. With a large dataset, the variety is often already there. Use your judgment. If your baseline is already high, augmentation may not move the needle much.

> **With your partner:** Look at the augmented samples in the activity. Which transformations do you think will actually help your model? Are any of them likely to hurt?

## Larger or Deeper Network

Try more nodes or an extra hidden layer. There's no formula for the right size. It depends on your data and how much of it you have.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(784,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

More capacity helps when the model is underfitting. With too little data, a larger model will overfit instead.

## More Epochs with Early Stopping

Let the model decide when to stop training. Add an early stopping callback and it will halt automatically when validation accuracy stops improving:

```python
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=5,           # stop if val_accuracy doesn't improve for 5 epochs
    restore_best_weights=True
)

model.fit(
    X_train, y_train,
    epochs=100,           # set a high ceiling
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stop]
)
```

`restore_best_weights=True` saves the weights from the best-performing epoch, so you end up with the best version of the model even if accuracy dips slightly in later epochs.

## Batch Normalization

Batch normalization normalizes the outputs of a layer before passing them to the next one. It tends to make training faster and more stable, and can allow you to use higher learning rates.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(784,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

This is worth trying if your training loss is unstable or slow to decrease.

> **With your partner:** Pick at least two techniques from this page to try. Did they help? By how much? What would you try next?

## Submit Your Best Model

When you're happy with your results, export and resubmit:

```python
model.save("my_digit_model_v2.keras")

from google.colab import files
files.download("my_digit_model_v2.keras")
```

Go to **[http://64.23.245.76/](http://64.23.245.76/)**, submit your updated model, and check the leaderboard.

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Digit+Recognition" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
