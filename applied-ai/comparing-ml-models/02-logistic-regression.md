---
title: "Logistic Regression"
order: 2
---

You've done this before. This page is a quick reminder of the steps, with a bit of context about why logistic regression is a useful baseline to compare against.

## Why Start Here

Logistic regression is the simplest classification model you can train. It learns a linear boundary between classes. That makes it fast to train, fast to run, and tiny to store. It's also easy to interpret: each feature gets a coefficient that tells you how much it pushes the prediction toward one class or another.

Starting with logistic regression gives you a baseline. If a more complex model can't beat it, that's a signal worth paying attention to.

## Train the Model

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

lr_preds = lr.predict(X_test_scaled)
lr_acc = accuracy_score(y_test, lr_preds)

print(f"Logistic Regression Accuracy: {lr_acc:.4f}")
```

`max_iter=1000` gives the optimizer more steps to converge. The default of 100 can sometimes cause a warning on larger datasets, so 1000 is a safer default.

## Save Your Results

You'll use these later when comparing all three models. Keep a running list in your notebook:

```python
# You'll add to this as you build each model
results = {
    "Logistic Regression": {
        "accuracy": lr_acc,
        "predictions": lr_preds
    }
}
```

> **With your partner:** Look at the accuracy. What does that number actually mean? If your accuracy is 0.92, how many of your test samples did the model get wrong?

That's it for logistic regression. Move on to the next model.
