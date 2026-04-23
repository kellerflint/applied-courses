---
title: "Build the Training Pipeline"
order: 2
---

Open a new Colab notebook. You'll build the training pipeline one step at a time, using AI for each piece.

## Setup

Ask your AI assistant to write the import block for this project. Tell it you need: NumPy, PIL (Pillow), matplotlib, os, scikit-learn's `train_test_split`, `scipy.ndimage`, TensorFlow/Keras, and `tf2onnx`. Ask it to also define two constants at the top: `IMG_SIZE = 28` and `BBOX_PAD = 2`.

Run the cell. If anything fails to import, show AI the error and ask it to fix it.

## Load the dataset

Ask AI to write code that loads a digit image dataset from a folder. Specify in your prompt:

- The dataset is organized as subfolders named "0" through "9", each containing PNG files
- Each image should be opened with PIL, converted to grayscale, resized to `IMG_SIZE × IMG_SIZE`, and stored as a `float32` NumPy array with values 0 to 1
- All images go into a list called `raw_images`, all labels into a list called `labels`
- Both lists should be converted to NumPy arrays at the end
- The folder path should use a variable called `DATASET_PATH` so it's easy to change

## Bbox normalization

When people draw digits, they draw them at different sizes and in different positions. When you resize the full canvas to 28×28, a small digit in a corner looks very different from a large centered digit. The model spends capacity on that positional variation rather than focusing on the shape of the digit itself.

Bbox normalization fixes this: find the bounding box of the drawn pixels, crop to that region, and resize back to 28×28. Every digit ends up centered and consistently scaled.

Ask AI to write a function called `bbox_normalize` that takes a 2D `float32` NumPy array (28×28, values 0 to 1). Tell it to:

- Find which rows and columns contain any pixel above 0.2
- Find the first and last row with content (top and bottom of the bounding box) and the first and last column (left and right)
- Add `BBOX_PAD` pixels of padding to each edge, clamped to stay within the image boundary
- Crop to that region, then resize back to `IMG_SIZE × IMG_SIZE` using PIL with `Image.LANCZOS`
- Return the result as a `float32` array normalized 0 to 1
- Return the image unchanged if it is blank (all pixels below the threshold)

Then ask it to apply the function to every image in `raw_images` and store the results in a new array called `images`.

### Verify

Ask AI to write visualization code that shows the original and normalized version of one sample per digit, side by side in a matplotlib grid. Save it to `check_bbox.png`.

Run it and look at the output. The right column should show each digit centered and scaled to fill the frame. If something looks wrong, describe the specific issue to AI and ask it to fix the function.

> **With your partner:** Look at `check_bbox.png`. Find a digit that was off-center or small in the original. Did normalization bring it in correctly? Is there anything that looks broken?

> **With your partner:** This preprocessing runs before training. But it also has to run at inference time, when a user draws a digit in the deployed app. Why? What would happen if you trained with normalized images but skipped this step when serving predictions?

## Data augmentation

With only about 1,400 images, the model will only ever see each digit drawn the way one specific person drew it. Augmentation randomly transforms each image every time the model trains on it, so the model learns to handle variation across angles, sizes, and stroke widths.

Ask AI to write a function called `augment` that takes a 28×28×1 NumPy `float32` array. Tell it to randomly apply a combination of: rotation (up to 15 degrees in either direction), translation (shift up to 12% of the image size in any direction), zoom (scale factor 0.75 to 1.25), binary dilation of the stroke (one iteration), and cutout (black out a small random rectangle). Tell it to use `scipy.ndimage` for the transforms and to guarantee that at least 2 transforms apply on every call.

Also ask it to write a `tf_augment` wrapper function that calls `augment` inside `tf.py_function` so it can be used inside a `tf.data` pipeline.

### Verify

Ask AI to write visualization code that shows the original and 5 augmented versions of one sample per digit in a grid. Save it to `check_augmentation.png`.

Run it. All 10 digits should still be clearly readable. If any look unrecognizable, ask AI to reduce the rotation range or zoom range. If the augmented versions look nearly identical to the original, ask it to increase them.

> **With your partner:** Are all digits still readable after augmentation? Augmentation only applies to the training set. The validation set uses the original images. Why does that matter for the accuracy numbers you see during training?

## Train, val, and test split

Ask AI to split the data into training, validation, and test sets. Tell it:

- Use scikit-learn's `train_test_split` with 20% held out for test, stratified by label
- Take 10% of the remaining training data as a validation set
- Reshape images to `(n, 28, 28, 1)` before splitting

Then ask it to build a `tf.data` pipeline. Tell it the training pipeline should shuffle, apply `tf_augment`, batch at size 32, and prefetch. Tell it the validation pipeline should batch only.

## Build the CNN

You've built CNNs in a previous unit. Build one for this dataset. Your input shape is `(28, 28, 1)` and you have 10 output classes.

Sketch the architecture with your partner first. You can use AI to help once you have a plan, but start from your own design. Use `BatchNormalization` and `Dropout` between conv blocks. Compile with Adam at learning rate `1e-3` and `sparse_categorical_crossentropy` loss.

> **With your partner:** Sketch your architecture before writing any code. How many conv blocks? How many filters per layer? Where does dropout go?

## Early stopping and training

Ask AI to write the training callbacks. Tell it you want:

- `EarlyStopping` monitoring `val_loss` with patience 20 and `restore_best_weights=True`
- `ReduceLROnPlateau` monitoring `val_loss`, cutting the learning rate in half with patience 8 and a minimum rate of `1e-5`

Then ask it to call `model.fit` with 200 epochs, your train and val datasets, and the callbacks. Ask it to also write code that evaluates on the test set and plots training and validation accuracy and loss curves.

> **With your partner:** What accuracy did you hit? Look at the curves. Is training accuracy still climbing while validation accuracy has leveled off? That is a sign of overfitting. What would you try to push accuracy higher?

## Export

Once you are satisfied with accuracy, export the model in two formats. You will need both for the deployment step.

First, install the export libraries in a separate cell:

```
!pip install tf2onnx onnxruntime tensorflowjs
```

Ask AI to export your Keras model to ONNX using `tf2onnx`. Tell it the input name should be `"input"`, the shape `[None, 28, 28, 1]`, dtype `float32`, and the opset should be 13. Output file: `digit_model.onnx`.

Then ask it to export to TF.js format using `tensorflowjs.converters.save_keras_model`. Output folder: `model/`.

Download `digit_model.onnx` and the `model/` folder from Colab. You will need both for the next step.
