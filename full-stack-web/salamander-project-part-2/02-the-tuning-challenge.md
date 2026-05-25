---
title: "The Tuning Challenge"
order: 2
---

Next user story is the meat of this pair program:

> As a researcher, I want to adjust a color target and brightness threshold and see the binarized image update immediately so that I can set good detection settings before running a full processing job.

Three new things are happening at once in that story:

1. There's a non-trivial **image processing algorithm** (binarization) that needs to run on the thumbnail.
2. It needs to run **live** as the user moves sliders, without a form submit.
3. We need to draw something the browser doesn't render natively (the binarized output), which means **canvas**, not `<img>`.

This page is all theory. You're going to learn the pieces and the *why* before you write any of it. The next page is where you actually build.

## What binarization is

Binarization turns a color image into a two-color image. Every pixel becomes either "on" or "off" based on some rule. For our purposes the rule is: if a pixel's brightness is above some threshold, it's "on"; otherwise it's "off."

It's the simplest possible step toward detecting something in an image. A salamander on a light tank floor is going to be darker than the floor, so if you set the threshold somewhere between "tank floor brightness" and "salamander brightness," everything dark stays in the "on" group and you get a silhouette.

Play with the activity below. It uses a real frame from a research video. Drag the slider and watch the image on the right change.

{% activity "binarization-threshold.html", "Binarization Threshold", "520px" %}

> **With your partner:** Find a threshold value where the salamander is clearly visible as a separate shape from the background. What happens at threshold 0? At 255? At the value where the salamander first disappears, what percentage of pixels are still above? Talk about what that number means.

The thing you just did with the slider is what your app needs to do in React, except your version will also let the user pick a color (which we'll use as the "on" color) on top of the threshold.

## Why this is harder than a normal React form

Most React forms you've built so far follow the same shape: input changes, state updates, re-render shows the new value. Boom. The DOM is markup, React owns the markup, easy.

Canvas isn't markup. A `<canvas>` is a *drawing surface*, and the pixels on it aren't part of the React tree. React doesn't know what's on the canvas. To change what's on the canvas, you have to grab a reference to the actual DOM element and call `.getContext('2d')` and friends.

Worse, you also need to load the source image before you can draw it. That's an asynchronous browser thing. Once it's loaded, you want to hang on to it and re-use it every time the threshold changes (re-downloading the image on every slider drag would be insane).

So this page's job is to teach you the right way to hold onto two things that don't fit React's normal state-and-rerender model: **the canvas DOM element** and **the loaded image data**.

## Why `useState` doesn't fit

Your instinct is probably "I'll just put the loaded image in `useState` and read it whenever I redraw." That works on the second slider drag. It causes problems on the first.

Walk through what would happen:

```jsx
// Hypothetical, don't write this:
const [image, setImage] = useState(null);

useEffect(() => {
  const img = new Image();
  img.onload = () => setImage(img);
  img.src = thumbnailUrl;
}, [thumbnailUrl]);
```

Every time `setImage(img)` runs, React re-renders. The component runs top to bottom again. Anything else in state stays put, but the component function executes from scratch. That's normal for things you want to display.

But the image element itself never changes after it loads. It's the same `Image` object forever. Putting it in state means we're paying for a full React re-render for a thing that has no business causing a re-render. It also makes the timing of effects subtle: the redraw effect that depends on `[image, color, threshold]` will run when *any* of those change, including the one time the image lands.

There's a worse version of the same problem with the canvas itself. The `<canvas>` DOM element is created once and never replaced. We don't want it in state at all; we just need a reference to it.

What we want is a way to **stash a value that survives re-renders but doesn't cause them**. That's `useRef`.

## `useRef`, in two minutes

`useRef` is the third React hook you'll meet, after `useState` and `useEffect`. It creates a mutable container with a `.current` property:

```jsx
const myRef = useRef(null);
console.log(myRef.current); // null
myRef.current = 42;
console.log(myRef.current); // 42
```

Three properties of `useRef` that make it the right tool here:

1. **Changing `.current` does not trigger a re-render.** Set it, read it, mutate it; React doesn't care.
2. **The same ref object persists across re-renders.** The `myRef` you get back is the same object every time the component renders, so `.current` survives.
3. **When you put a ref on a JSX element**, React fills in `.current` with the DOM node after the element mounts.

That last one is the magic for canvas. You write:

```jsx
const canvasRef = useRef(null);

return <canvas ref={canvasRef} />;
```

After the component mounts, `canvasRef.current` is the actual `<canvas>` DOM element. You can call `canvasRef.current.getContext('2d')` and draw on it.

## How it fits together

The Preview page is going to end up with this shape:

```jsx
// State for the inputs - these DO trigger re-renders, which is what we want.
const [color, setColor] = useState('#00ff00');
const [threshold, setThreshold] = useState(128);

// Refs for the things that need to survive renders but not cause them.
const canvasRef = useRef(null);  // the <canvas> DOM element
const imgRef = useRef(null);     // the loaded Image object

// A useEffect for loading the image (runs when filename changes).
// A useEffect for redrawing (runs when imageReady or any input changes).
```

The `imgRef` holds the loaded image so we can redraw without re-loading. The `canvasRef` gives us the canvas element so we can draw on it. The state hooks hold the inputs because we want re-renders when they change, which is what triggers the redraw effect.

> **With your partner:** Without looking at the next page, sketch the shape of `Preview.jsx` together. What pieces of state does it have? What refs? What effects, and what's in their dependency arrays? You don't need to be right. You'll find out next page.

## Heads up: what to watch for

Two things will bite you on the next page if you don't know to expect them:

- **The drawing surface and the display size are different.** A `<canvas>` has CSS dimensions (how big it looks on the page) and intrinsic dimensions (how many pixels are in its drawing buffer). If you only set the CSS size, everything you draw gets stretched. Set `canvas.width` and `canvas.height` programmatically, not via CSS, to make them match.
- **Cross-origin images can taint the canvas.** If you load an image from a different origin and then try to read its pixels, the browser may refuse with a "tainted canvas" error. Set `img.crossOrigin = 'anonymous'` on the Image object before assigning `.src`, and use images served from your own origin (which is what `public/salamander1.jpg` will be) or hosts that send proper CORS headers.

Both are easier to handle if you know they exist. Both are infuriating mysteries if you don't.
