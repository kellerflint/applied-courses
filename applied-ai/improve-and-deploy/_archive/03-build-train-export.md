---
title: "Build, Train, and Export"
order: 3
---

Data is preprocessed and augmented. Now you'll wire it into a training pipeline, build and train the model, and export it in two formats for deployment.

## Split your data

Before building the model, set up your train, validation, and test splits. The validation set is used during training to monitor for overfitting. The test set is held out entirely, giving you an honest accuracy number that reflects real-world performance.

```python
from sklearn.model_selection import train_test_split

X = images.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
y = labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

val_size = max(1, int(len(X_train) * 0.1))
X_val,   y_val   = X_train[-val_size:], y_train[-val_size:]
X_train, y_train = X_train[:-val_size], y_train[:-val_size]

print(f"Train: {len(X_train)}  Val: {len(X_val)}  Test: {len(X_test)}")
```

Then build a `tf.data` pipeline that applies augmentation on the fly during training:

```python
BATCH_SIZE = 32

train_ds = (
    tf.data.Dataset.from_tensor_slices((X_train, y_train))
    .shuffle(len(X_train), reshuffle_each_iteration=True)
    .map(tf_augment, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)
val_ds = (
    tf.data.Dataset.from_tensor_slices((X_val, y_val))
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)
```

Augmentation is only applied to the training set. The validation set uses the original images so the metrics reflect real-world performance.

## Build your CNN

You've built CNNs before. Build one now for this dataset. Your input shape is `(28, 28, 1)` and you have 10 output classes.

Refer to the convolutional networks unit if you want a reference. Use `BatchNormalization` and `Dropout` between blocks. If you're not sure where to start, describe what you want to a coding assistant and iterate from there. That's a normal way to work.

> **With your partner:** Sketch your architecture before you write the code. How many conv blocks? How many filters per layer? Where will you put dropout?

Compile it when you're ready:

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()
```

## Early stopping

Training a model means running it over your dataset repeatedly. One full pass is called an epoch. With each epoch, the model improves on the training data, but at some point it starts to overfit. The model gets better at the specific training examples and its performance on new data levels off or drops.

Early stopping monitors validation loss during training and stops when it stops improving. This lets you set a high epoch ceiling and let training find the right stopping point on its own.

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=20,
        restore_best_weights=True,
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=8,
        min_lr=1e-5,
        verbose=1
    ),
]
```

`patience=20` means training will continue for 20 more epochs after validation loss stops improving, in case it recovers. `restore_best_weights=True` rolls the model back to its best checkpoint when training ends. `ReduceLROnPlateau` cuts the learning rate in half when progress stalls, which can help squeeze out extra accuracy in the later epochs.

## Train

```python
history = model.fit(
    train_ds,
    epochs=200,
    validation_data=val_ds,
    callbacks=callbacks,
    verbose=1
)
```

## Evaluate

After training, check accuracy on the held-out test set and look at the learning curves.

```python
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {acc:.4f}")
print(f"Test loss:     {loss:.4f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history.history['accuracy'],     label='train')
ax1.plot(history.history['val_accuracy'], label='val')
ax1.set_title('Accuracy'); ax1.set_xlabel('Epoch'); ax1.legend()
ax2.plot(history.history['loss'],     label='train')
ax2.plot(history.history['val_loss'], label='val')
ax2.set_title('Loss'); ax2.set_xlabel('Epoch'); ax2.legend()
plt.tight_layout()
plt.show()
```

> **With your partner:** What accuracy did you hit? Look at the learning curves. Does the model show signs of overfitting? Look for training accuracy climbing while validation accuracy levels off or drops. What would you try to push accuracy higher?

## Export your model

Once you're happy with the results, export the model in two formats. You'll need both for the deployment step.

**ONNX** is a standard model format that works across different languages and frameworks. The Node.js server loads this file using onnxruntime, a lightweight JavaScript package.

**TF.js** is a version of your model that runs directly in a web browser using JavaScript.

First, install the export libraries. In Colab, run this as its own cell:

```
!pip install tf2onnx onnxruntime tensorflowjs
```

Then export:

```python
import tf2onnx
import tensorflowjs as tfjs
import os

# Export to ONNX for the Node.js server
input_signature = [
    tf.TensorSpec(shape=[None, 28, 28, 1], dtype=tf.float32, name="input")
]
tf2onnx.convert.from_keras(
    model,
    input_signature=input_signature,
    opset=13,
    output_path="digit_model.onnx",
)
print("Saved digit_model.onnx")

# Export to TF.js for the browser
os.makedirs("model", exist_ok=True)
tfjs.converters.save_keras_model(model, "model")
print("Saved model/")
```

Download both `digit_model.onnx` and the `model/` folder from Colab. You'll copy them into the deploy starter in the next step.
