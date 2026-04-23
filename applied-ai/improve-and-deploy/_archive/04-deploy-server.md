---
title: "Deploy: Server Side"
order: 4
---

Your model is trained. Now you'll deploy it three ways and compare the trade-offs. Start with a server.

## What "server-side inference" means

In this setup, the model lives on a server. When a user draws a digit, the browser sends the image to the server. The server runs it through the model and sends back a prediction. The user's device only receives the result.

This is how most production ML systems work. The model stays on a machine you control.

## Setup

You'll need Node.js installed. Download it from [nodejs.org](https://nodejs.org) (LTS version).

Download the starter repo from the class GitHub and open it in your terminal. Then install dependencies:

```
npm install
```

## Copy your model files

Copy `digit_model.onnx` (from your Colab notebook) into the starter repo folder.

Your folder should look like this:

```
digit-deploy/
  digit_model.onnx    ← your file goes here
  server.js
  server.html
  browser.html
  style.css
  drawing.js
  package.json
```

## Fill in the blanks

Open `server.js`. Find the two marked sections and complete them.

**Section 1: Load the model**

The server loads the ONNX model once at startup so it's ready for every request. Find the comment that says `TODO: load your model here` and replace it with:

```js
const sessionPromise = ort.InferenceSession.create(
  path.join(__dirname, 'digit_model.onnx')
)
```

**Section 2: Run inference**

Inside the `/predict` route, find the comment that says `TODO: run inference here` and replace it with:

```js
const session  = await sessionPromise
const results  = await session.run({ [session.inputNames[0]]: tensor })
const probs    = Array.from(results[session.outputNames[0]].data)
const digit    = probs.indexOf(Math.max(...probs))
```

`session.inputNames[0]` and `session.outputNames[0]` read the input and output node names directly from the model file. This means the code works with any ONNX model, not just yours.

## Start the server

```
node server.js
```

Open **http://localhost:8080** in your browser. Draw a digit and hit Predict.

> **With your partner:** Open the browser's network tab (DevTools → Network) while you click Predict. Find the POST request to `/predict`. What is the payload? What does the response look like? What happens on the server between those two moments?

<details>
<summary>Reveal answer</summary>

The payload is a JSON object with a `pixels` array of 784 floats, one per pixel of the 28×28 downsampled canvas.

The server receives those pixels, applies bbox normalization (the same centering step you used during training), wraps them in an ONNX tensor, and runs the model. The response is a JSON object with the predicted digit, the confidence score, and the full probability array for all 10 digits.

</details>

## What the server is actually doing

Open `server.js` and read through it. A few things worth understanding:

The client sends a flat array of 784 pixel values. The browser already downsamples the drawing canvas to 28×28 before sending. This keeps the request small and avoids image decoding on the server.

The `bboxNormalize` function in `server.js` is the same logic as `bbox_normalize` in your Python pipeline. The preprocessing at inference time has to match training. If the model was trained on centered, cropped digits, it needs to receive centered, cropped digits when deployed.
