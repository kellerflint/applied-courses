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
const [color, setColor] = useState('#6b4423'); // a brown, near salamander color
const [tolerance, setTolerance] = useState(80);
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

**Why `img.crossOrigin = 'anonymous'`?** When you load an image from a different origin and then try to read its pixels (which is exactly what stage 5 does), the browser will refuse with a "tainted canvas" error if the image was loaded without CORS. Setting `crossOrigin = 'anonymous'` before assigning `.src` tells the browser to make the request CORS-style. For images served from your own origin (like `public/salamander1.jpg`) this is irrelevant. For anything cross-origin it's required.

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

## Stage 5: Binarize

The last piece. Replace the body of the redraw effect with code that reads the pixels, applies the binarization rule, and writes them back.

The placeholder algorithm: for each pixel, compute how far its RGB color is from the picked target color. If it's close (within the tolerance), it's a match and gets drawn white. Otherwise it's drawn black. The picked color is the salamander's color; matching pixels become the visible silhouette.

Below your existing `ctx.drawImage(img, 0, 0)` line, add:

```jsx
const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
const px = data.data;

const tr = parseInt(color.slice(1, 3), 16);
const tg = parseInt(color.slice(3, 5), 16);
const tb = parseInt(color.slice(5, 7), 16);

for (let i = 0; i < px.length; i += 4) {
  const dr = px[i]     - tr;
  const dg = px[i + 1] - tg;
  const db = px[i + 2] - tb;
  const distance = Math.sqrt(dr * dr + dg * dg + db * db);
  const matches = distance <= tolerance;
  px[i]     = matches ? 255 : 0;
  px[i + 1] = matches ? 255 : 0;
  px[i + 2] = matches ? 255 : 0;
}

ctx.putImageData(data, 0, 0);
```

What's happening:

- `getImageData` returns a `Uint8ClampedArray` of pixel bytes in `RGBARGBARGBA...` order, four bytes per pixel.
- The `for` loop walks four bytes at a time: index `i` is red, `i+1` green, `i+2` blue, `i+3` alpha. Alpha is left untouched.
- The picked color is parsed from its `#rrggbb` string into integer components `tr`, `tg`, `tb` once, outside the loop.
- For each pixel, `distance` is the straight-line distance from this pixel's color to the target color in RGB space. Small distance = similar colors; large distance = very different.
- If the distance is within `tolerance`, the pixel becomes white (matches the target). Otherwise it becomes black (background).
- `putImageData` writes the modified pixel array back to the canvas.

This is a placeholder algorithm. RGB distance is the simplest possible color-match rule and produces obviously imperfect masks. Your 334 course will give you a real algorithm; when you have it, replace the body of the `for` loop with your real logic and the rest of this scaffolding keeps working.

### Verify

1. Reload the page. The canvas should now show a black-and-white silhouette: white where pixels are close enough to the target color, black where they aren't.
2. Drag the tolerance slider. The amount of white area should grow as tolerance goes up (more pixels qualify as a match) and shrink as it goes down. At tolerance 0, the image should be nearly entirely black. At tolerance 255+, mostly white.
3. Change the target color. Pick something close to the salamander (a brown). The silhouette should appear. Pick something far off (bright blue). The salamander disappears.

> **With your partner:** Pick a target color close to the salamander's actual color in the original thumbnail. Adjust tolerance until just the salamander shows up as a clean silhouette. What other pixels light up at higher tolerances? Talk through why.

## What you just built

A live image processing pipeline. Inputs in React state. Image data in a ref. Canvas DOM element in a ref. Re-render triggered by input change. Effect dependency array is the wiring that ties them together.

When a future pair program adds the centroid-dot user story, it slots into this same redraw effect. After `putImageData`, you'll add a few lines that find the largest "on" region, compute its centroid, and draw a dot on the canvas with `ctx.arc(...); ctx.fill()`. Same effect, same deps, same shape.

When you swap the placeholder body for your real algorithm, the rest of the file doesn't change. The scaffolding *is* the lesson. The algorithm is yours.
