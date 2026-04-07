---
title: "Reflect & Submit"
order: 3
---

You trained a model and built an app with it. Before moving on, work through these questions with your partner.

## The Workflow

What you did today follows a general pattern that shows up in almost every applied AI project. With your partner, put the steps and descriptions in the right order.

{% activity "workflow-sort.html", "AI Workflow Sort", "520px" %}

## Why So Few Examples?

Most machine learning tasks require thousands or millions of training examples. Your model worked with around 50 per class.

> **With your partner:** Why? What was different about your situation that made this possible?

<details>
<summary>Reveal answer</summary>

Google trained a large neural network called MobileNet on millions of images. That training taught the network to recognize general visual features: edges, corners, textures, shapes. This took days on expensive hardware.

When you trained your model, you reused all of that existing knowledge. Teachable Machine kept the MobileNet layers frozen and trained a small new layer on top that maps those general features to your specific classes. 50 examples was enough because the model already understood what images "look like." It only needed to learn your particular categories.

This technique is called **transfer learning**, and it's one of the most practical tools in applied AI. You'll use it again when you fine-tune YOLO for object detection later in the course.
</details>

## When It Goes Wrong

Think back to when you tested your model. You probably ran into at least one of these situations:

- The model worked for one partner but struggled with the other
- The model got confused when something in the background changed
- Two of your classes were hard for the model to tell apart

> **With your partner:** Pick one problem you actually experienced. What do you think the model was paying attention to in the training data that caused this? Why would that lead to the behavior you saw?

<details>
<summary>Reveal answer</summary>

All three problems come from the same root cause: **the model learns whatever pattern best separates the classes in the training data**, even if that pattern isn't what you intended.

If only one person recorded training data, the model may have learned features of that person's appearance (skin tone, clothing, hand shape) rather than the gesture itself. That was the easiest way to separate the classes in the data it was given.

If every "thumbs up" sample had the same bookshelf in the background, the model may have learned "bookshelf = thumbs up." The background was a reliable signal in the training data, so the model used it.

If two classes look nearly identical on a small webcam image, the model doesn't have enough visual information to tell them apart reliably.

In all three cases, the fix is the same: make your training data more varied so the only consistent difference between classes is the thing you actually care about.
</details>

## Open Discussion

> **With your partner:** Discuss these. There's no single right answer.
>
> 1. If you were going to actually deploy your app to thousnds of users, what specific things might you need to change about your process or approach to training?
>
> 2. Your model runs entirely in the browser on the user's device. What are the advantages of that? What are the limitations compared to sending images to a server?
>
> 3. You used transfer learning to build a custom classifier from a small dataset. Where else might this technique be useful? Think about other kinds of data or scenarios beyond image classification.

## What to Turn In

- Your working `index.html` file
- A brief comment (a few sentences) answering the three discussion questions above

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Teachable+Machines" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
