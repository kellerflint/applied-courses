---
title: "The Tuning Challenge"
order: 2
---

Next user story is the meat of this pair program:

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

Two new ideas in that story: **what binarization actually does to an image**, and **how to make a `<canvas>` redraw in response to React state changes**. This page covers both. The next page is where you actually build it.

## What binarization is

Binarization turns a color image into a two-color image. Every pixel becomes either "on" or "off" based on some rule. For our purposes the rule is: if a pixel's brightness is above some threshold, it's "on"; otherwise it's "off."

It's the simplest possible step toward detecting something in an image. A salamander on a light tank floor is going to be darker than the floor, so if you set the threshold somewhere between "tank floor brightness" and "salamander brightness," everything dark stays in the "on" group and you get a silhouette.

Play with the activity below. It uses a real frame from a research video. Drag the slider and watch the image on the right change.

{% activity "binarization-threshold.html", "Binarization Threshold", "520px" %}

> **With your partner:** Find a threshold value where the salamander is clearly visible as a separate shape from the background. What happens at threshold 0? At 255? At the value where the salamander first disappears, what percentage of pixels are still above? Talk about what that number means.

The thing you just did with the slider is what your app needs to do in React, except your version will also let the user pick a color (which becomes the "on" pixel color) on top of the threshold.

## First, in plain HTML

Forget React for a minute. If you wanted to draw on a canvas in a vanilla HTML page, the whole program is about five lines:

```html
<canvas id="myCanvas" width="400" height="300"></canvas>
<script>
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'red';
  ctx.fillRect(20, 20, 100, 100);
</script>
```

A few things worth noticing:

- `<canvas>` is a **native HTML element**, built into every browser. You don't import it from React or any library. It's been part of HTML for fifteen years.
- The canvas element itself is just an empty rectangle. The drawing happens through a **drawing API** you get by calling `.getContext('2d')` on the DOM element. That API has methods like `fillRect`, `drawImage`, `arc`, `fill` for putting pixels on the canvas.
- As soon as you call `fillRect`, the red square shows up. The browser handles displaying whatever you've drawn. There's no submit step, no render step.

Everything else on this page is figuring out how to do the equivalent inside a React component.

## Doing it in React, the obvious-but-broken way

Inside a React component, you can't write a `<script>` tag and grab the DOM right after, because **when your component function runs, the DOM elements in your JSX don't exist yet**. React hasn't mounted them. If you write:

```jsx
function CanvasDemo() {
  const canvas = document.getElementById('myCanvas');  // null - not mounted yet
  const ctx = canvas.getContext('2d');                 // crash
  return <canvas id="myCanvas" />;
}
```

You crash on the second line. The `<canvas>` you're trying to reach is in the JSX *below* the line that's trying to use it. There's nothing in the DOM yet.

The pattern you'd reach for next is `useEffect`, which runs *after* React mounts your JSX:

```jsx
function CanvasDemo() {
  useEffect(() => {
    const canvas = document.getElementById('myCanvas');
    const ctx = canvas.getContext('2d');
    ctx.fillRect(20, 20, 100, 100);
  }, []);

  return <canvas id="myCanvas" />;
}
```

This actually works. By the time the effect runs, React has mounted the `<canvas>` and `getElementById` can find it. But there are a few reasons it's brittle:

- You need a globally unique `id`. Render two `CanvasDemo`s on the same page and they fight over the same id.
- `getElementById` scans the whole document. Fine in a tiny app, fragile in a big one.
- It's not the way React-aware code grabs DOM elements. There's a purpose-built tool.

That purpose-built tool is `useRef`.

## What `useRef` actually is

The cleanest way to understand `useRef` is to compare it to two things you already know: a plain `let` variable, and `useState`.

|  | Survives re-renders? | Triggers a re-render when changed? |
|---|---|---|
| `let count = 0` inside the component | No, resets every render | No |
| `useState(0)` | Yes | Yes |
| `useRef(0)` | Yes | No |

`useRef` is the one combination you can't get the other ways: a value that **persists across re-renders without causing them**.

The difference between `let` and `useRef` is the one that's subtlest, and it's the reason `useRef` exists. Play with the activity below to see it.

{% activity "let-vs-useref-counter.html", "let vs useRef Counter", "560px" %}

> **With your partner:** On the left (`let count`) panel, click `+1` three times and watch the count climb in the log. Now click `force re-render` and then `+1` again. What happens? Now do the same sequence on the right (`useRef`) panel. What's different? Why?

The thing the activity shows: `let` accumulates fine *until something else causes a re-render*. In a real app, lots of unrelated things cause re-renders: a parent's state changes, a sibling updates, a prop changes. Any of them resets your `let`. You can't depend on it. `useRef` solves that by giving you a container React hands back with `.current` intact, on every render.

The React docs call this use of `useRef` [Referencing a value with a ref](https://react.dev/reference/react/useRef#referencing-a-value-with-a-ref). Game state, timer IDs, the previous value of a prop — any value you want to remember across renders without making React track it.

## The DOM-ref pattern

The counter example uses `useRef` for a number. The second way to use it is for a DOM element, which is what we need for canvas. The React docs call this [Manipulating the DOM with a ref](https://react.dev/reference/react/useRef#manipulating-the-dom-with-a-ref).

The shape:

```jsx
const canvasRef = useRef(null);

return <canvas ref={canvasRef} />;
```

When you pass a ref to a JSX element via the `ref` prop, React does something extra. After it mounts the element to the DOM, **React itself assigns `canvasRef.current = (that DOM canvas element)`**. You didn't write `canvasRef.current = ...` anywhere; React did it for you.

So the timeline is:

1. `useRef(null)` runs. `canvasRef.current` is `null`.
2. React renders the JSX. The browser creates a real `<canvas>` DOM element.
3. React assigns `canvasRef.current = (that DOM canvas)`. Now `.current` is the actual element.
4. Anywhere you can run code after mount (inside a `useEffect`, inside an `onClick` handler), `canvasRef.current.getContext('2d')` gives you the drawing API.

This is the React-idiomatic version of `document.getElementById('myCanvas')`. Same end result (a handle to the DOM element), without the global id, without the document scan, without the timing problem. React only fills in `.current` after the element exists.

Play with the activity below. The code is on the left with three callouts on the parts that matter. The live canvas is on the right.

{% activity "useref-canvas.html", "useRef + Canvas", "500px" %}

> **With your partner:** Read the three numbered callouts in the code panel. Click "Draw a circle" a few times. Talk through what each callout does in your own words. Watch the render count and the ref output panel as you click. What does each one tell you about how `useRef` is working?

That's the whole `useRef` story you need. On the next page you'll use it twice: once for the canvas (so you can draw on it), and once for the loaded `Image` object (so you can hang on to it without making it part of React state). The second use is the value-ref pattern from the counter activity, applied to an image.
