---
title: "Submit"
order: 4
---

## What you should have

By the end of this pair program your app talks to a real backend instead of mock data:

- Your backend runs on its own port and you can hit every endpoint directly with the browser or curl.
- Vite has a `server.proxy` block forwarding every backend path prefix to the backend.
- A real `src/api.js` module makes `fetch` calls with the same function names your components already used.
- Your components import from `api.js`, and every story you've built so far works against real data.
- The video list shows a real error state when the backend is down.

If anything on that list isn't true, finish it before you submit.

## Push to GitHub

Make sure all your work is committed, including `vite.config.js` and `api.js`. Then push.

Before you split for the day, the partner who wasn't driving most recently should pull the latest changes, start **both** the backend and the frontend on their own machine, and confirm the app loads real data. Sort any issues out now. You'll both need to run the full stack going forward.

## Submit on Canvas

**One partner** submits the GitHub repo URL on Canvas. The repo's README should list both partners' names.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web+Development&unit=Salamander+Project+Part+3" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
