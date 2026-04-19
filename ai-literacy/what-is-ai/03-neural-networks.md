---
title: "Neural Networks"
order: 3
---

**Neural Networks** are a specific machine learning technique loosely inspired by how the brain processes information. They use layers of connected nodes called **neurons**, and each connection between neurons has a **weight**. Training a neural network means adjusting all those weights until the network produces the right outputs for the inputs it's given.

Neural networks are what make modern image recognition, speech recognition, and text generation work at scale.

## The Structure

The diagram below shows what a neural network looks like. Adjust the sliders to see how the architecture changes as you add or remove nodes and layers.

{% activity "mlp-diagram.html", "Neural Network Diagram", "500px" %}

A few things to notice:

- **Input layer:** one node for each piece of information going in. Predicting admission from GPA, SAT, and essay score means three input nodes.
- **Hidden layers:** where learning happens. These layers find patterns in the inputs that help predict the output.
- **Output layer:** one node per possible answer. For admission, it might be a single number: the predicted chance.

> **Reflect:** As you add more hidden nodes, the network gets more complex. What do you think the trade-off is between a simpler network and a more complex one?

## See It Train

TensorFlow Playground lets you watch a neural network train in real time in your browser.

<a href="https://playground.tensorflow.org/" target="_blank">Open TensorFlow Playground</a>

There's math terminology around the edges you can ignore. Focus on three things: the colored dots on the left (the two groups the network is trying to tell apart), the network in the middle (the lines change thickness as it learns), and the output image on the right (it reshapes to separate the groups).

Press play and watch. Try switching the dataset shape using the buttons on the far left.

> **Reflect:** Which shapes does the network separate easily? Which ones does it struggle with?

## Deep Learning

**Deep Learning** is neural networks with many layers. More layers means the network can learn more abstract patterns. In an image recognition network, early layers might detect edges. Middle layers combine edges into shapes. Later layers combine shapes into recognizable objects.

When people say "deep learning" today, they usually mean modern neural networks. The two terms are used interchangeably.
