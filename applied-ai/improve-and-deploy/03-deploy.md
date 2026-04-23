---
title: "Deploy"
order: 3
---

You have a trained model in two formats. Now you will serve it two ways: from a Node.js server and directly in the browser.

## Setup

You will need Node.js installed. Download it from [nodejs.org](https://nodejs.org) (LTS version).

Download or clone the deploy starter from [github.com/kellerflint/digit-starter](https://github.com/kellerflint/digit-starter). Open the folder in your terminal and run:

```
npm install
```

Copy your model files into the folder:

```
digit-deploy/
  digit_model.onnx        ← from Colab
  model/                  ← from Colab
    model.json
    group1-shard1of1.bin
  server.js
  browser.html
  ...
```

## Server-side inference

Open `server.js`. There are two TODO sections to fill in.

**Load the model.** Find the comment that says `TODO: load your model here`. Ask your AI assistant how to create an onnxruntime `InferenceSession` from a local file path in Node.js. Give it the variable name `sessionPromise` and tell it the model file is `digit_model.onnx` in the same folder.

**Run inference.** Find the comment that says `TODO: run inference here`. Ask AI how to run inference on an onnxruntime session in Node.js. Tell it:

- The session is available as `await sessionPromise`
- The input tensor (a `Float32Array`) is already prepared and stored as `tensor`
- You want the output probabilities as a regular JavaScript array
- Store the predicted digit index in a variable called `digit` and the probabilities in `probs`

Start the server:

```
node server.js
```

Open **http://localhost:8080**, draw a digit, and click Predict.

> **With your partner:** Open the browser's network tab (DevTools → Network) while you click Predict. Find the POST request to `/predict`. What is in the payload? What does the response look like? What is the server doing between those two moments?

## Browser-side inference

Open `browser.html`. Find the `TODO` comment and ask AI how to run a prediction using a loaded TF.js model in JavaScript. Tell it:

- The model is already loaded and stored as `model`
- The input tensor is stored as `t` with shape `[28, 28, 1]`
- You need the output as a regular JavaScript array of probabilities
- Store the predicted digit index in `digit` and the probabilities in `probs`
- Dispose both tensors after use

Open **http://localhost:8080/browser**, draw a digit, and click Predict.

Open the network tab again. Draw another digit and predict. Inference happens entirely in JavaScript, so the prediction produces no network activity.

> **With your partner:** Compare the two pages. Both predict the same digit using the same model weights. What is different about how they work? When would you choose one approach over the other?

## Submit

When you are done, share your notebook:

1. Click **Share** in the top right of Colab
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**
3. Copy the link

**Both partners submit individually on Canvas** with the shared notebook link.

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Improve+and+Deploy" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
