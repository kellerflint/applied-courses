---
title: "Build the Tuning"
order: 3
---

Time to wire it up. Same staged pattern as Part 1: build one piece, verify it works, then add the next piece.

You'll build this in five stages:

1. Add the controls and their state.
2. Add the canvas element and a ref.
3. Load the image into a ref.
4. Draw the image onto the canvas.
5. Binarize the pixels.

By the end of stage 4, you'll see the thumbnail rendered through the canvas (just a copy of the original). Stage 5 is where it becomes binarization.

## Stage 1: The controls

Add two new pieces of state to `Preview.jsx` and render the inputs. No canvas yet.

The state:

```jsx
const [color, setColor] = useState('#00ff00');
const [threshold, setThreshold] = useState(128);
```

The inputs go in your JSX somewhere below the thumbnail. A color picker is `<input type="color">`; a slider is `<input type="range">`. Both fire `onChange` with `e.target.value`. The range value comes back as a string, so wrap it in `Number(...)` before setting state.

> **With your partner:** Build these two inputs together. Add a small `console.log` in each `onChange` handler so you can confirm the state actually updates when you drag.

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

Open the page. The canvas is invisible right now (it's 300x150 white by default, on a white background, with no content). To prove it exists, briefly add a temporary {% raw %}`style={{ border: '1px solid red' }}`{% endraw %} to the `<canvas>` and reload. You should see a red rectangle. Remove the temp style when you're done.

## Stage 3: Load the image into a ref

You already fetch the thumbnail *URL* via the mock API. Now you need to load the URL into an actual `Image` object so you can draw it.

Two new pieces alongside your existing state and refs:

```jsx
const imgRef = useRef(null);
const [imageReady, setImageReady] = useState(false);
```

The `imageReady` boolean is a tiny piece of state whose only job is to trigger a re-render when the image finishes loading. The image itself lives on the ref.

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
}, [imageReady, color, threshold]);
```

Two things worth noticing:

- **`canvas.width` and `canvas.height` get set inside the effect**, not via CSS. This is the "drawing surface vs display size" gotcha from page 2. We're sizing the drawing buffer to match the source image.
- **The dependency array includes `color` and `threshold`** even though this effect doesn't use them yet. That's deliberate. Adding them now means the redraw is already wired to re-run on input changes; in stage 5 you just add the logic that uses them.

### Verify

Reload the page. The canvas should now show the same image as the `<img>` next to it. Drag the slider and pick a new color. The canvas doesn't change yet (the inputs don't drive any logic), but the effect *is* re-running on each change. You can confirm by temporarily adding `console.log('redrawing')` at the top of the effect and watching it fire on every slider tick.

## Stage 5: Binarize

The last piece. Replace the body of the redraw effect with code that reads the pixels, applies the binarization rule, and writes them back.

Below your existing `ctx.drawImage(img, 0, 0)` line, add:

```jsx
const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
const px = data.data;

const r = parseInt(color.slice(1, 3), 16);
const g = parseInt(color.slice(3, 5), 16);
const b = parseInt(color.slice(5, 7), 16);

for (let i = 0; i < px.length; i += 4) {
  const brightness = (px[i] + px[i + 1] + px[i + 2]) / 3;
  const on = brightness > threshold;
  px[i]     = on ? r : 0;
  px[i + 1] = on ? g : 0;
  px[i + 2] = on ? b : 0;
}

ctx.putImageData(data, 0, 0);
```

What's happening:

- `getImageData` returns a `Uint8ClampedArray` of pixel bytes in `RGBARGBARGBA...` order, four bytes per pixel.
- The `for` loop walks four bytes at a time: index `i` is red, `i+1` green, `i+2` blue, `i+3` alpha. Alpha is left untouched.
- The picked color is parsed from its `#rrggbb` string into integer components once, outside the loop.
- Each pixel's average brightness is compared against the threshold. Above threshold pixels become the picked color; everything else goes to black.
- `putImageData` writes the modified pixel array back to the canvas.

This is a placeholder algorithm. It uses brightness because that's the simplest possible rule that demonstrates "image responds to slider." In your 334 course, you (will) write a real color-masking algorithm that compares each pixel to the target color rather than just looking at brightness. When you have that, replace the body of the `for` loop with your real logic and the rest of this scaffolding keeps working.

### Verify

1. Reload the page. The canvas should now show a two-color version of the image: the picked color where pixels are above the threshold, black where they're below.
2. Drag the threshold slider. The amount of colored area should change immediately as you drag. Above threshold 255, the image should be entirely black. Below threshold 0, entirely colored.
3. Change the color picker. The "on" color should switch immediately.

> **With your partner:** Set the slider so the salamander silhouette is clearly visible. Talk about what's happening at the pixel level. Why does the salamander show up at *low* threshold values rather than high ones?

## What you just built

A live image processing pipeline. Inputs in React state. Image data in a ref. Canvas DOM element in a ref. Re-render triggered by input change. Effect dependency array is the wiring that ties them together.

When a future pair program adds the centroid-dot user story, it slots into this same redraw effect. After `putImageData`, you'll add a few lines that find the largest "on" region, compute its centroid, and draw a dot on the canvas with `ctx.arc(...); ctx.fill()`. Same effect, same deps, same shape.

When you swap the placeholder body for your real algorithm, the rest of the file doesn't change. The scaffolding *is* the lesson. The algorithm is yours.
