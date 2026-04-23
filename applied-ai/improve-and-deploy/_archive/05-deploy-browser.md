---
title: "Deploy: Browser Side"
order: 5
---

Now deploy the same model a different way. This time the model runs entirely inside the browser.

## What "client-side inference" means

TensorFlow.js (TF.js) is a version of TensorFlow that runs in JavaScript. You can load a model into a browser tab and run predictions locally on the user's device.

The server still exists here, but only to serve the HTML and model files. Once those are loaded, inference happens entirely in the browser on the user's device.

## Your model is already converted

When you ran the export at the end of your training notebook, it saved a `model/` folder alongside `digit_model.onnx`. That folder contains the TF.js version of your model.

Copy the `model/` folder into your starter repo folder:

```
digit-deploy/
  digit_model.onnx
  model/               ← copy this from Colab
    model.json
    group1-shard1of1.bin
  server.js
  ...
```

## Fill in the blank

Open `browser.html`. Find the comment that says `TODO: run inference here` and replace it with:

```js
const out   = model.predict(t.expandDims(0))
const probs = Array.from(out.dataSync())
const digit = probs.indexOf(Math.max(...probs))
t.dispose(); out.dispose()
```

`expandDims(0)` adds the batch dimension the model expects: shape `[28, 28, 1]` becomes `[1, 28, 28, 1]`. After predicting, `dispose()` frees the tensors from GPU memory. TF.js does not garbage collect tensors automatically.

## Test it

Start the server if it's not already running:

```
node server.js
```

Open **http://localhost:8080/browser**. Draw a digit and hit Predict.

Open the network tab in DevTools. Draw another digit and predict again. Notice that no network request is made. The prediction happens entirely in the browser.

> **With your partner:** Compare the two pages side by side. Both predict the same digits using the same model. What's different about how they work? When the browser page first loads, what is it actually downloading?

<details>
<summary>Reveal answer</summary>

On the server page, every prediction makes a network request to `/predict`. The model runs on the server and sends back the result.

On the browser page, the model is downloaded once when the page first loads (that's the `model.json` and `.bin` files). After that, every prediction runs locally in JavaScript with no network calls.

</details>
