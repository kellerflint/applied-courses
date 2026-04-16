---
title: "Build Your First Network"
order: 2
---

You have your data loaded. Now you'll build a neural network in TensorFlow and train it to recognize handwritten digits.

This is your first time using TensorFlow directly. The library does a lot of the heavy lifting. Your job is to describe the network structure and tell it how to train.

## What You're Building

A neural network for this task takes in 784 numbers (one per pixel) and outputs 10 numbers (one probability per digit class). The network learns to map the first set of numbers to the second set by adjusting its weights during training.

Use the diagram below to get a feel for the structure before you write any code. Try adjusting the hidden layer sizes and watch how the architecture and the code change.

{% activity "keras-diagram.html", "Keras Network Builder", "620px" %}

The key things to notice:

- **Input layer:** always 784 nodes, one per pixel. This is fixed by your data.
- **Hidden layers:** you choose how many nodes. More nodes means more capacity to learn, but also more training time and a higher risk of memorizing the training data instead of generalizing.
- **Output layer:** always 10 nodes, one per digit class. The `softmax` activation turns the raw outputs into probabilities that add up to 1.

## Split Into Train and Test

Before training, set aside some data to test on. The test set is data you hold back from training. It's how you measure whether the model actually learned something general.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples:     {len(X_test)}")
```

`test_size=0.2` reserves 20% of your data for testing. `random_state=42` makes the split reproducible. You'll get the same split every time you run this.

## Build the Model

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(784,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.summary()
```

Breaking this down:

- `Sequential` means the layers run one after another in order. The output of each layer feeds into the next.
- `Input(shape=(784,))` tells the model each sample has 784 features. This matches your flattened 28×28 images.
- `Dense(128, activation='relu')` is a fully-connected layer with 128 nodes. Every node in this layer connects to every node in the previous layer. `relu` clips any negative outputs to 0. It is one of the simplest and most effective activation functions available.
- `Dense(64, activation='relu')` does the same thing with 64 nodes. Stacking layers lets the network learn increasingly abstract patterns.
- `Dense(10, activation='softmax')` is the output layer. 10 nodes, one per digit. `softmax` converts the raw scores into probabilities that sum to 1, so you get something like `[0.02, 0.91, 0.01, ...]` where the biggest number is the model's best guess.

`model.summary()` prints the layer sizes and total number of trainable parameters. Take a look at how many there are.

> **With your partner:** How many parameters does your model have? What does it mean for a model to have more parameters? What are those numbers actually representing?

<details>
<summary>Reveal answer</summary>

Parameters are the weights, the numbers that get adjusted during training. Each connection between nodes has one weight. More parameters means the model can learn more complex patterns, but it also needs more data to learn well and takes longer to train.

For the 784 → 128 layer alone: 784 × 128 weights + 128 bias values = **100,480 parameters** in just that one layer.

</details>

## Compile the Model

Before you can train, you need to tell TensorFlow three things: how to update the weights, how to measure error, and what to track.

```python
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

- `optimizer='adam'` is the algorithm that adjusts weights during training. Adam is a good default. It adjusts the learning rate automatically and works well on most problems.
- `loss='sparse_categorical_crossentropy'` measures how wrong the model is. This loss function is designed for classification problems where your labels are plain integers like 0, 1, 2.
- `metrics=['accuracy']` tells TensorFlow to track accuracy so you can see it during training.

## Train the Model

```python
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_data=(X_test, y_test)
)
```

- `epochs=20` means the model will go through the entire training set 20 times. Each pass adjusts the weights a little.
- `batch_size=32` means the model processes 32 samples at a time before updating weights. Smaller batches update more frequently but are noisier; larger batches are more stable but slower.
- `validation_data=(X_test, y_test)` runs the model against your test set at the end of each epoch so you can track how it performs on data it hasn't trained on. If training accuracy keeps rising but validation accuracy stalls or drops, the model is starting to overfit.

Watch the output as it trains. You should see the accuracy increase with each epoch.

## Plot Your Learning Curves

The `history` object that `model.fit()` returns contains the accuracy and loss numbers from every epoch. Plotting them is the best way to understand what happened during training.

These plots are called **learning curves**. They show you whether your model learned well, stopped too early, or started memorizing the training data.

{% activity "learning-curves.html", "Learning Curves", "500px" %}

Try all three buttons in the activity above. The pattern to watch for in your own training:

- **Underfitting:** both lines are still climbing. Train longer or use a bigger network.
- **Good fit:** both lines converge close together. This is what you want.
- **Overfitting:** training accuracy keeps rising but validation accuracy plateaus or drops. The gap between the two lines is the signal.

Run this to plot your own training history:

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'],     label='Training')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'],     label='Training')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()
```

Look at both plots. Which pattern does your training match? If you see overfitting, that's not a failure — it's information. You'll fix it on the next page.

> **With your partner:** Look at your learning curves. Where does validation accuracy stop improving? Does training accuracy keep going after that? What does that tell you about how many epochs you actually need?

## Evaluate on the Test Set

```python
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\nTest accuracy: {test_acc:.4f}")
```

This runs the model on the held-out test data and reports how often it got the right answer. This is the honest performance number. Training accuracy is usually higher because the model has been optimized directly on that data.

> **With your partner:** Is your test accuracy higher or lower than your training accuracy? Why might they differ?

## Look at Some Predictions

Run this to see what the model actually predicts on a few test samples:

```python
import matplotlib.pyplot as plt

predictions = model.predict(X_test[:10])
predicted_labels = predictions.argmax(axis=1)

fig, axes = plt.subplots(2, 5, figsize=(10, 4))
for i, ax in enumerate(axes.flat):
    ax.imshow(X_test[i].reshape(28, 28), cmap="gray_r")
    correct = predicted_labels[i] == y_test[i]
    color = "green" if correct else "red"
    ax.set_title(f"pred: {predicted_labels[i]}\ntrue: {y_test[i]}", color=color, fontsize=9)
    ax.axis("off")

plt.tight_layout()
plt.show()
```

Green title means the model got it right. Red means it got it wrong.

`predictions.argmax(axis=1)` takes the output probabilities for each sample and picks the index with the highest value. That index is the predicted digit class.

## Export and Submit

Save your model and upload it to the leaderboard:

```python
model.save("my_digit_model.keras")

from google.colab import files
files.download("my_digit_model.keras")
```

Then go to **[http://64.23.245.76/](http://64.23.245.76/)**, click the **Submit Model** tab, enter your name, and upload the `.keras` file. The site will score your model and add it to the leaderboard.

> **With your partner:** Before you look at the leaderboard, predict: do you think your model will get above 50%? Above 80%? What factors do you think will most affect the score?
