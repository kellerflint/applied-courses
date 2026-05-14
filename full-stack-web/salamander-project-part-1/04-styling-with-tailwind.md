---
title: "Styling with Tailwind"
order: 4
---

Your app works. It looks awful. Time to do something about that.

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

A short cheat sheet for the most common utilities:

- **Spacing:** `p-4` (padding all sides), `px-4 py-2` (horizontal/vertical), `m-2`, `mt-8`
- **Sizing:** `w-full`, `h-12`, `max-w-md`
- **Layout:** `flex`, `gap-4`, `items-center`, `justify-between`, `grid grid-cols-3`
- **Typography:** `text-lg`, `font-bold`, `text-gray-700`
- **Color:** `bg-blue-500`, `text-white`, `border-gray-200`
- **Effects:** `rounded-lg`, `shadow`, `hover:bg-blue-600`

The numbers (`p-4`, `text-lg`, `gap-2`) come from a consistent design scale. Anything written like `*-4` is the same value across utilities, so spacing and sizing match without you doing math.

## The rule going forward

Apply styles at the component level wherever possible. Reach for Tailwind first. When you genuinely need something Tailwind doesn't have, write component-scoped CSS (a `.module.css` file or a small CSS file imported by that component) rather than dumping rules into a global stylesheet. The global stylesheet is for app-wide concerns like fonts and base colors, not "the card on the Videos page."

You don't have to memorize the utilities. The [Tailwind docs](https://tailwindcss.com/docs) are searchable, and most teams keep them open in a tab while building.

> **With your partner:** Open the Tailwind docs and look up how to do these three things: center an item horizontally on the page, put space between items in a list, and change a button's background color on hover. You don't need to write code yet. Just find the utilities. This is the shape of how you'll work with Tailwind from now on.
