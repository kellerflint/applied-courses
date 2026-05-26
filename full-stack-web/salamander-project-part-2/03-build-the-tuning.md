---
title: "Build the Tuning"
order: 3
---

You'll build this in five stages:

1. Add the controls and their state.
2. Add the canvas element and a ref.
3. Load the image into a ref.
4. Draw the image onto the canvas.
5. Binarize the pixels.

## Stage 1: The controls

Add two new pieces of state to `Preview.jsx` and render the inputs. You need `color` and `tolerance`

A color picker is `<input type="color">`; a slider is `<input type="range">`. Both fire `onChange` with `e.target.value`. Add a small `console.log` in each `onChange` handler so you can confirm the state actually updates when you drag.

### Verify

Drag the slider and toggle the color picker. The console should show the new values each time. The page itself doesn't look different yet, which is fine.

## Stage 2: The canvas element and ref

Add a `<canvas>` to the JSX next to the thumbnail, and a ref pointing at it. Also remember the import:

```jsx
import { useRef, useState, useEffect } from 'react';
```

The ref declaration goes alongside your state:

```jsx
const canvasRef = useRef(null);
```

The element gets the ref via the `ref` prop:

```jsx
<canvas ref={canvasRef} />
```

### Verify

Open the page. The canvas is invisible right now (it's 300x150 white by default, on a white background, with no content). To prove it exists, you can add a temporary border to the `<canvas>` and reload. Remove the temp style when you're done.

## Stage 3: Load the image into a ref

You already fetch the thumbnail *URL* via the mock API. Now you need to load the URL into an actual `Image` object so you can draw it.

Two new pieces alongside your existing state and refs:

```jsx
const imgRef = useRef(null);
const [imageReady, setImageReady] = useState(false);
```

A second `useRef`, same pattern as the canvas ref. This one holds a decoded `Image` object that you'll use to read pixel data when you draw onto the canvas in stage 4. (The user-visible original thumbnail is still rendered via a regular `<img>` tag from `thumbnailUrl`, side-by-side with the canvas. This separate `Image` object is just a pixel source for the canvas drawing API; the user never sees it.)

The `imageReady` boolean is a tiny piece of state whose only job is to trigger a re-render when the image finishes loading, so the redraw effect (next stage) knows the image is available.

Then a new `useEffect` that runs when the thumbnail URL changes:

```jsx
useEffect(() => {
  if (!thumbnailUrl) return;
  setImageReady(false);
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    imgRef.current = img;
    setImageReady(true);
  };
  img.src = thumbnailUrl;
}, [thumbnailUrl]);
```

The `setImageReady(false)` at the top covers the case where the user navigates from one preview page to another with a different filename. You reset, then flip back to true once the new image loads.

**Why `img.crossOrigin = 'anonymous'`?** When you load an image from a different origin and then try to read its pixels, the browser will refuse with an error. For images served from your own origin (like `public/salamander1.jpg`) this is irrelevant, but the placeholder images in the mock data come from a different origin.

### Verify

Add a temporary `console.log('image loaded:', imgRef.current.naturalWidth, 'x', imgRef.current.naturalHeight)` inside the `onload` callback. Reload the preview page. The console should print the image dimensions once. Remove the log when you're done.

## Stage 4: Draw the image onto the canvas

Add a second `useEffect` that runs whenever the image is ready or the inputs change. For now, this effect just copies the image onto the canvas, no transformation:

```jsx
useEffect(() => {
  if (!imageReady) return;
  const img = imgRef.current;
  const canvas = canvasRef.current;
  if (!img || !canvas) return;

  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
}, [imageReady, color, tolerance]);
```

Two things worth noticing:

- **`canvas.width` and `canvas.height` get set inside the effect**, not via CSS. A canvas has two different sizes: its CSS dimensions (how big it looks on the page) and its intrinsic dimensions (how many pixels are in its drawing buffer). If you only set the CSS size, everything you draw gets stretched. Setting `canvas.width` and `canvas.height` to the image's dimensions makes the drawing buffer match the image 1:1.
- **The dependency array includes `color` and `tolerance`** even though this effect doesn't use them yet. That's deliberate. Adding them now means the redraw is already wired to re-run on input changes; in stage 5 you just add the logic that uses them.

### Verify

Reload the page. The canvas should now show the same image as the `<img>` next to it. Drag the slider and pick a new color. The canvas doesn't change yet (the inputs don't drive any logic), but the effect *is* re-running on each change. You can confirm by temporarily adding `console.log('redrawing')` at the top of the effect and watching it fire on every slider tick.

## Stage 5: Wire up the pixel pipeline

This page isn't going to teach you the binarization algorithm. That's the work you've done (or are doing) in your 334 course. This step is just the React-side plumbing that your algorithm will plug into.

Below your existing `ctx.drawImage(img, 0, 0)` line, add:

```jsx
const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
const px = data.data;

for (let i = 0; i < px.length; i += 4) {
  // px[i]     = red channel of this pixel (0-255)
  // px[i + 1] = green channel
  // px[i + 2] = blue channel
  // px[i + 3] = alpha (transparency, usually leave alone)
  //
  // Your algorithm from 334 goes here. Look at the pixel above,
  // look at `color` and `tolerance`, decide the pixel's new value,
  // and write it back the same way:
  //   px[i]     = newRed;
  //   px[i + 1] = newGreen;
  //   px[i + 2] = newBlue;
}

ctx.putImageData(data, 0, 0);
```

`getImageData` reads every pixel on the canvas into `data.data`, a flat array of bytes. The layout is RGBA, packed end-to-end: 4 bytes per pixel. For an image that's 480 × 424 pixels, that's 480 × 424 × 4 = 813,760 bytes in `data.data`. The first 4 bytes are the top-left pixel. The next 4 are the pixel right of it. And so on, row by row.

The `for` loop walks that array 4 bytes at a time. Each iteration's `i` lands on the start of the next pixel. `px[i]` is its red, `px[i+1]` its green, `px[i+2]` its blue, `px[i+3]` its alpha. Your algorithm reads those, decides what the pixel should look like, and writes the new values back to the same positions. When the loop finishes, `putImageData` pushes the whole modified array back onto the canvas in one shot.

### Now port your algorithm

You wrote a binarization algorithm in 334, in Java. Port that logic into the body of the for loop. Same shape you used there: walk the pixels, compare each to the target color and the tolerance, decide its new value, write it back. The only thing different here is the language and where you're reading and writing from.

Once it's in, reload the page. The canvas should turn into a black-and-white silhouette. Drag the tolerance slider; the silhouette grows or shrinks. Change the target color; the silhouette tracks the color you picked.

That's the user story. Everything you just built on this page is the React side. The algorithm itself is the work you already did in 334.

## What you just built

A live image processing pipeline. Inputs in React state. Image data in a ref. Canvas DOM element in a ref. Re-render triggered by input change. Effect dependency array is the wiring that ties them together. The algorithm is the only piece you'll fill in yourself.

When a future pair program adds the centroid-dot user story, it slots into this same redraw effect. After `putImageData`, you'll add a few lines that find the largest "on" region, compute its centroid, and draw a dot on the canvas with `ctx.arc(...); ctx.fill()`. Same effect, same deps, same shape.

When you add your algorithm, the rest of the file doesn't change. The scaffolding *is* the lesson.
