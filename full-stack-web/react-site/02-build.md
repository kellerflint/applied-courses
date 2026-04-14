---
title: "Build Your Site"
order: 2
---

Work through each section below in order. Read the full section before you start writing code.

## Set Up the Project

Create a new Vite + React project:

```bash
npm create vite@latest
```

Choose React and JavaScript when prompted. Once it's running, delete everything inside the `return ()` in `App.jsx` and clear out both CSS files. Start with a blank page.

> **With your partner:** Get both machines running before continuing.

## Organize Your Files

Create a `components` folder inside `src`. Every component you build goes in there, paired with its own CSS file:

```
src/
├── App.jsx
├── App.css
├── index.css
└── components/
    ├── Header.jsx
    ├── Header.css
    ├── Card.jsx
    ├── Card.css
    └── ...
```

Keeping components in their own folder makes a growing project much easier to navigate.

## Build the Header

Create `Header.jsx` and `Header.css` inside your `components` folder. The header should include your site's title and anchor links for navigation.

Use `className` on your elements and style them in `Header.css`. Import the CSS at the top of `Header.jsx`. Import and render the Header in `App.jsx`.

> **With your partner:** Make the header look intentional before moving on. Give it a background color, padding, typography, and anything else it needs to look good. A plain browser heading is boring!

## Build the Hero Section

Create `HeroSection.jsx` and `HeroSection.css`. The hero introduces your topic and is the first thing visitors see after the header. Include a heading, a short paragraph, and at least one image. Make it visually distinct from the content sections further down the page.

Add it to `App.jsx` right below the Header.

## Build a Reusable Card

Your card component will appear many times on the page, each instance showing different data. Decide what props make sense for your topic: a name and description, an image and a caption, a title and a stat, whatever fits.

Create `Card.jsx` and `Card.css`. Accept your props in the function signature, use `className` on your elements, and style the card in `Card.css`.

Once the card renders correctly with one set of props, use it at least five times in `App.jsx` with different data passed each time.

{% activity "component-as-template.html", "Components as Templates", "600px" %}

> **With your partner:** Trace one card instance from start to screen. Start at the prop value you're passing in `App.jsx`, follow it into the component function, and find where it shows up in the rendered output.

## Add a Section Component

A `Section` component gives `App.jsx` a clean, readable structure as your page grows. The **`children` prop** lets a component render whatever you pass between its opening and closing tags.

Here's the pattern:

```jsx
function Section({ title, children }) {
  return (
    <section className="section">
      <h2>{title}</h2>
      <div className="section-content">
        {children}
      </div>
    </section>
  );
}
```

Use it like this:

```jsx
<Section title="Films">
  <Card title="A New Hope" description="..." />
  <Card title="The Empire Strikes Back" description="..." />
</Section>
```

`Section` accepts any content you place inside it, which makes it genuinely reusable across your whole page.

Create at least three sections on your page, each with a heading and at least two or three cards inside.

> **With your partner:** Once you have two sections working, talk through how `children` flows through the component. What would happen if you passed a paragraph or an image instead of cards?

## Add Images

Put your images in the `public` folder at the root of your project. Reference them with a path starting at `/`:

```jsx
<img src="/my-image.jpg" alt="A short description of what this image shows" />
```

Every image needs a descriptive `alt` attribute. Write a short sentence describing what the image shows. Use images in at least two places.

> **With your partner:** Find or use AI to generate a few images relevant to your topic and add them. Make sure the alt text on each one is genuinely descriptive.

## Build the Footer

Create a `Footer` component. Include your names at minimum. Style it so it reads clearly as a footer, visually separated from the content above it.

> **With your partner:** Scroll through the full page once everything is in place. Does it feel like a real website? Which sections still need more content or better styling?
