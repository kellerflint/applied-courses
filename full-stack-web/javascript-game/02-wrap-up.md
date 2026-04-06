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
