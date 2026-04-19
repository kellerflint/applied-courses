---
title: "Types of Machine Learning"
order: 1
---

There are three main approaches to machine learning. Each solves a different kind of problem, and they differ in what data they need and how the learning actually happens. You'll try a hands-on example of each one.

## Supervised Learning

In supervised learning, you give the model labeled examples and it learns to map inputs to those labels. If you want a model that recognizes spam, you feed it thousands of emails already marked "spam" or "not spam," and it learns which patterns predict which label. The model is "supervised" because the right answer is provided for every training example.

Try it yourself. Teachable Machine lets you train a supervised image classifier in your browser using your webcam. You'll record examples of two or three categories and the model will learn to tell them apart.

<a href="https://teachablemachine.withgoogle.com/train/image" target="_blank">Open Teachable Machine</a>

Spend about ten minutes with it. Create two or three classes (like "thumbs up," "thumbs down," and "nothing"), record 20-30 samples per class, and click Train. You'll build a more complete project with Teachable Machine in the next unit. For now, just get a feel for the process: you provide labeled examples, and the model learns to classify from those labels.

> **Reflect:** What were you actually providing when you recorded your training samples? What was the model doing with that information?

## Unsupervised Learning

In unsupervised learning, the model finds patterns in data on its own. It receives no labels and no correct answers to learn from. The model looks for structure: groupings, similarities, or things that stand out as unusual.

A common unsupervised task is **anomaly detection**, the process of identifying data points that deviate from the normal pattern. The activity below puts you in the role of the algorithm. You'll see data with no labels and have to figure out what's "normal" and flag what doesn't belong.

{% activity "unsupervised-anomaly-demo.html", "Spot the Outlier: Unsupervised Learning", "800px" %}

> **Reflect:** What made something count as an outlier? How did you decide where the line was between "normal" and "doesn't fit"?

## Reinforcement Learning

In reinforcement learning, there's no dataset at all. A model called an **agent** takes actions in an environment and receives rewards or penalties based on what it does. Over time, it learns a strategy that maximizes its total reward.

Nobody tells the agent the right action. It discovers good strategies through trial and error. This is how AlphaGo learned to play Go at a superhuman level, and how robots learn to walk. The agent just plays, receives feedback, and adjusts.

The activity below puts you in the agent's role. You'll see colored shapes and have to figure out which actions earn points. The rules are hidden from you. You learn by playing.

{% activity "reinforcement-learning-demo.html", "Learn the Rules: Reinforcement Learning", "800px" %}

> **Reflect:** How is the process you just went through similar to how a machine learns in reinforcement learning? Where does the "reinforcement" actually come from?

## Check Your Understanding

Try to answer each question before opening the reveal.

### What makes supervised learning "supervised"?

<details>
<summary>Reveal answer</summary>

The model trains on labeled examples where the correct answer is already known. It learns to map inputs to those labels. It's supervised because you're providing the right answers during training, guiding what the model learns.

</details>

### What does an unsupervised model do when there are no labels?

<details>
<summary>Reveal answer</summary>

It finds patterns and structure in data on its own, without being told what anything means. It looks for groupings, similarities, or things that stand out as unusual. There's no right answer to check against.

</details>

### How does a reinforcement learning agent figure out what to do?

<details>
<summary>Reveal answer</summary>

It takes actions in an environment and receives rewards or penalties based on the results. There's no dataset and no labeled examples. The agent discovers good strategies through trial and error, gradually learning which actions lead to the highest reward.

</details>

### Give a real-world example of supervised learning. What are the inputs, and what is the label?

<details>
<summary>Reveal answer</summary>

Many answers work. A few examples:

- **Spam detection:** Each training example is an email (input) labeled "spam" or "not spam" (label). The model learns which words and patterns appear in spam.
- **Disease diagnosis from scans:** Medical images are the input and a doctor's diagnosis is the label. The model learns to spot visual patterns that predict the diagnosis.
- **Loan default prediction:** Customer financial data is the input and whether they actually defaulted is the label. The model learns which factors predict risk.

</details>

### Give a real-world example of reinforcement learning. What is the agent, the environment, and the reward signal?

<details>
<summary>Reveal answer</summary>

Many answers work. A few examples:

- **Game-playing AI:** The agent is the player, the environment is the game, and the reward is the score.
- **Robotics:** The agent is a robot arm, the environment is physical space, and the reward might be successfully grasping an object. The robot learns through trial and error what movements work.
- **Datacenter cooling:** The agent controls cooling systems, the environment is the datacenter, and the reward is reduced energy use without overheating. Google used this approach to cut cooling costs significantly.

</details>
