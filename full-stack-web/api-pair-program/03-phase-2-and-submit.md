---
title: "Phase 2 and Submit"
order: 3
---

## Phase 2: User Interaction

Now add a way for the user to fetch different data. Pick one of these (or invent your own):

- A **search input** that fetches data based on the user's query
- **Category buttons** that fetch different slices of data
- A **dropdown** that changes what the API returns
- **Input fields** that modify API parameters (city name, item ID, date, etc.)

When the user interacts with your controls, trigger a new fetch with the updated parameters. Handle loading and error states during these subsequent fetches the same way you did for the initial load. A visible loading message keeps users confident that their click registered.

There are two common ways to wire this up:

1. Put the user's input in state and put that piece of state in the dependency array of your existing `useEffect`. Each change re-runs the effect automatically.
2. Run the fetch directly inside an event handler (like `onSubmit` or `onClick`) instead of through `useEffect`.

Both are valid. The first is cleaner when the fetch should mirror state. The second is clearer when the fetch should only happen on an explicit action like a button click.

> **With your partner:** Talk through which approach fits your interaction before you write it. Then build it.

## Styling

If you have time, style the app so it looks deliberate. Consider:

- A coherent color palette and consistent spacing
- Conditional class names based on data (a Pokémon type, a country region, a weather condition)
- Hover and focus states on interactive elements
- A loading state that doesn't make the page jump around when data arrives

## Presentation

Be ready to walk another group through your app. Cover:

1. The initial fetch when the component mounts
2. How data flows from the API response down through your components
3. Your loading and error states
4. Your Phase 2 interaction and how it triggers a new fetch

Walk through your `useEffect` call and explain the dependency array. Mention any challenges you hit and how you worked through them. The challenges are often the most interesting part to talk about.

## Submit

Push your latest changes, run `npm run deploy`, and confirm the live site reflects Phase 2.

Submit your live GitHub Pages URL on Canvas.

## Feedback

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Full+Stack+Web+Development&unit=API+Data+Display" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
