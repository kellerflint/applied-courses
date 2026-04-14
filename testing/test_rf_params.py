"""
Quick test to find reasonable RandomForest params for the lesson.
Trying different max_depth and n_estimators combos to see
size/speed/accuracy tradeoffs.
"""

import pickle, time
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

raw = load_breast_cancer()
X, y = raw.data, raw.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)
sample_100 = X_test_s[:100]

def human_size(b):
    if b < 1024: return f"{b} B"
    elif b < 1024**2: return f"{b/1024:.1f} KB"
    else: return f"{b/1024**2:.2f} MB"

def time_predict(model, X, repeats=50):
    start = time.perf_counter()
    for _ in range(repeats):
        model.predict(X)
    return (time.perf_counter() - start) / repeats * 1000

configs = [
    dict(n_estimators=100, max_depth=None),   # current default (overkill)
    dict(n_estimators=100, max_depth=10),
    dict(n_estimators=100, max_depth=8),
    dict(n_estimators=100, max_depth=5),
    dict(n_estimators=50,  max_depth=10),
    dict(n_estimators=50,  max_depth=8),
    dict(n_estimators=20,  max_depth=10),
]

print(f"{'Config':<35} {'Accuracy':>9} {'Size':>10} {'Speed (ms)':>12}")
print("-" * 70)

for cfg in configs:
    rf = RandomForestClassifier(**cfg, random_state=42)
    rf.fit(X_train_s, y_train)
    acc  = accuracy_score(y_test, rf.predict(X_test_s))
    size = len(pickle.dumps(rf))
    spd  = time_predict(rf, sample_100)
    label = f"n={cfg['n_estimators']}, max_depth={cfg['max_depth']}"
    print(f"{label:<35} {acc:>9.4f} {human_size(size):>10} {spd:>12.3f}")
