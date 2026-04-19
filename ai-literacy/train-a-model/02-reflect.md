---
title: "Reflect"
order: 2
---

You trained a model from scratch using only a few dozen examples. Before moving on, work through these questions.

## Why So Few Examples?

Most machine learning tasks require thousands or millions of training examples. Your model worked with around 50 per class.

> **Reflect:** Why did that work? What made your situation different from a model trained from scratch?

<details>
<summary>Reveal answer</summary>

Google trained a large neural network called MobileNet on millions of images. That training taught the network to recognize general visual features: edges, corners, textures, shapes. This took days of computing on expensive hardware.

When you trained your model, you reused all of that existing knowledge. Teachable Machine kept the MobileNet layers frozen and trained only a small new layer on top that maps those general features to your specific classes. 50 examples was enough because the model already understood what images look like. It only needed to learn your particular categories.

This technique is called **transfer learning**, and it's one of the most practical tools in applied AI. It's also why a relatively small organization can build a useful image classifier without training a model from scratch.

</details>

## When It Goes Wrong

Think back to the failure you found when testing.

> **Reflect:** Pick one failure. What do you think the model was actually paying attention to in the training data that caused it?

<details>
<summary>Reveal answer</summary>

The model learns whatever pattern most reliably separates the classes in the training data, even if that pattern is not the one you intended it to learn.

If every "thumbs up" sample had the same bookshelf in the background, the model may have learned "bookshelf = thumbs up" rather than the gesture. If only one person recorded training data, the model may have learned features of that person's appearance rather than the gesture itself.

The fix is the same in both cases: make the training data more varied so the only consistent difference between classes is the thing you actually want the model to learn.

</details>

## Open Questions

> **Reflect:** Think through these. There's no single right answer.
>
> 1. You trained this model in a controlled setting. What would you need to change if you were deploying it to thousands of users in different environments?
>
> 2. Your model ran entirely in your browser, on your device. What are the advantages of that? What are the trade-offs compared to sending images to a server for processing?
>
> 3. Transfer learning let you build a custom image classifier from a small dataset. Where else might that technique be useful? Think beyond image classification.

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=AI+Literacy&unit=Train+a+Model" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
