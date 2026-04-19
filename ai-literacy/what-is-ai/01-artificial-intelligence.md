---
title: "Artificial Intelligence"
order: 1
---

The terms Artificial Intelligence, Machine Learning, Neural Network, Deep Learning, and Generative AI all get used to describe the same kinds of tools. They're related, but not the same.

## What is Artificial Intelligence?

**Artificial Intelligence** is the broadest term. It covers any technique that lets a machine behave in a way we'd call intelligent. That includes hand-coded rule systems, search algorithms, and the most advanced neural networks. A game enemy navigating a maze is AI. So is ChatGPT.

The two activities below are both AI. In both cases, a person wrote the decision-making logic ahead of time, and the machine executes it.

### Following a plan: pathfinding

This is a search algorithm. It finds the shortest route from a start point to a goal by systematically exploring outward, cell by cell. Every step of the logic was written by a programmer ahead of time.

Watch the steps on the left light up as the search runs on the grid. Each step corresponds to something happening in the visualization. Use Step to advance one at a time, or Play to watch it run.

{% activity "ai-pathfinding-demo.html", "Pathfinding: rules-based AI", "640px" %}

> **Reflect:** Where in this algorithm is anything being *learned*? What parts were decided by a programmer ahead of time, and what parts happened while the code was running?

### Following a set of rules: a help-desk bot

This is an **expert system**, a program that mimics how a human expert makes decisions by walking through a set of if/else rules. Try the help-desk bot below. When you reach the end, click "See the decision path."

{% activity "ai-helpdesk-bot.html", "IT help desk: expert system", "620px" %}

The logic was authored entirely by a person. Nothing was learned from data. Every branch existed before the first user ever clicked a button.

> **Reflect:** What other systems have you interacted with that worked like this? Call-center phone trees, insurance claim forms, tax software. Where else have you run into hand-written logic dressed up as a helper?

### "AI is whatever hasn't been done yet"

Both of those examples qualify as AI by the textbook definition. There's a running joke in the field. **AI is whatever hasn't been done yet.** Once something works reliably, it stops feeling like AI and starts feeling like software.

Chess was AI until computers got good at it. Then it was "just chess programs." GPS navigation, spam filters, face unlock on your phone. All of them were AI research problems at some point. Now they're just features.

The label is a moving target. When someone says "this product uses AI," they might mean a neural network with billions of parameters, or a hand-coded rule system from 1985. Both can honestly use the label.
