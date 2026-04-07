---
title: "Build Your App"
order: 2
---

You have a trained model hosted at a URL. Now you're going to load it into a web page, connect it to your webcam, and write JavaScript that reacts to the model's predictions in real time.

This is the "integrate" step of the AI workflow. The model is the brain, and your code decides what to do with its output. This is the same pattern you'd use to add AI to any web application.

## The Starter Code

Create a new file called `index.html` and paste in this starter code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teachable Machine App</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 600px;
            margin: 2rem auto;
            padding: 0 1rem;
            text-align: center;
        }
        #webcam-container canvas {
            display: none;
            border-radius: 8px;
        }
        #webcam-container.active canvas {
            display: block;
        }
        #label-container div {
            font-size: 1.1rem;
            padding: 0.25rem 0;
        }
        button {
            padding: 0.6rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            border-radius: 6px;
            border: none;
            color: white;
            background: #2563eb;
            margin: 1rem 0;
        }
        button.stop { background: #dc2626; }
        button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <h1>My Teachable Machine App</h1>

    <button id="toggleButton" onclick="toggleCamera()">Start Camera</button>

    <div id="webcam-container"></div>
    <div id="label-container"></div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
    <script>
        // REPLACE THIS with your model URL from Teachable Machine:
        const URL = "https://teachablemachine.withgoogle.com/models/YOUR_MODEL_ID/";

        let model, webcam, labelContainer, maxPredictions;
        let isRunning = false;

        async function init() {
            model = await tmImage.load(URL + "model.json", URL + "metadata.json");
            maxPredictions = model.getTotalClasses();

            webcam = new tmImage.Webcam(300, 300, true);
            await webcam.setup();
            await webcam.play();

            const container = document.getElementById("webcam-container");
            container.innerHTML = "";
            container.appendChild(webcam.canvas);
            container.classList.add("active");

            labelContainer = document.getElementById("label-container");
            labelContainer.innerHTML = "";
            for (let i = 0; i < maxPredictions; i++) {
                labelContainer.appendChild(document.createElement("div"));
            }

            isRunning = true;
            window.requestAnimationFrame(loop);
        }

        async function loop() {
            if (!isRunning) return;
            webcam.update();
            await predict();
            window.requestAnimationFrame(loop);
        }

        async function predict() {
            const prediction = await model.predict(webcam.canvas);
            for (let i = 0; i < maxPredictions; i++) {
                const classPrediction =
                    prediction[i].className + ": " + prediction[i].probability.toFixed(2);
                labelContainer.childNodes[i].innerHTML = classPrediction;
            }
        }

        async function toggleCamera() {
            const button = document.getElementById("toggleButton");
            if (!isRunning) {
                await init();
                button.textContent = "Stop Camera";
                button.classList.add("stop");
            } else {
                isRunning = false;
                webcam.stop();
                document.getElementById("webcam-container").classList.remove("active");
                button.textContent = "Start Camera";
                button.classList.remove("stop");
            }
        }
    </script>
</body>
</html>
```

Let's walk through what this code does before you change anything.

The page loads two libraries: **TensorFlow.js** (the engine that runs neural networks in the browser) and the **Teachable Machine image library** (which knows how to load and use Teachable Machine models specifically).

When you click **Start Camera**, the `init()` function runs. It loads your model from the URL, starts the webcam, and begins a loop. Every frame, `loop()` calls `predict()`, which feeds the current webcam image to the model and displays the results.

The `predict()` function is where you'll spend most of your time. Right now it displays the raw predictions. You're going to extend it to make the page react based on what the model sees.

## Step 1: Plug In Your Model

Find this line near the top of the `<script>`:

```js
const URL = "https://teachablemachine.withgoogle.com/models/YOUR_MODEL_ID/";
```

Replace `YOUR_MODEL_ID` with the URL you copied from Teachable Machine in the previous step. Make sure the URL ends with a `/`.

## Step 2: Open It

Open `index.html` in your browser. Some browsers require a local server for webcam access to work. If opening the file directly gives you errors, run this in your terminal from the folder where your file is:

```bash
python -m http.server 8000
```

Then go to `http://localhost:8000` in your browser. Click **Start Camera** and allow webcam access.

You should see your webcam feed with live prediction labels updating below it. If you see `NaN` or errors, double-check that your model URL is correct and ends with `/`.

> **With your partner:** Verify it's working for both of you. Does the model perform the same on your partner's face/hands as yours? If it doesn't, think about why. What was in your training data?

## Step 3: Find the Top Prediction

To make your app react to the model, you need to know which class has the highest confidence. Replace your `predict()` function with this version:

```js
async function predict() {
    const prediction = await model.predict(webcam.canvas);

    // Find the class with the highest probability
    let topClass = prediction[0];
    for (let i = 1; i < prediction.length; i++) {
        if (prediction[i].probability > topClass.probability) {
            topClass = prediction[i];
        }
    }

    // topClass.className is the winning label
    // topClass.probability is how confident the model is
    console.log(topClass.className, topClass.probability);

    // Update the display
    for (let i = 0; i < maxPredictions; i++) {
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
    }
}
```

Open the browser console (F12, then Console tab) and you'll see the top class and confidence logging every frame. This is useful for debugging as you build out your app.


## Understanding the Prediction Array

Every frame, the model produces an array of predictions. Before you start writing code that uses these predictions, explore the interactive demo below. It shows what the prediction array looks like in different situations and traces through what your code would do with it.

{% activity "prediction-explorer.html", "Prediction Explorer", "480px" %}

## Step 4: Make It Do Something

Now you'll extend the `predict()` function to make your page respond to what the model sees.

The examples below use a **confidence threshold**, a check like `topClass.probability > 0.8`. Before writing any of this code, try the demo to see why that matters.

{% activity "confidence-threshold.html", "Confidence Threshold Explorer", "520px" %}

Switch between scenarios and watch what happens to the two output panels. Without a threshold, your app acts on the top predicted class even when the model is barely more confident in it than the others. The threshold means you only act when the model is actually sure.

### Change the background color

```js
if (topClass.className === "Thumbs Up" && topClass.probability > 0.8) {
    document.body.style.backgroundColor = "#4ade80"; // green
} else if (topClass.className === "Thumbs Down" && topClass.probability > 0.8) {
    document.body.style.backgroundColor = "#f87171"; // red
} else {
    document.body.style.backgroundColor = "white";
}
```

### Display a message

Add a `<div id="message"></div>` to your HTML body, then:

```js
const messageEl = document.getElementById("message");
if (topClass.className === "Wave" && topClass.probability > 0.85) {
    messageEl.textContent = "Hello!";
} else {
    messageEl.textContent = "";
}
```

### Move an element on screen

Add a styled `<div id="box">` to your HTML, then:

```js
const box = document.getElementById("box");
if (topClass.className === "Left" && topClass.probability > 0.7) {
    box.style.transform = "translateX(-100px)";
} else if (topClass.className === "Right" && topClass.probability > 0.7) {
    box.style.transform = "translateX(100px)";
} else {
    box.style.transform = "translateX(0)";
}
```

These are starting points. Combine them, add CSS transitions, build a game. It's your app.

> **With your partner:** Decide what you want your app to do. You have the rest of the session to build it out. Here are some ideas if you need a starting point:
> - A gesture-controlled character that moves left/right based on which hand you raise
> - A "Simon Says" game where the model checks if you're doing the right pose
> - A mood display that changes color and text based on facial expression
> - A detector that plays a sound or shows an image when it recognizes a specific object
>
> You can finish this in class or take it home. Either way, be ready to show it off at the start of next class.

