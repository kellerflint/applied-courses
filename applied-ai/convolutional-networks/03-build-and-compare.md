---
title: "Build and Compare"
order: 3
---

You'll build two models on the same dataset and compare them directly. Start with a flat dense network as the baseline, then build a CNN. The goal is to see whether the CNN architecture actually helps on your specific problem, and by how much.

## Baseline: Flat Dense Network

Build a dense network the same way you did for digits. Add a `Flatten` layer first to convert the 2D image input into a 1D vector. The architecture is up to you. Use similar sizing to what worked for digits.

```python
NUM_CLASSES = len(np.unique(y_train))
IMG_H, IMG_W = X_train.shape[1], X_train.shape[2]

flat_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(IMG_H, IMG_W, 1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

flat_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

flat_history = flat_model.fit(
    X_train, y_train,
    epochs=15,
    batch_size=32,
    validation_data=(X_test, y_test)
)
```

Note your test accuracy. You will compare it to the CNN after training both.

## Build the CNN

```python
cnn_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(IMG_H, IMG_W, 1)),

    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

cnn_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

cnn_model.summary()
```

What the new layers do:

**`Conv2D(32, (3, 3), activation='relu')`** applies 32 different 3×3 filters across the image. Each filter learns to detect a different local feature. The output has 32 channels, one per filter. `relu` clips any negative values to zero, the same as in your dense layers.

**`MaxPooling2D((2, 2))`** downsamples the feature maps by keeping only the maximum value in each 2×2 region. This cuts the spatial size in half, reduces computation, and makes the detected features more robust to small position shifts.

**The second `Conv2D(64, ...)`** block repeats the process on the feature maps from the first block. The second layer detects combinations of the features the first layer found. It sees shapes where the first layer saw edges.

**`Flatten()`** converts the final 2D feature maps into a 1D vector before the dense classification layers. This is where the spatial processing ends and the classification begins.

> **With your partner:** Run `cnn_model.summary()`. How many parameters does the CNN have compared to the flat model? Which has more? Why might having more parameters not automatically mean better results?

<details>
<summary>Reveal answer</summary>

The flat model often has more total parameters. The first Dense layer connects every pixel directly to every node. For a 28×28 image with 256 nodes, that's 784 × 256 = 200,704 weights in one layer alone.

The CNN's convolutional filters are tiny (a 3×3 filter has 9 weights) and share those weights across the whole image, so they cover the same spatial area with far fewer parameters. More parameters can lead to overfitting when there isn't enough data to train them all well.

</details>

Train the CNN for the same number of epochs as the flat model so the comparison is fair:

```python
cnn_history = cnn_model.fit(
    X_train, y_train,
    epochs=15,
    batch_size=32,
    validation_data=(X_test, y_test)
)
```

## Compare Results

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, history, label in zip(axes, [flat_history, cnn_history], ['Flat Network', 'CNN']):
    ax.plot(history.history['accuracy'],     label='Training')
    ax.plot(history.history['val_accuracy'], label='Validation')
    ax.set_title(label)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.legend()

plt.tight_layout()
plt.show()

flat_acc = flat_model.evaluate(X_test, y_test, verbose=0)[1]
cnn_acc  = cnn_model.evaluate(X_test, y_test, verbose=0)[1]
print(f"Flat network: {flat_acc:.4f}")
print(f"CNN:          {cnn_acc:.4f}")
```

> **With your partner:** How large is the gap between the two models? Does either show signs of overfitting? Does the result match what you expected based on the introduction?
