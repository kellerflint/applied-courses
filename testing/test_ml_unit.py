"""
Test script for the Comparing ML Models lesson unit.

Uses sklearn's built-in breast cancer dataset (binary classification) as a
stand-in for a Kaggle dataset, so we can verify all lesson code works without
needing an external file.

Covers:
- Null/NaN handling
- Outlier detection (IQR method)
- StandardScaler
- Train/test split
- LogisticRegression
- RandomForestClassifier
- MLPClassifier (neural network)
- Confusion matrices with ConfusionMatrixDisplay
- Accuracy bar chart
- Timing predictions on 100 samples
- Model size via pickle
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend so it works without a display
import matplotlib.pyplot as plt
import pickle
import time

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

print("=" * 60)
print("STEP 1: Load and inspect data")
print("=" * 60)

# Simulate loading a Kaggle dataset as a DataFrame
raw = load_breast_cancer()
df = pd.DataFrame(raw.data, columns=raw.feature_names)
df["target"] = raw.target

print(f"Shape: {df.shape}")
print(f"Target classes: {list(raw.target_names)}")
print(f"\nFirst 3 rows:")
print(df.head(3))

# ── Null handling ────────────────────────────────────────────────────────────
print("\n--- Null check ---")
print(df.isnull().sum().to_string())
# Introduce some nulls to prove handling works
df_with_nulls = df.copy()
df_with_nulls.iloc[0, 0] = np.nan
df_with_nulls.iloc[5, 2] = np.nan
print(f"\nNulls after injection: {df_with_nulls.isnull().sum().sum()}")

# Option 1: drop rows with nulls
df_dropped = df_with_nulls.dropna()
print(f"Rows after dropna: {len(df_dropped)} (was {len(df_with_nulls)})")

# Option 2: fill with median (show this as an alternative)
df_filled = df_with_nulls.fillna(df_with_nulls.median(numeric_only=True))
print(f"Nulls after fillna: {df_filled.isnull().sum().sum()}")

# Use clean df going forward
print("\n(Using original clean dataset going forward)")

# ── Outlier detection (IQR method) ──────────────────────────────────────────
print("\n--- Outlier removal (IQR method) ---")
feature_cols = list(raw.feature_names)

def remove_outliers_iqr(dataframe, columns, factor=3.0):
    mask = pd.Series([True] * len(dataframe), index=dataframe.index)
    for col in columns:
        Q1 = dataframe[col].quantile(0.25)
        Q3 = dataframe[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask = mask & dataframe[col].between(lower, upper)
    return dataframe[mask]

df_clean = remove_outliers_iqr(df, feature_cols)
print(f"Rows before: {len(df)}, after outlier removal: {len(df_clean)}")

# ── Features and target ──────────────────────────────────────────────────────
X = df_clean[feature_cols]
y = df_clean["target"]

# ── Binarization demo (for lesson: turning continuous → classification) ──────
print("\n--- Binarization demo ---")
# Example: if target were continuous (like a score), you could threshold it
continuous_example = np.random.uniform(0, 100, 20)
threshold = 50
binary_from_continuous = (continuous_example > threshold).astype(int)
print(f"Sample continuous values: {continuous_example[:5].round(1)}")
print(f"After threshold={threshold}: {binary_from_continuous[:5]}")

# ── Train/test split ─────────────────────────────────────────────────────────
print("\n--- Train/test split ---")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# ── Standardization ──────────────────────────────────────────────────────────
print("\n--- StandardScaler ---")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # NOTE: fit only on train, transform test
print(f"Train mean (first feature, should be ~0): {X_train_scaled[:, 0].mean():.4f}")
print(f"Train std  (first feature, should be ~1): {X_train_scaled[:, 0].std():.4f}")

# ── LOGISTIC REGRESSION ──────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Logistic Regression")
print("=" * 60)

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
lr_preds = lr.predict(X_test_scaled)
lr_acc = accuracy_score(y_test, lr_preds)
print(f"Accuracy: {lr_acc:.4f}")

# ── RANDOM FOREST ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Random Forest")
print("=" * 60)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
rf_preds = rf.predict(X_test_scaled)
rf_acc = accuracy_score(y_test, rf_preds)
print(f"Accuracy: {rf_acc:.4f}")

# ── NEURAL NETWORK (MLPClassifier) ───────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Neural Network (MLPClassifier)")
print("=" * 60)

mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
mlp.fit(X_train_scaled, y_train)
mlp_preds = mlp.predict(X_test_scaled)
mlp_acc = accuracy_score(y_test, mlp_preds)
print(f"Accuracy: {mlp_acc:.4f}")
print(f"Hidden layers: {mlp.hidden_layer_sizes}")
print(f"n_layers_: {mlp.n_layers_}")
print(f"Converged in {mlp.n_iter_} iterations")

# ── CONFUSION MATRICES ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: Confusion matrices side by side")
print("=" * 60)

class_names = list(raw.target_names)
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, preds, title in zip(
    axes,
    [lr_preds, rf_preds, mlp_preds],
    ["Logistic Regression", "Random Forest", "Neural Network"]
):
    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(title)

plt.tight_layout()
plt.savefig("/Users/kellerflint/Projects/courses/testing/confusion_matrices.png", dpi=100)
plt.close()
print("Saved: confusion_matrices.png")

# ── ACCURACY BAR CHART ───────────────────────────────────────────────────────
print("\n--- Accuracy bar chart ---")

model_names = ["Logistic Regression", "Random Forest", "Neural Network"]
accuracies = [lr_acc, rf_acc, mlp_acc]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(model_names, accuracies, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylim(0.8, 1.0)
ax.set_ylabel("Accuracy")
ax.set_title("Model Accuracy Comparison")
for bar, acc in zip(bars, accuracies):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.003,
        f"{acc:.3f}",
        ha="center", va="bottom", fontsize=11
    )
plt.tight_layout()
plt.savefig("/Users/kellerflint/Projects/courses/testing/accuracy_chart.png", dpi=100)
plt.close()
print("Saved: accuracy_chart.png")

# ── TIMING ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: Prediction timing (100 samples)")
print("=" * 60)

sample_100 = X_test_scaled[:100]

REPEATS = 50  # repeat timing to get stable numbers

def time_predict(model, X, repeats=REPEATS):
    start = time.perf_counter()
    for _ in range(repeats):
        model.predict(X)
    elapsed = (time.perf_counter() - start) / repeats
    return elapsed

lr_time  = time_predict(lr,  sample_100)
rf_time  = time_predict(rf,  sample_100)
mlp_time = time_predict(mlp, sample_100)

print(f"Logistic Regression : {lr_time * 1000:.3f} ms")
print(f"Random Forest       : {rf_time * 1000:.3f} ms")
print(f"Neural Network      : {mlp_time * 1000:.3f} ms")

times_ms = [lr_time * 1000, rf_time * 1000, mlp_time * 1000]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(model_names, times_ms, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylabel("Time per prediction batch (ms)")
ax.set_title("Prediction Speed: 100 Samples")
for bar, t in zip(bars, times_ms):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.001,
        f"{t:.3f}ms",
        ha="center", va="bottom", fontsize=10
    )
plt.tight_layout()
plt.savefig("/Users/kellerflint/Projects/courses/testing/timing_chart.png", dpi=100)
plt.close()
print("Saved: timing_chart.png")

# ── MODEL SIZE ───────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: Model size via pickle")
print("=" * 60)

def model_size_bytes(model):
    return len(pickle.dumps(model))

lr_size  = model_size_bytes(lr)
rf_size  = model_size_bytes(rf)
mlp_size = model_size_bytes(mlp)

def human_size(b):
    if b < 1024:
        return f"{b} B"
    elif b < 1024 ** 2:
        return f"{b / 1024:.1f} KB"
    else:
        return f"{b / 1024 ** 2:.2f} MB"

print(f"Logistic Regression : {human_size(lr_size)}")
print(f"Random Forest       : {human_size(rf_size)}")
print(f"Neural Network      : {human_size(mlp_size)}")

sizes_kb = [lr_size / 1024, rf_size / 1024, mlp_size / 1024]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(model_names, sizes_kb, color=["#4f86c6", "#4caf8a", "#e07b54"])
ax.set_ylabel("Model size (KB)")
ax.set_title("Serialized Model Size")
for bar, s, raw_b in zip(bars, sizes_kb, [lr_size, rf_size, mlp_size]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        human_size(raw_b),
        ha="center", va="bottom", fontsize=10
    )
plt.tight_layout()
plt.savefig("/Users/kellerflint/Projects/courses/testing/size_chart.png", dpi=100)
plt.close()
print("Saved: size_chart.png")

# ── COMBINED COMPARISON FIGURE ───────────────────────────────────────────────
print("\n--- Combined comparison chart ---")

fig, axes = plt.subplots(1, 3, figsize=(16, 4))

# Accuracy
axes[0].bar(model_names, accuracies, color=["#4f86c6", "#4caf8a", "#e07b54"])
axes[0].set_ylim(0.8, 1.0)
axes[0].set_title("Accuracy")
axes[0].set_ylabel("Accuracy")
for bar, acc in zip(axes[0].patches, accuracies):
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.003,
        f"{acc:.3f}", ha="center", va="bottom", fontsize=10
    )

# Speed
axes[1].bar(model_names, times_ms, color=["#4f86c6", "#4caf8a", "#e07b54"])
axes[1].set_title("Prediction Speed (100 samples)")
axes[1].set_ylabel("Time (ms)")

# Size
axes[2].bar(model_names, sizes_kb, color=["#4f86c6", "#4caf8a", "#e07b54"])
axes[2].set_title("Model Size")
axes[2].set_ylabel("Size (KB)")

plt.tight_layout()
plt.savefig("/Users/kellerflint/Projects/courses/testing/comparison_all.png", dpi=100)
plt.close()
print("Saved: comparison_all.png")

# ── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"{'Model':<22} {'Accuracy':>10} {'Speed (ms)':>12} {'Size':>10}")
print("-" * 56)
for name, acc, t, s in zip(model_names, accuracies, times_ms, [lr_size, rf_size, mlp_size]):
    print(f"{name:<22} {acc:>10.4f} {t:>12.3f} {human_size(s):>10}")

print("\nAll checks passed.")
