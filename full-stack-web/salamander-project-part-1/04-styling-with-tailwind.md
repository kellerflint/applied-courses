---
title: "Styling with Tailwind"
order: 4
---

Your app works. But it probably looks awful. 

Let's do something about that.

## How styling moved

Old web style kept everything separated by language. HTML in templates, CSS in stylesheets, JS in script files. The thinking was *separation of concerns*: markup, presentation, and behavior each got their own files. In practice that meant three giant files per feature. Touching a button meant editing the template, hunting the right selector in the stylesheet, and finding the click handler in the script. Three open tabs to change one thing.

React (and modern tooling generally) flipped it. Concerns are still separate, but they live together at the **component level** instead of by language. One component file owns its markup, behavior, and styling. The Videos page you just built is markup (JSX), state (`useState`), data fetching (`useEffect`), and rendering, all in one file. The next step is putting styling there too.

The structural improvement is that big files become small files. You don't end up with one giant `App.jsx`, you end up with a Videos component, a Preview component, a VideoListItem component, each of them small and self-contained. Components are the unit of reuse. Anything specific to a component should live with it.

## What Tailwind is

Tailwind is a CSS framework built around tiny **utility classes**. Instead of writing this:

```css
.card {
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
}
```

```html
<div class="card">...</div>
```

You write this:

```jsx
<div className="p-4 bg-white rounded-lg shadow">...</div>
```

Each class does one thing. `p-4` is padding. `bg-white` is a background color. `rounded-lg` is border radius. `shadow` is box-shadow. You compose UI from a small vocabulary of utilities.

If you've spent years separating concerns, your first reaction is probably *isn't this a step backward?* Stick with it. There are real wins:

- **You almost never write custom CSS.** Less time naming things, less context-switching between files.
- **Styles don't drift.** When you delete a component, its styles go with it. There's no orphan CSS rotting in a stylesheet.
- **Reading the markup tells you what it looks like.** You don't have to jump to a stylesheet to figure out what `.card` means this week.

There's a utility for almost every CSS property you'd reach for: padding, margin, width, font size, color, flexbox, grid, hover states, transitions, all of it. The numbers (`p-4`, `text-lg`, `gap-2`) come from a consistent design scale, so anything written like `*-4` is the same value across utilities and your spacing matches without doing math.

You don't memorize the utilities. You search for them. The [official Tailwind docs](https://tailwindcss.com/docs) are *the* reference. The search box at the top is how everyone uses it: type "padding" or "rounded" or "background color" and you land on the page with every variant listed.

## The rule going forward

Apply styles at the component level wherever possible. Reach for Tailwind first. When you genuinely need something Tailwind doesn't have, write component-scoped CSS (a `.module.css` file or a small CSS file imported by that component) rather than dumping rules into a global stylesheet. The global stylesheet is for app-wide concerns like fonts and base colors, not "the card on the Videos page."

> **With your partner:** Open the [Tailwind docs](https://tailwindcss.com/docs) and use the search to find the utilities for these three things: centering an item horizontally on the page, putting space between items in a list, and changing a button's background color on hover. You don't need to write code yet. Just practice the lookup. This is how you'll work with Tailwind from now on.
