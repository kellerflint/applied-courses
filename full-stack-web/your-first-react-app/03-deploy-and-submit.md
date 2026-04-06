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
