---
title: "Train a Vision Model"
order: 1
---

In this unit you'll train your own image classification model using your webcam. No coding required. The goal is to experience the full loop firsthand: collect data, train a model, and see how it performs on things it hasn't seen before.

## What is Teachable Machine?

[Teachable Machine](https://teachablemachine.withgoogle.com/) is a browser-based tool from Google for training image, sound, and pose classifiers. You show it examples of different categories and it learns to tell them apart.

It works with a small number of examples because of a technique called **transfer learning**. Google already trained a large neural network on millions of images. That network learned to recognize general visual features like edges, shapes, and textures. When you train a Teachable Machine model, you're reusing all of that existing knowledge and training a small layer on top that maps those general features to your specific categories. This is why 30-50 examples per class is enough. The hard work of understanding what images look like was already done.

## Step 1: Create a New Project

1. Go to [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com/)
2. Click **Get Started**
3. Choose **Image Project**, then **Standard image model**

You'll see a workspace with two default classes. You can rename them and add more.

## Step 2: Define Your Classes

Come up with 2-3 categories you want the model to recognize. Pick something you can demonstrate on camera right now. A few ideas:

- **Thumbs up / Thumbs down / Open hand**
- **Holding an object / Not holding it**
- **Two different people** (you and a colleague, if someone's nearby)

Rename the default classes to match your choices.

**Always include a "background" class.** Fill it with webcam footage of whatever the camera sees when nothing interesting is happening. The model has to assign every frame to some class. Without a background class, it will confidently label your empty desk as "thumbs up." The background class gives the model a way to say nothing is happening right now.

## Step 3: Record Training Samples

For each class:

1. Click **Webcam** on that class
2. Hold the **Record** button while demonstrating the gesture or object
3. Move around while recording. Change angles, shift position, try both hands if relevant. This variety helps the model learn the gesture itself rather than memorizing one specific pose.
4. Aim for **40-60 samples per class.**

A few things that matter for getting good training data:

- **Change your background between recordings.** If every "thumbs up" sample has the same bookshelf behind you, the model might learn "bookshelf = thumbs up" instead of learning the gesture.
- **Keep your classes visually distinct.** If two gestures look nearly identical on camera, the model doesn't have enough signal to tell them apart.

## Step 4: Train

Click **Train Model**. This takes 20-60 seconds.

Once it finishes, the **Preview** panel on the right activates. You'll see your webcam feed with live confidence bars showing how the model is classifying each frame.

## Step 5: Test It

Spend five minutes actively trying to break the model. This is not a failure condition. This is how you learn what the model actually learned.

Try these:

- What happens when you partially do a gesture?
- What happens in different lighting?
- What happens when you change what's in the background?
- If a colleague is nearby, what happens when they try it?

> **Reflect:** Write down one thing the model handles well and one place it fails. Then think about why each result happened. What was in your training data that might explain it?

Hold onto those observations. They're what the next page is about.
