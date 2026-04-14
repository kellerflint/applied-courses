---
title: "Random Forest"
order: 3
---

Same deal as the last page. You've trained random forests before. Train it, evaluate it, save the results, and move on.

## A Quick Refresher

A random forest trains a large number of decision trees, each on a randomly sampled subset of the training data and features. At prediction time, every tree votes, and the most popular class wins. The randomness is what makes it work: because each tree sees slightly different data, the trees make different errors, and averaging them out produces a more robust prediction than any single tree could.

The tradeoff is size and speed. Each tree gets stored separately, which makes the model much larger than logistic regression. And at prediction time, the model has to run every tree before it can give you an answer.

## Train the Model

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

rf_preds = rf.predict(X_test_scaled)
rf_acc = accuracy_score(y_test, rf_preds)

print(f"Random Forest Accuracy: {rf_acc:.4f}")
```

`n_estimators=100` means 100 trees. This is the standard default. If training is slow or you want a smaller model, you can reduce it. Halving to 50 trees typically cuts the model size and inference time roughly in half and may not impact accuracy. Try out a few other values, see if you can get the same results with a smaller model.

## Add to Your Results

```python
results["Random Forest"] = {
    "accuracy": rf_acc,
    "predictions": rf_preds
}
```

> **With your partner:** How does the random forest accuracy compare to logistic regression? Is a more complex model always more accurate? What might explain cases where it isn't?

On to the neural network.
