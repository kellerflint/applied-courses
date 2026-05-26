---
title: "The Tuning Challenge"
order: 2
---

Next user story is the meat of this pair program:

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

Two new ideas in that story: **what binarization actually does to an image**, and **how to draw on a `<canvas>` from inside a React component**. This page covers both. The next page is where you build it.

## What binarization is

Binarization turns a color image into a two-color image. Every pixel becomes either "on" or "off" based on some rule. For our purposes the rule is: if a pixel's brightness is above some threshold, it's "on"; otherwise it's "off."

It's the simplest possible step toward detecting something in an image. A salamander on a light tank floor is going to be darker than the floor, so if you set the threshold somewhere between "tank floor brightness" and "salamander brightness," everything dark stays in the "on" group and you get a silhouette.

Play with the activity below. Drag the slider and watch the image on the right change.

{% activity "binarization-threshold.html", "Binarization Threshold", "520px" %}

> **With your partner:** Find a threshold value where the salamander is clearly visible as a separate shape from the background. What happens at threshold 0? At 255? Talk about what the percentage-of-pixels-above number means.

The thing you just did with the slider is what your app needs to do in React, except your version will also let the user pick a color (which becomes the "on" pixel color) on top of the threshold.

## Canvas in plain HTML

Before getting into React, look at what canvas is on its own. In a vanilla HTML file, drawing a red square on a canvas is about five lines:

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

- `<canvas>` is a **native HTML element**, built into every browser. You don't import it from React or any library.
- The drawing happens through a **drawing API** you get by calling `.getContext('2d')` on the DOM element. That API has methods like `fillRect`, `drawImage`, `arc`, `fill`.
- As soon as you call `fillRect`, the red square shows up. The browser handles displaying it. No render step.

The whole point of the next section is figuring out how to do the equivalent inside a React component.

## In a React component: `useRef`

Inside a React component, you can't write `document.getElementById('myCanvas')` at the top of the function, because **when your component function runs, the DOM elements in your JSX don't exist yet**. There's nothing to find. You need a way to grab the canvas element *after* React has mounted it.

That way is the `useRef` hook. Two lines do the whole thing:

```jsx
const canvasRef = useRef(null);

return <canvas ref={canvasRef} />;
```

`useRef(null)` gives you back a small container object that React keeps around for you across re-renders. The container has one property: `.current`, which starts as `null`. When you pass that container to a JSX element via the `ref` prop, **React assigns `canvasRef.current = (that DOM element)` after it mounts the element**. From then on, `canvasRef.current` is the actual `<canvas>` DOM node, and you can call its native methods on it:

```jsx
canvasRef.current.getContext('2d').fillRect(20, 20, 100, 100);
```

Same `getContext` call as in the plain HTML version. The only difference is how you got a handle to the canvas: `useRef` + the `ref` prop instead of `document.getElementById`. And because the drawing happens through a direct method call on the DOM element, it doesn't go through React's render cycle. The pixels just appear. React isn't involved in the drawing at all.

The activity below shows that pattern in motion. Code on the left with three numbered callouts on the parts that matter; live canvas on the right.

{% activity "useref-canvas.html", "useRef + Canvas", "500px" %}

> **With your partner:** Read the three numbered callouts together. Click "Draw a circle" a few times. Talk through what each callout is doing in your own words. If one doesn't click yet, sit with it side by side with the canvas behavior until it does.

The next page walks you through using this pattern in your own app.
