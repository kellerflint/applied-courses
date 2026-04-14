---
title: "Neural Network"
order: 4
---

The first two models you trained are ones you've seen before. This one is new. Before you write any code, you need a working mental model of what a neural network actually is.

## What Is a Neural Network?

A neural network is a model made of layers of simple units called **nodes** (also called neurons). Each node takes in some numbers, multiplies each one by a weight, adds them up, and passes the result through a function that squashes it into a useful range. Then that output feeds into the next layer of nodes, and so on.

The network has three kinds of layers:

- **Input layer:** one node for each feature in your dataset. If your data has 10 feature columns, you have 10 input nodes.
- **Hidden layers:** one or more layers of nodes in between. These are where the model learns patterns. More nodes and more layers means more capacity to learn complex patterns, at the cost of more training time and risk of overfitting.
- **Output layer:** one node per class. Each output node produces a probability that the input belongs to that class.

During training, the network adjusts all its weights to make better predictions. It does this by measuring how wrong it is, tracing that error backwards through the layers (a process called **backpropagation**), and nudging each weight slightly in the direction that reduces the error. Repeat this thousands of times across the training data and the weights converge on values that actually work.

The diagram below shows what this looks like for a small network.

{% activity "mlp-diagram.html", "Neural Network Architecture", "500px" %}

## Training a Neural Network with scikit-learn

scikit-learn includes a neural network classifier called `MLPClassifier` (MLP stands for Multi-Layer Perceptron, which is the technical name for this type of network). It handles all the weight updates and backpropagation for you.

```python
from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
mlp.fit(X_train_scaled, y_train)

mlp_preds = mlp.predict(X_test_scaled)
mlp_acc = accuracy_score(y_test, mlp_preds)

print(f"Neural Network Accuracy: {mlp_acc:.4f}")
print(f"Converged in {mlp.n_iter_} iterations")
```

`hidden_layer_sizes=(64, 32)` creates two hidden layers: the first with 64 nodes and the second with 32. The input layer size is determined automatically from your data, and the output layer size is determined automatically from the number of classes.

`max_iter=500` sets the maximum number of training passes. If you see a convergence warning, you can increase this.

### If training is slow

On a large dataset, the MLP can take a while. Try reducing the hidden layer sizes:

```python
mlp = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=300, random_state=42)
```

## Add to Your Results

```python
results["Neural Network"] = {
    "accuracy": mlp_acc,
    "predictions": mlp_preds
}
```

> **With your partner:** You've now trained three models on the same data. Before looking at any detailed comparison, just from the accuracy numbers: which model surprised you? Did the neural network win?

On small tabular datasets like the one you're working with, logistic regression and random forest often match or outperform neural networks. Neural networks have a lot of parameters to tune and need more data to generalize well.

That said, on image, audio, and text data, neural networks are in a different league. The architecture you just trained is about as basic as they get. The same fundamental structure, scaled up massively and trained on millions of examples, is what drives the AI tools you use every day.

On to the comparison.
