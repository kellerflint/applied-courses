"""
End-to-end test of the Convolutional Networks lesson pipeline.
Follows all steps from 02-explore-your-data.md and 03-build-and-compare.md
for each dataset, restricted to 3 classes for speed on a local machine.

Outputs: sample images, class distribution, learning curves, confusion matrices
         → testing/cnn_test_outputs/<dataset>/

Run with: python3.11 testing/test_cnn_pipeline.py
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf

OUTPUT_DIR = "testing/cnn_test_outputs"
EPOCHS = 8
BATCH_SIZE = 32
KEEP_CLASSES = [0, 1, 2]


# ── Helpers ───────────────────────────────────────────────────────────────────

def filter_to_classes(X, y, keep):
    mask = np.isin(y, keep)
    X_f, y_f = X[mask], y[mask]
    label_map = {old: new for new, old in enumerate(sorted(keep))}
    y_f = np.array([label_map[v] for v in y_f])
    return X_f, y_f


def save_class_distribution(y, class_names, path):
    counts = np.bincount(y)
    labels = [class_names[i] for i in range(len(counts))]
    plt.figure(figsize=(8, 4))
    plt.bar(range(len(counts)), counts)
    plt.xticks(range(len(counts)), labels, rotation=45, ha='right')
    plt.ylabel("Count")
    plt.title("Samples per class")
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"  saved {path}")


def save_sample_images(X, y, class_names, title, path):
    num_classes = len(class_names)
    fig, axes = plt.subplots(num_classes, 5, figsize=(8, num_classes * 1.6))
    fig.suptitle(title, fontsize=13)
    for label in range(num_classes):
        idxs = np.where(y == label)[0][:5]
        for col in range(5):
            ax = axes[label][col]
            if col < len(idxs):
                img = X[idxs[col]]
                if img.ndim == 3:
                    img = img[:, :, 0]
                ax.imshow(img, cmap='gray_r')
            ax.axis('off')
            if col == 0:
                ax.set_ylabel(class_names[label], fontsize=9, rotation=0, labelpad=50, va='center')
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"  saved {path}")


def save_learning_curves(flat_history, cnn_history, path):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, history, label in zip(axes, [flat_history, cnn_history], ['Flat Network', 'CNN']):
        ax.plot(history.history['accuracy'],     label='Training')
        ax.plot(history.history['val_accuracy'], label='Validation')
        ax.set_title(label)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Accuracy')
        ax.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"  saved {path}")


def save_confusion_matrix(model, X_test, y_test, class_names, title, path):
    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
    num_classes = len(class_names)
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for true, pred in zip(y_test, y_pred):
        cm[true][pred] += 1
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap='Blues')
    ax.set_xticks(range(num_classes))
    ax.set_yticks(range(num_classes))
    ax.set_xticklabels(class_names, rotation=45, ha='right')
    ax.set_yticklabels(class_names)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_title(title)
    for i in range(num_classes):
        for j in range(num_classes):
            ax.text(j, i, cm[i][j], ha='center', va='center',
                    color='white' if cm[i][j] > cm.max() * 0.5 else 'black')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"  saved {path}")


def save_prediction_grid(model_flat, model_cnn, X_test, y_test, class_names, path):
    num_classes = len(class_names)
    flat_preds = np.argmax(model_flat.predict(X_test, verbose=0), axis=1)
    cnn_preds  = np.argmax(model_cnn.predict(X_test, verbose=0),  axis=1)
    fig, axes = plt.subplots(num_classes, 5, figsize=(10, num_classes * 2))
    fig.suptitle("Test predictions  (F=Flat  C=CNN)  green=correct  red=wrong", fontsize=11)
    for label in range(num_classes):
        idxs = np.where(y_test == label)[0][:5]
        for col in range(5):
            ax = axes[label][col]
            if col < len(idxs):
                idx = idxs[col]
                img = X_test[idx, :, :, 0]
                ax.imshow(img, cmap='gray_r')
                fp = class_names[flat_preds[idx]][:5]
                cp = class_names[cnn_preds[idx]][:5]
                both_right = flat_preds[idx] == label and cnn_preds[idx] == label
                color = 'green' if both_right else 'red'
                ax.set_title(f"F:{fp}\nC:{cp}", fontsize=7, color=color)
            ax.axis('off')
            if col == 0:
                ax.set_ylabel(class_names[label], fontsize=9, rotation=0, labelpad=50, va='center')
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()
    print(f"  saved {path}")


# ── Pipeline (follows lesson steps exactly) ───────────────────────────────────

def run_pipeline(dataset_name, X_train_raw, y_train_raw, X_test_raw, y_test_raw, all_class_names):
    print(f"\n{'='*60}")
    print(f"  {dataset_name}")
    print(f"{'='*60}")

    out = os.path.join(OUTPUT_DIR, dataset_name.lower().replace(" ", "_").replace("-", "_"))
    os.makedirs(out, exist_ok=True)

    # tfds images sometimes arrive as (N, H, W, 1) — squeeze to (N, H, W)
    if X_train_raw.ndim == 4:
        X_train_raw = X_train_raw.squeeze(-1)
    if X_test_raw.ndim == 4:
        X_test_raw = X_test_raw.squeeze(-1)

    # ── Restrict to 3 classes ────────────────────────────────────
    X_train, y_train = filter_to_classes(X_train_raw, y_train_raw, KEEP_CLASSES)
    X_test,  y_test  = filter_to_classes(X_test_raw,  y_test_raw,  KEEP_CLASSES)
    class_names = [all_class_names[i] for i in KEEP_CLASSES]
    NUM_CLASSES = len(class_names)

    # ── Shape and size (lesson page 02) ──────────────────────────
    print(f"  Training samples:  {X_train.shape[0]}")
    print(f"  Test samples:      {X_test.shape[0]}")
    print(f"  Image size:        {X_train.shape[1:]}")
    print(f"  Number of classes: {len(np.unique(y_train))}")
    print(f"  Pixel value range: {X_train.min()} to {X_train.max()}")

    # ── Class distribution ────────────────────────────────────────
    save_class_distribution(y_train, class_names,
                            os.path.join(out, "class_distribution.png"))

    # ── Sample images ─────────────────────────────────────────────
    save_sample_images(X_train, y_train, class_names,
                       f"5 samples per class — {dataset_name}",
                       os.path.join(out, "sample_images.png"))

    # ── Normalize (lesson page 02) ────────────────────────────────
    X_train = X_train.astype('float32') / 255.0
    X_test  = X_test.astype('float32')  / 255.0

    # ── Reshape to (N, H, W, 1) (lesson page 02) ──────────────────
    H, W = X_train.shape[1], X_train.shape[2]
    X_train = X_train.reshape(-1, H, W, 1)
    X_test  = X_test.reshape(-1, H, W, 1)
    print(f"  X_train shape: {X_train.shape}")
    print(f"  X_test shape:  {X_test.shape}")

    IMG_H, IMG_W = X_train.shape[1], X_train.shape[2]

    # ── Flat dense network (lesson page 03) ───────────────────────
    print("\n  [flat model]")
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
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        verbose=1
    )

    # ── CNN (lesson page 03) ──────────────────────────────────────
    print("\n  [CNN model]")
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
    cnn_history = cnn_model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        verbose=1
    )

    # ── Compare results (lesson page 03) ─────────────────────────
    flat_acc = flat_model.evaluate(X_test, y_test, verbose=0)[1]
    cnn_acc  = cnn_model.evaluate(X_test, y_test, verbose=0)[1]
    print(f"\n  Flat network: {flat_acc:.4f}")
    print(f"  CNN:          {cnn_acc:.4f}")

    # ── Save outputs ──────────────────────────────────────────────
    save_learning_curves(flat_history, cnn_history,
                         os.path.join(out, "learning_curves.png"))
    save_confusion_matrix(flat_model, X_test, y_test, class_names,
                          f"{dataset_name} — Flat Network",
                          os.path.join(out, "cm_flat.png"))
    save_confusion_matrix(cnn_model, X_test, y_test, class_names,
                          f"{dataset_name} — CNN",
                          os.path.join(out, "cm_cnn.png"))
    save_prediction_grid(flat_model, cnn_model, X_test, y_test, class_names,
                         os.path.join(out, "test_predictions.png"))

    return flat_acc, cnn_acc


# ── Load datasets and run ─────────────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)
results = {}

# Fashion-MNIST — loads via tf.keras.datasets (no extra package needed)
print("\n>>> Loading Fashion-MNIST")
(X_tr, y_tr), (X_te, y_te) = tf.keras.datasets.fashion_mnist.load_data()
fmnist_class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                      'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
results['Fashion-MNIST'] = run_pipeline(
    'Fashion-MNIST', X_tr, y_tr, X_te, y_te, fmnist_class_names)

# EMNIST Letters — requires tensorflow_datasets
print("\n>>> Loading EMNIST Letters")
try:
    import tensorflow_datasets as tfds

    (ds_train, ds_test), info = tfds.load(
        'emnist/letters',
        split=['train', 'test'],
        as_supervised=True,
        with_info=True
    )
    X_tr_e = np.array([x.numpy() for x, _ in ds_train])
    y_tr_e = np.array([y.numpy() for _, y in ds_train])
    X_te_e = np.array([x.numpy() for x, _ in ds_test])
    y_te_e = np.array([y.numpy() for _, y in ds_test])
    # EMNIST labels are 1-based (1-26) — shift to 0-based
    y_tr_e = y_tr_e - 1
    y_te_e = y_te_e - 1

    emnist_class_names = [chr(ord('A') + i) for i in range(26)]
    results['EMNIST-Letters'] = run_pipeline(
        'EMNIST-Letters', X_tr_e, y_tr_e, X_te_e, y_te_e, emnist_class_names)

except ImportError:
    print("  SKIP — tensorflow_datasets not installed")
    print("  Install with: pip install tensorflow-datasets")

# Kuzushiji-MNIST — requires tensorflow_datasets
print("\n>>> Loading Kuzushiji-MNIST")
try:
    import tensorflow_datasets as tfds

    ds_train_k = tfds.load('kmnist', split='train', as_supervised=True)
    ds_test_k  = tfds.load('kmnist', split='test',  as_supervised=True)
    X_tr_k = np.array([x.numpy() for x, _ in ds_train_k])
    y_tr_k = np.array([y.numpy() for _, y in ds_train_k])
    X_te_k = np.array([x.numpy() for x, _ in ds_test_k])
    y_te_k = np.array([y.numpy() for _, y in ds_test_k])

    kmnist_class_names = ['o (お)', 'ki (き)', 'su (す)', 'tsu (つ)', 'na (な)',
                          'ha (は)', 'ma (ま)', 'ya (や)', 're (れ)', 'wo (を)']
    results['Kuzushiji-MNIST'] = run_pipeline(
        'Kuzushiji-MNIST', X_tr_k, y_tr_k, X_te_k, y_te_k, kmnist_class_names)

except ImportError:
    print("  SKIP — tensorflow_datasets not installed")
    print("  Install with: pip install tensorflow-datasets")

# ── Final summary ─────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("  RESULTS SUMMARY")
print(f"{'='*60}")
for name, (flat_acc, cnn_acc) in results.items():
    diff = cnn_acc - flat_acc
    sign = '+' if diff >= 0 else ''
    print(f"  {name:<20}  flat={flat_acc:.4f}  cnn={cnn_acc:.4f}  ({sign}{diff:.4f})")
print(f"\n  Outputs: {OUTPUT_DIR}/")
