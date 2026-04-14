---
title: "What is AI?"
order: 1
---

You've probably heard a lot of terms thrown around: Artificial Intelligence, Machine Learning, Deep Learning, Generative AI. They're all related, but each one means something specific. Knowing where each sits makes it easier to know what tool you're actually using.

## Artificial Intelligence

**Artificial Intelligence** is the broadest term. It covers any technique that lets a machine behave in a way we'd call intelligent. That includes hand-coded rule systems, search algorithms, and the most advanced neural networks. A game enemy navigating a maze is AI. So is ChatGPT.

The two activities below both count as AI. In both cases, a person wrote the decision-making logic ahead of time, and the machine just follows it.

### Following a plan: pathfinding

The first example is a search algorithm. It finds the shortest route from a start point to a goal by systematically exploring outward, cell by cell, until it reaches the destination. Every step of the procedure was written by a person. The machine just executes it.

Watch the pseudocode on the left light up as the search happens on the grid. Each line of code corresponds to something happening on the grid, so you can see exactly what the algorithm is doing at each moment. Use the Step button to advance one line at a time, or hit Play to watch it run.

{% activity "ai-pathfinding-demo.html", "Pathfinding: rules-based AI", "640px" %}

> **With your partner:** Where in this algorithm is anything being learned? What parts were decided by a programmer ahead of time, and what parts were decided while the code was running?

### Following a set of rules: an IT help-desk bot

The second example is an **expert system**: a program that mimics how a human expert makes decisions by walking through a set of if/else rules. In this case, the expert is a tech support agent. Try the help-desk bot below.

{% activity "ai-helpdesk-bot.html", "IT help desk: expert system", "620px" %}

Every branch of the logic was written by hand. When you click "See the rules it followed" at the end, you see exactly that.

> **With your partner:** What other systems have you interacted with that felt like this? Call-center phone trees, insurance claim forms, tax software. Where have you run into clearly hand-written logic dressed up as a helper?

### "AI is whatever hasn't been done yet"

Both of those examples are AI by the textbook definition. But there's a running joke in the field: **AI is whatever hasn't been done yet.** Once something works, it stops feeling like AI and starts feeling like regular software.

Chess was AI until computers got good at it. Then it was "just chess programs." Spell check was AI until it worked reliably. Then it was "just spell check." GPS navigation, spam filters, face unlock on your phone. All of them were AI research problems at some point. Now they're just features.

The term is a moving target. That matters because when someone says "this product uses AI," they might mean a neural network with billions of parameters, or a hand-coded rule system from 1985. Both can honestly use the label. Ask what's actually under the hood.

## Machine Learning

**Machine Learning** is a subfield of AI where the machine learns patterns from data. A person provides examples, and the machine figures out the pattern on its own. Predicting house prices from past sales, flagging spam emails, recommending videos: these all use machine learning.

The activity below walks through a classic example: predicting someone's chance of college admission from three things, their GPA, their SAT score, and the score their admission essay got from the readers. The first section shows the raw data. The second section shows how each piece of data relates to the outcome as a graph. The third section lets you plug in your own numbers and see a prediction.

{% activity "ml-admission-demo.html", "Predicting admission chance", "820px" %}

> **With your partner:** If you wanted this model to make better predictions, what other pieces of data would you want to feed it? What data would you avoid, and why?

## Neural Networks

**Neural Networks** are a specific machine learning technique inspired loosely by how the brain processes information. They use layers of interconnected nodes called **neurons**, and each connection between neurons has a **weight**. Training a neural network means adjusting all those weights until the network produces the right outputs for the inputs you care about.

Neural networks are what make modern image recognition, speech recognition, and text generation work at scale. They are the core technology behind most of the AI you've heard of in the last few years.

The easiest way to get a feel for a neural network is to watch one train. **TensorFlow Playground** is a small in-browser neural network you can play with directly.

<a href="https://playground.tensorflow.org/" target="_blank">Open TensorFlow Playground</a>

The interface has some math terminology around the edges that you can skip. Focus on three things:
- The colored dots on the left. These are the training data, two groups the network is trying to tell apart.
- The network in the middle. Circles are neurons, lines are connections between them. Line thickness shows how strong each connection is.
- The output image on the right. This shows how the network is currently splitting the space between the two groups.

Press the play button at the top and watch. The lines change thickness as the network adjusts its weights, and the output image on the right reshapes itself to separate the dots more cleanly. That's training happening in real time. After it runs for a bit, try switching the dataset with the buttons on the far left and running it again.

> **With your partner:** After running a few datasets, which shapes does the network separate easily? Which ones does it struggle with or fail to separate at all?

### Deep Learning

**Deep Learning** is neural networks with a lot of layers. That's the whole definition. Historically people called anything with more than two or three hidden layers "deep." Modern systems like GPT have dozens or even hundreds of layers.

More layers means the network can learn more abstract patterns. In an image recognition network, early layers might detect edges. Middle layers combine those edges into shapes. Later layers combine shapes into whole objects like faces or cars. The depth is what lets the network build up that kind of complexity.

When people say "deep learning" today, they usually just mean modern neural networks. The two terms are often used interchangeably.

## Generative AI

**Generative AI** uses deep neural networks to create new content: text, images, code, audio, video. ChatGPT generates text. DALL-E and Midjourney generate images. Suno generates music. All of them are generative AI.

The core mechanism behind a text generator is simpler than it sounds. The model predicts the next word, technically the next **token**, based on everything it has seen so far. Then it adds that word to its output and predicts the next one. Then the next. Over and over until it stops.

The activity below shows that process step by step. Watch the probability bars on the right update as each new token is chosen. Start slow so you can see what's happening, then speed it up and watch what real-time text generation looks like.

{% activity "genai-token-predictor.html", "How an LLM generates text", "600px" %}

Every word you've ever read from ChatGPT was produced by roughly the same loop, running on a much bigger model with many more possible next tokens at each step.

## How it all fits together

These four terms nest inside each other. Generative AI is also neural networks. Neural networks are also machine learning. Machine learning is also AI. A single tool can be accurately described by all four labels at once. Which label you reach for depends on which aspect of the system you want to talk about.

{% activity "ai-nested-labels.html", "How many labels apply?", "560px" %}

> **With your partner:** Pick one AI tool you use often. Which of these four labels apply to it? How do you know?
