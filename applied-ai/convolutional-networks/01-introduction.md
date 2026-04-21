---
title: "Convolutional Neural Networks"
order: 1
---

Today you'll build a convolutional neural network (CNN) on a dataset of your choosing. By the end of class you'll have trained two models on the same data and seen firsthand whether the CNN architecture makes a difference.

First, the core idea behind how CNNs work.

## Filters

The flat network you built for digits flattens the image into a list of numbers, losing all spatial information. A shape shifted two pixels to the right looks completely different, even though it's obviously the same shape.

CNNs solve this with **filters**. A filter is a small pattern detector, typically 3×3 pixels, that slides across the image one position at a time. At each position it checks: does this patch of the image match my pattern? If it does, it activates. If not, it doesn't.

Try it below. Draw something on the grid, pick a filter, and click Run. Watch the amber window scan across the input. The output (feature map) shows where the filter matched.

{% activity "filter-demo.html", "Filter Demo", "320px" %}

Try the horizontal edge filter on a horizontal line. Then try the vertical edge filter on the same drawing. The output should change dramatically.

## Layers Stack Up

One filter detects one kind of pattern. A real CNN runs dozens of filters in parallel, each learning to detect something different. Edges, curves, corners.

The next layer takes those detections as input and combines them. It sees shapes where the first layer saw edges. The layer after that sees higher-level structures. By the end, the network has built up enough to classify the image.

The visualizer below shows this happening on a trained network. Draw a digit and watch what activates at each layer.

{% activity "cnn-visualizer.html", "CNN 2D Visualizer", "700px" %}

*Visualizer by [Adam Harley](https://adamharley.com/nn_vis/cnn/2d.html)*

The goal of this class is just to get the gist of now neural networks function. If you're interested in learning more, there are lots of great videos and resources out there that show and explain each step in detail. Here's one I liked when I was first learning about CNNs: [Image Classification with Convolutional Neural Networks (CNNs)](https://www.youtube.com/watch?v=HGwBXDKFk9I)

## One More Thing

In practice you will almost always use a network architecture someone else designed, but having a little intuition around how they work is useful. The training dynamics you already understand (overfitting, early stopping, learning rate) all carry over and having the gist of what is happening under the hood makes it easier to understand why larger models behave the way they do.
