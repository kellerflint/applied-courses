---
title: "Add Tailwind to Your Project"
order: 5
---

Now wire Tailwind into your project and start using it.

## Install

Two packages, one config edit, one CSS import. From your project root:

```bash
npm install tailwindcss @tailwindcss/vite
```

That installs Tailwind's core engine and the Vite plugin that hooks it into your build.

In `vite.config.js`, add the plugin:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Now `src/index.css`. The Vite scaffold drops a fair amount of opinionated CSS in here (custom variables, an aggressive `h1` size, a fixed `#root` width, etc). Those rules will fight every Tailwind utility you try to apply, so the cleanest thing is to wipe the file and start over. Replace the entire contents of `src/index.css` with:

```css
@import "tailwindcss";
```

That's it. Tailwind ships its own resets and base styles, so you don't need anything else here yet.

Restart the dev server.

## Verify it's working

Open `src/pages/Home.jsx` and add a Tailwind class to the heading:

```jsx
<h1 className="text-4xl font-bold text-blue-600">Salamander Tracker</h1>
```

Reload `/`. The heading should now be larger, bold, and blue. If nothing changed, Tailwind isn't picking up your file. Check that the Vite plugin is in `vite.config.js` and that `@import "tailwindcss"` is at the top of `src/index.css`. Restart the dev server again after fixing.

## Style your pages

Now go through your app and apply Tailwind to what you've built so far. There are no required classes. Your wireframes guide what looks right.

Lean on the [Tailwind docs](https://tailwindcss.com/docs) search as you go. The categories you'll hit on almost every page: layout (flex, grid, container width), spacing (padding and margin), typography (size, weight, color), and borders. Most pages benefit from a centered max-width wrapper, a clear nav, headings that stand out from body text, and consistent spacing between items in any list.

Don't try to nail it on the first pass. Ship a coherent rough version of every page, then iterate.

> **With your partner:** Look at your wireframes. What's the overall feel? Clean and minimal? Bold and friendly? Pick a direction together before you start applying styles.

> **With your partner:** Figure out a specific color palette if you haven't already. The Tailwind docs have a [color reference](https://tailwindcss.com/docs/colors) you can pick from. You can change them later.

## What "done enough" looks like

For this pair program, "done enough" means each page reads as deliberate. Headings stand out, links are clearly clickable, content has breathing room, the palette is consistent across pages. You're aiming for *this looks intentional* instead of *this is unstyled HTML*.

Iterate until you and your partner both agree it's at that bar.
