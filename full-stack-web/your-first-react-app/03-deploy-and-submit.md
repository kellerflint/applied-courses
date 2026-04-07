---
title: "Deploy, Extend, and Submit"
order: 3
---

## Deploy

Get your project live before doing anything else. Follow the React/Vite deploy instructions here: [Hosting with GitHub Pages](/full-stack-web/orientation/05-github-pages/)

Once that's done, run `npm run deploy` any time you want to push the latest version to your live site.

> **With your partner:** Get both of your sites live before moving on. Verify the URL loads correctly.

## Keep Building

Your site is live. Use the rest of class time to keep adding to it.

A few directions to try:

**Add more cards.** Come up with some more facts between you. Get to know each other and fill up the page!

**Build a second component.** Try building out a nicer header component that includes not just the `<h1>`, but also borders, your name, your partner's name, and other styling to give it more substance. Abstract it into its own `PageHeader` component.

**Try grouping.** Wrap related facts in a `<section>` with an `<h2>` label. See if you can make a `FactSection` component that takes a `title` prop and wraps whatever you put inside it.

## Submit

Run `npm run deploy` to push your final version live.

Submit your live URL on Canvas.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web+Development&unit=Your+First+React+App" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
