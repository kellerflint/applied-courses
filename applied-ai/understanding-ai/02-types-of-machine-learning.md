---
title: "Types of Machine Learning"
order: 2
---

There are three main approaches to machine learning. Each one solves a different kind of problem, and they differ in what kind of data they need and how they learn. You're going to try a hands-on demo of each one.

## Supervised Learning

In supervised learning, you give the model labeled examples ("this image is a cat," "this image is a dog") and it learns to map inputs to those labels. The model is supervised because you're telling it the right answer for every training example.

Try it yourself. Teachable Machine lets you train a supervised image classifier right in your browser. You'll record examples of different categories using your webcam, and the model will learn to tell them apart.

<a href="https://teachablemachine.withgoogle.com/train/image" target="_blank">Open Teachable Machine</a>

Train a quick model with 2-3 classes (like "thumbs up" vs. "thumbs down" vs. "nothing"). Record about 30 samples for each class and click Train. You'll build a full project with Teachable Machine later in the course. For now, just get a feel for the process: you provide labeled data, and the model learns to classify based on your labels.

## Unsupervised Learning

In unsupervised learning, the model works with unlabeled data. There are no "right answers" to learn from. Instead, the model looks for structure in the data on its own: patterns, groupings, or things that don't fit.

A common unsupervised task is **anomaly detection**: finding data points that deviate from the normal pattern. The demo below puts you in the role of the algorithm. You'll see data with no labels and have to figure out what's "normal" and flag what doesn't belong.

{% activity "unsupervised-anomaly-demo.html", "Spot the Outlier: Unsupervised Learning", "800px" %}

## Reinforcement Learning

In reinforcement learning, there's no dataset at all. Instead, the model (called an **agent**) takes actions in an environment and receives rewards or penalties based on what it does. Over time, it learns a strategy that maximizes its total reward.

The key difference from supervised learning: nobody tells the agent the right action. It has to discover good strategies through trial and error.

The demo below puts you in the agent's role. You'll see colored shapes and have to figure out which actions earn points. The rules are hidden. You learn by playing.

{% activity "reinforcement-learning-demo.html", "Learn the Rules: Reinforcement Learning", "800px" %}

## Check Your Understanding

Below are six questions to check your understanding. Partners should swap back and forth answering each question without looking at the lesson or any notes. Answer out loud before opening the reveal and reflect briefly on anything you might have missed.

### Supervised Learning

> **Partner A:** Describe supervised learning in your own words. What makes it "supervised"?

<details>
<summary>Reveal answer</summary>

The model is trained on labeled examples where the correct answer is already known. It learns to map inputs to those labels. It's "supervised" because you're providing the right answers during training, guiding what the model learns.

</details>

### Unsupervised Learning

> **Partner B:** Describe unsupervised learning in your own words. What does the model do when there are no labels?

<details>
<summary>Reveal answer</summary>

The model finds patterns and structure in data on its own, without being told what anything means. It looks for groupings, similarities, or things that stand out as unusual. There's no "right answer" to check against.

</details>

### Reinforcement Learning

> **Partner A:** Describe reinforcement learning in your own words. How does the agent figure out what to do?

<details>
<summary>Reveal answer</summary>

An agent takes actions in an environment and receives rewards or penalties based on the results. There's no dataset and no labeled examples. The agent discovers good strategies through trial and error, gradually learning what actions lead to the highest reward.

</details>

### Supervised Learning Example

> **Partner B:** Come up with a real-world application that uses supervised learning. What would the training data look like? What are the inputs, and what is the label the model learns to predict?

<details>
<summary>Reveal answer</summary>

Many answers work here. A few examples:

- **Spam detection:** Each training example is an email (input) labeled "spam" or "not spam" (label). The model learns which words and patterns appear in spam.
- **Disease diagnosis from scans:** Images are the input, and a doctor's diagnosis is the label. The model learns to spot visual patterns that predict the diagnosis.
- **Loan default prediction:** Customer financial data is the input, and whether they actually defaulted is the label. The model learns which factors predict risk.

</details>

### Unsupervised Learning Example

> **Partner A:** Come up with a real-world application that uses unsupervised learning. What data goes in, and what kind of structure or pattern is the model looking for?

<details>
<summary>Reveal answer</summary>

Many answers work here. A few examples:

- **Customer segmentation:** Purchase history and behavior go in with no labels. The model groups customers by similarity so a business can target each group differently.
- **Network intrusion detection:** Normal traffic patterns go in unlabeled. The model learns what "normal" looks like and flags activity that doesn't fit.
- **Topic modeling in documents:** Raw text goes in. The model finds recurring clusters of words that suggest underlying topics, with no human defining the topics in advance.

</details>

### Reinforcement Learning Example

> **Partner B:** Come up with a real-world application that uses reinforcement learning. What is the agent, what is the environment, and what does the reward signal look like?

<details>
<summary>Reveal answer</summary>

Many answers work here. A few examples:

- **Game-playing AI:** The agent is the player, the environment is the game, and the reward is the score. The agent tries actions and keeps the ones that increase its score over time.
- **Robotics:** The agent is a robot arm, the environment is physical space, and the reward might be successfully grasping an object. It learns through trial and error what movements work.
- **Datacenter cooling:** The agent controls cooling systems, the environment is the datacenter, and the reward is reduced energy use without overheating. Google has used this approach to cut cooling costs.

</details>
