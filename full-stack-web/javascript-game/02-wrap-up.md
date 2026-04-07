---
title: "Extend, Deploy, and Submit"
order: 2
---

The core loop is done. Now make it your own.

## Extend the Game

Pick directions that fit your theme and what you want to practice. Get one thing working and committed before starting the next.

**Deepen the upgrade system:**
- Track how many times each upgrade has been purchased and show the count
- Scale the cost after each purchase so buying the same upgrade again costs more each time
- Make some upgrades one-time-only and hide the button after purchase

**Add automation:**
- Use `setInterval` to add points every second automatically
- Create upgrades that increase the auto-click rate

**Add feedback and polish:**
- Show a floating "+X" popup near the click button when clicked
- Change the page appearance at score milestones (new background color, a new section unlocking)
- Play a sound on click using an `<audio>` element

**Add a goal:**
- Set a score threshold that shows a win screen
- Add a prestige option: reset the score but multiply future earnings

> **With your partner:** Pick a few things you want to add. Decide which to start with, get it working, then move to the next. Commit your working code before starting each new feature.

## Deploy

Host your game on GitHub Pages so you can share it and submit it. This is a plain HTML/CSS/JavaScript project, so use the **static site** method.

See [Hosting with GitHub Pages](/full-stack-web/orientation/05-github-pages/) for step-by-step instructions.

Make sure your main file is named `index.html` before uploading.

## Submit

Submit the link to your live GitHub Pages site on Canvas. Your repository should include a README with a brief description of your game mechanics and the link to the live site.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web&unit=Interactive+JavaScript+Game" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
