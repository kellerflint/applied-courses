---
title: "A Deliberate Look and Feel"
order: 3
---

Styling isn't a user story, but it's a requirement for the final project. By the end, your app should look like someone designed it on purpose. A researcher should be able to land on it and feel like it's a real tool rather than a class exercise.

## What "deliberate" means

Deliberate means consistent choices applied across the whole app. The opposite is every page looking like a different person built it: one page centered, the next left-aligned, three different blues, random font sizes, etc. Pick your choices once and apply them everywhere.

You already started this. In the [wireframes assignment](/full-stack-web/salamander-project/03-wireframes/) you chose a color palette, and in [Part 1](/full-stack-web/salamander-project-part-1/04-styling-with-tailwind/) you set up Tailwind. Now you carry that palette and a consistent visual language through every page.

A cohesive design usually means deciding and reusing:

- **Color.** Your 3 to 5 color palette from the wireframes: a background, a primary action color, text, and an accent or two. Use them consistently. The "submit" button should be the same color everywhere it appears.
- **Typography.** A consistent heading size and body size. Headings on every page should look like headings on every other page.
- **Spacing.** Consistent padding and gaps. Tailwind's spacing scale makes this easy because the numbers line up across utilities.
- **Layout.** A shared page shell: the nav in the same place, content at a consistent max width, the same margins. You likely already have this in `App.jsx`.
- **States.** Loading, error, and disabled states should be styled too, not bare text. They're part of the app, and the researcher sees them.

## Tailwind first, CSS when you need it

The rule from Part 1 still holds. Reach for Tailwind utilities first, applied at the component level. When you genuinely need something Tailwind doesn't give you cleanly, write component-scoped CSS. The global stylesheet is for app-wide concerns like fonts and base background, not for one specific card.

You must use both **Tailwind and CSS** in the project. Most of your styling will be Tailwind. CSS is for the cases where a utility class would be awkward: a custom animation, a complicated gradient, a reusable component class you'd rather not repeat as ten utilities on every element.

> **With your partner:** Open your app on every page back to back. Where does it look inconsistent? List the specific mismatches: different colors, headings that don't match, uneven spacing. Fix the list. Then resize the browser narrow and wide. Does it hold up, or does it break on a small screen? These apps should look decent and be usable on mobile as well.

## Make it feel like one app

A few things that cheaply make an app feel finished:

- A clear header or nav that's identical on every page.
- Hover and focus states on anything clickable, so the app responds to the user.
- The thumbnail and canvas laid out cleanly with labels.
- Enough breathing room. New designers almost always under-use whitespace.

You don't need to be a designer, but you do need to be consistent and intentional. If you want a starting point for a palette, the tools listed on the [wireframes page](/full-stack-web/salamander-project/03-wireframes/) still apply.

> **With your partner:** Agree on your final palette and write the hex codes (or Tailwind color names). Document your choices in the README or somewhere else in your project files for reference.
