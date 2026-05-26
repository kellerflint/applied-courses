---
title: "The Tuning Challenge"
order: 2
---

Next user story is the bulk of this pair program:

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

Two new ideas in that story: **what binarization actually does to an image**, and **how to draw on a `<canvas>` from inside a React component**. This page covers the concepts. The next page is where you build it.

## What binarization is

Binarization turns a color image into a two-color image. Every pixel becomes either "on" or "off" based on some rule.

Play with the activity below. Drag the slider and watch the image on the right change.

{% activity "binarization-threshold.html", "Binarization Threshold", "520px" %}

The activity uses brightness as its rule because it's the simplest one to show. Your app uses a different rule. Instead of brightness, it compares each pixel to a picked **target color** (the color you expect the salamander to be) and marks it "on" if the colors are close enough.

## Canvas in plain HTML

You're going to need to draw a binarization version of the original image. How?

Before getting into React, look at what canvas is on its own. In a vanilla HTML file, drawing a square on a canvas is about five lines:

```html
<canvas id="myCanvas" width="400" height="300"></canvas>
<script>
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'red';
  ctx.fillRect(20, 20, 100, 100);
</script>
```

Three things worth knowing:

- `<canvas>` is a native HTML element, built into every browser. You don't import it from React or any library.
- The drawing happens through a drawing API you get by calling `.getContext('2d')` on the DOM element. That API has methods like `fillRect`, `drawImage`, `arc`, `fill`.
- As soon as you call `fillRect`, the red square shows up. The browser handles displaying it.

The whole point of the next section is figuring out how to do the equivalent inside a React component.

## What `useRef` is

`useRef` is a React hook that gives you a container for a value you want to hang on to without putting it in state. Looks like this:

```jsx
const myRef = useRef(initialValue);
// Read:  myRef.current
// Write: myRef.current = newValue;
```

Two things about that container are worth knowing up front:

- **It persists across re-renders.** Every time your component re-runs, React hands you back the same container with whatever `.current` was on the previous render. The `initialValue` you pass to `useRef` is only used on the very first render. After that it's ignored.
- **Changing `.current` does not trigger a re-render.** It's a plain JavaScript property assignment. React doesn't know or care that you changed it.

That's the whole concept. It's useful for any value you want to remember across renders without making React do anything about it: timer IDs, the previous value of a prop, a game-state object, or (as you'll see in a second) a handle to a DOM element.

## Using `useRef` to grab the canvas

Inside a React component, you can't write `document.getElementById('myCanvas')` at the top of the function, because when your component function runs, the DOM elements in your JSX don't exist yet. There's nothing to find. You need a way to grab the canvas element *after* React has mounted it.

`useRef` solves this with a small bonus that only applies when you pass the container to a JSX element. Here's the whole pattern in one component:

```jsx
import { useRef } from 'react';

function CanvasDemo() {
  const canvasRef = useRef(null);

  function draw() {
    canvasRef.current.getContext('2d').fillRect(20, 20, 100, 100);
  }

  return (
    <>
      <canvas ref={canvasRef} />
      <button onClick={draw}>Draw</button>
    </>
  );
}
```

Three things are happening:

1. `useRef(null)` gives you back a small container object that React keeps around for you across re-renders. The container has one property: `.current`, which starts as `null`.
2. Passing the container to a JSX element via the `ref` prop (`ref={canvasRef}`) tells React: **after you mount this element, assign `canvasRef.current = (that DOM element)`**.
3. After mount, `canvasRef.current` is the actual `<canvas>` DOM node. So anywhere code runs later (like the `draw` function on a button click), `canvasRef.current.getContext('2d')` gives you the drawing API, and you call its native methods.

Same `getContext` call as in the plain HTML version. The only difference is how you got a handle to the canvas: `useRef` + the `ref` prop instead of `document.getElementById`. And because the drawing happens through a direct method call on the DOM element, it doesn't go through React's render cycle. The pixels just appear. React isn't involved in the drawing at all.

The activity below shows that pattern in motion. Code on the left with three numbered callouts on the parts that matter; live canvas on the right.

{% activity "useref-canvas.html", "useRef + Canvas", "500px" %}

> **With your partner:** Read the three numbered callouts together. Click "Draw a circle" a few times. Talk through what each callout is doing in your own words. If one doesn't click yet, sit with it side by side with the canvas behavior until it does.

The next page walks you through using this pattern in your own app.
