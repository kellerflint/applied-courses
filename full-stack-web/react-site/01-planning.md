---
title: "Planning Your Site"
order: 1
---

You're building a single-page informational website about a topic of your choice. The page will be long, scroll through multiple sections, and look like a real site someone might actually visit. Unlike the fun facts board, this one has a lot more surface area to build, which is exactly the point.

The goal is to practice building a React project the way you'd build a real one: organized files, decomposed components, and styles that live where they belong.

## What You're Building

Your finished site needs all of these:

- A **header** with your site's title
- A **hero section** that introduces your topic with an image
- At least **three content sections**, each with a heading and multiple items
- A **reusable card component** used at least five times with different props
- **Images** in at least two places on the page
- A **footer** with your names

These are the requirements. Everything else is yours to decide: the specific sections, the visual style, how things are laid out, how many components you build beyond the minimum. The goal is a site that looks deliberate and well-crafted.

> **With your partner:** Agree on a topic. Pick something you both know enough about to fill a long page: a game, a film series, a sport, a music genre, a city, a historical era, whatever. The more you already know about it, the less time you'll spend looking things up. I always suggest picking something REAL! What can you make that might be genuinely cool, useful, or interesting?

## Wireframe Your Site

Before writing any code, sketch what your site will look like. A **wireframe** is a rough layout drawing with boxes and labels showing where sections, images, and text will go. It shows what sections exist, where things sit on the page, and what each section contains.

You can wireframe on paper or use a tool like [Wireframe.cc](https://wireframe.cc/).

Once you have a layout sketched out, go back through it and circle or label each area that will become its own component. A section that repeats (like a row of cards) is a strong signal that a component belongs there.

> **With your partner:** Build your wireframe together. Identify distinct components in it before moving on. Note where you'll reuse the same component with different content.

## Sketch Your Component Tree

A **component tree** shows the parent-child relationships between your components. Start from your wireframe and map it out.

Here's an example for a site about a film series:

```
App
├── Header
├── HeroSection
├── Section (title="Films")
│   ├── FilmCard
│   ├── FilmCard
│   └── FilmCard
├── Section (title="Characters")
│   ├── CharacterCard
│   └── CharacterCard
└── Footer
```

Your site needs at least two different reusable components. At least one should appear inside another component, like `FilmCard` inside `Section`.

> **With your partner:** Write out your component tree. For each component, note what props it will take. You'll refine this as you build, but having the structure in front of you makes starting much easier.

## Two Concepts Before You Build

### className

In HTML you write `class="card"`. In JSX, the attribute is `className`. The reason: `class` is a reserved word in JavaScript, so React uses `className` instead. You'll use this on nearly every element you style.

```jsx
<div className="hero">
  <h1>My Site</h1>
</div>
```

### Per-Component CSS

Each component gets its own CSS file. This keeps styles easy to find and easy to change in isolation.

For a `Card` component, you'd have `Card.jsx` and `Card.css` in the same folder. Import the CSS at the top of the component file:

```jsx
import './Card.css'

function Card({ title, description }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default Card;
```

The CSS file covers only what that component renders. Page-level layout and global styles live in `App.css` or `index.css`.
