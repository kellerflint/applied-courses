---
title: "Reflect & Submit"
order: 8
---

Once your app is working, take time to reflect on what you built before you submit. The reflection is part of the deliverable, and the questions below are worth thinking through with your partner.

## The comparison

Your README needs a paragraph comparing color masking to YOLO based on what you actually saw. Before you write it, talk it through.

> **With your partner:** Pull up a frame where YOLO succeeded and color masking would have struggled. Then find one where color masking would have been just as good or better. Be specific about what made the difference.

<details>
<summary>Reveal answer</summary>

There's no single right answer here, but the strongest comparisons usually point at things like:

YOLO wins when the background isn't uniform (textured tank floors, leaves, debris), when lighting changes mid-recording, when there are multiple salamanders that overlap or pass over each other, and when the salamander's color shifts (wet vs dry, in shadow, near a colored object).

Color masking wins when the setup is controlled, when speed matters more than flexibility, when you have no labeled data and don't have time to make any, or when the alternative would require a much larger training set than you can realistically build.

"Better" depends on the constraints. A study with clear consistent backgrounds might be a color masking job. A study across many conditions probably wants YOLO.

</details>

## What you'd do with more time

Every project hits scope limits. The cuts you made are useful information.

> **With your partner:** What's the next thing you would have built if you had another week? Why didn't it make the cut for this version?

## Demo prep

You'll do a live demo during class in groups. Plan what you're going to show.

A demo should walk through:

- The app running end to end on one of the videos
- All metrics you implemented (especially the unique one you added)
- A quick mention of how you went about training your model
- Any major challenges that came up

## Submit

Push your code to GitHub. Make sure your repo includes:

- Your trained model file
- The README with run instructions, dataset details, and the color masking comparison
- All source code for both the backend and frontend

**Both partners submit individually on Canvas** with the GitHub link.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Salamander+Tracker" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
