---
title: "Train a Vision Model"
order: 1
---

Today you're going to train an image classification model and plug it into a web app you build yourself. The model will use your webcam to recognize gestures, objects, or poses in real time, and your app will react to what it sees.

This matters because it's the same basic workflow behind most applied AI: collect data, train a model, and integrate it into software. We're starting here because [Teachable Machine](https://teachablemachine.withgoogle.com/) lets you do the whole loop in about an hour, so you can see how all the pieces fit together before we dig into each one individually later in the course.

Find a partner. You'll pair program on one shared app (so only one of you needs to open Teachable Machine and train the model).

## What is Teachable Machine?

[Teachable Machine](https://teachablemachine.withgoogle.com/) is a browser-based tool from Google for training simple image, sound, and pose classifiers. You show it examples of different categories (like "thumbs up" vs. "thumbs down"), and it learns to tell them apart.

It's able to do this with a small number of examples because of a technique called **transfer learning**. Google already trained a large neural network (called MobileNet) on millions of images. That network learned to recognize general visual features like edges, shapes, and textures. When you train a Teachable Machine model, you're reusing all of that existing knowledge and training a small layer on top that maps those features to your specific categories. This is why you can train a useful image classifier with around 50 examples per category: the hard part of understanding what images "look like" was already done. You'll dig deeper into transfer learning later in the course. If you're curious about the details now, [this article](https://www.geeksforgeeks.org/machine-learning/what-is-the-difference-between-fine-tuning-and-transfer-learning/) is a good overview.

## Step 1: Create a New Image Project

1. Go to [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com/)
2. Click **Get Started**
3. Choose **Image Project**, then **Standard image model**

You'll see a workspace with two default classes. You can rename them and add more.

## Step 2: Define Your Classes

Come up with 2-4 classes you want your model to recognize. Here are some ideas:

- **Thumbs up / Thumbs down / Open hand** (gesture recognition)
- **Face / Specific object on desk** (presence detection)
- **Holding phone / Not holding phone** (activity detection)
- **Two different people** (person identification)

> **With your partner:** Decide what classes you're going to train. Pick something you can easily show on camera, because you'll need to record 30+ examples of each one in a few minutes.

Rename the default classes to match what you picked. Click **Add a Class** if you need more than two.

**Always include a "background" or "nothing" class.** This class should be whatever the camera sees when nobody is doing anything interesting. The model has to assign every frame to *some* class, so if you leave this out, it will label your empty room as "thumbs up" with 60% confidence. The background class gives the model a way to say "nothing is happening right now."

## Step 3: Record Training Samples

For each class:

1. Click **Webcam** on that class
2. Hold the **Record** button while demonstrating the pose, gesture, or object
3. Move around while recording. Lean, shift angles, use both hands if relevant. This variety helps the model learn the gesture itself rather than memorizing one specific position.
4. Aim for **40-80 samples per class.** This gives the model enough variety to generalize. Going above 100 has diminishing returns for a model this small.

### Tips for good training data

- **Both partners should record samples (for the same model).** If only one person records, the model may learn to recognize that person's appearance rather than the gesture. Having two different people in the training data forces it to focus on what actually matters.
- **Change your background between recordings** for the same reason. If every "thumbs up" sample has the same bookshelf behind you, the model might learn "bookshelf = thumbs up."
- **Keep your classes visually distinct.** If two gestures look nearly identical on camera, the model has very little to work with to tell them apart.

> **With your partner:** Take turns recording samples. Have one person record while the other watches the sample count and checks that the images look reasonable.

## Step 4: Train the Model

Click **Train Model**. This usually takes 20-60 seconds.

Once it finishes, the **Preview** panel on the right will activate. You'll see your webcam feed with live confidence bars showing how the model is classifying each frame.

> **With your partner:** Test the model together. Try to find its limits. What happens when you partially do a gesture? What about when someone the model hasn't seen before tries it? What about different lighting? Write down one thing that works well and one thing that fails. You'll come back to this later.

## Step 5: Export the Model

1. Click **Export Model**
2. Select the **TensorFlow.js** tab
3. Click **Upload my model**
4. Copy the URL it gives you. It will look something like:
   `https://teachablemachine.withgoogle.com/models/abc123/`

**Save this URL.** You'll use it on the next page to load your model into your app.

When you upload the model, Google hosts it at that URL as a set of files that any web page can load using TensorFlow.js. This is how your app will access the model you just trained.
