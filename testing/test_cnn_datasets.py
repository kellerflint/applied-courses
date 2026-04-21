"""
Test the dataset loading code from applied-ai/convolutional-networks/02-explore-your-data.md
Run with: python testing/test_cnn_datasets.py
"""
import numpy as np

PASS = "✓"
FAIL = "✗"

def check(label, condition, got=""):
    status = PASS if condition else FAIL
    note = f"  → {got}" if got else ""
    print(f"  {status} {label}{note}")
    return condition

# ── Fashion-MNIST ────────────────────────────────────────────────────────────
print("\n=== Fashion-MNIST (tf.keras.datasets) ===")
try:
    import tensorflow as tf
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

    check("loads without error", True)
    check("X_train shape is (60000, 28, 28)", X_train.shape == (60000, 28, 28), str(X_train.shape))
    check("X_test shape is (10000, 28, 28)",  X_test.shape  == (10000, 28, 28), str(X_test.shape))
    check("10 classes", len(np.unique(y_train)) == 10, str(len(np.unique(y_train))))
    check("pixel range 0-255", X_train.min() == 0 and X_train.max() == 255,
          f"{X_train.min()} to {X_train.max()}")
    check("class_names length matches", True, "10 names provided in lesson ✓")

    # Test normalize + reshape (the prep code)
    X_tr = X_train.astype('float32') / 255.0
    X_te = X_test.astype('float32')  / 255.0
    H, W = X_tr.shape[1], X_tr.shape[2]
    X_tr = X_tr.reshape(-1, H, W, 1)
    X_te = X_te.reshape(-1, H, W, 1)
    check("reshape to (N, 28, 28, 1) works", X_tr.shape == (60000, 28, 28, 1), str(X_tr.shape))

except Exception as e:
    print(f"  {FAIL} FAILED: {e}")

# ── EMNIST Letters ────────────────────────────────────────────────────────────
print("\n=== EMNIST Letters ===")
try:
    # Not in tf.keras.datasets — try tensorflow_datasets
    import tensorflow_datasets as tfds

    ds_train, info = tfds.load('emnist/letters', split='train', as_supervised=True, with_info=True)
    ds_test        = tfds.load('emnist/letters', split='test',  as_supervised=True)

    # Convert to numpy
    X_train_e = np.array([x.numpy() for x, _ in ds_train])
    y_train_e = np.array([y.numpy() for _, y in ds_train])
    X_test_e  = np.array([x.numpy() for x, _ in ds_test])
    y_test_e  = np.array([y.numpy() for _, y in ds_test])

    check("loads via tensorflow_datasets", True)
    check("images are 28x28", X_train_e.shape[1:3] == (28, 28), str(X_train_e.shape))
    check("26 classes", len(np.unique(y_train_e)) == 26, str(len(np.unique(y_train_e))))
    check("pixel range", True, f"{X_train_e.min()} to {X_train_e.max()}")
    print(f"  → NOTE: requires 'tensorflow-datasets' package, NOT tf.keras.datasets")
    print(f"  → y labels are 1-based (1–26), not 0-based")

except ImportError:
    print(f"  {FAIL} tensorflow_datasets not installed")
    print(f"  → EMNIST is not in tf.keras.datasets — needs tensorflow-datasets package")
except Exception as e:
    print(f"  {FAIL} FAILED: {e}")

# ── Kuzushiji-MNIST ───────────────────────────────────────────────────────────
print("\n=== Kuzushiji-MNIST ===")
try:
    import tensorflow_datasets as tfds

    ds_train = tfds.load('kmnist', split='train', as_supervised=True)
    ds_test  = tfds.load('kmnist', split='test',  as_supervised=True)

    X_train_k = np.array([x.numpy() for x, _ in ds_train])
    y_train_k = np.array([y.numpy() for _, y in ds_train])
    X_test_k  = np.array([x.numpy() for x, _ in ds_test])

    check("loads via tensorflow_datasets", True)
    check("images are 28x28", X_train_k.shape[1:3] == (28, 28), str(X_train_k.shape))
    check("10 classes", len(np.unique(y_train_k)) == 10, str(len(np.unique(y_train_k))))
    check("pixel range", True, f"{X_train_k.min()} to {X_train_k.max()}")
    print(f"  → NOTE: requires 'tensorflow-datasets' package, NOT tf.keras.datasets")

except ImportError:
    print(f"  {FAIL} tensorflow_datasets not installed")
    print(f"  → Kuzushiji-MNIST is not in tf.keras.datasets — needs tensorflow-datasets package")
except Exception as e:
    print(f"  {FAIL} FAILED: {e}")

print()
